import os
import sys
import json
import requests
import logging
import time
import csv
import re
import traceback

from django.urls import reverse, resolve
from django.conf.urls import url, include
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse

from dateutil import parser as dateparser

from enrichsdk.app.utils import clean_and_validate_widgets
from enrichsdk.lib import get_credentials_by_name

logger = logging.getLogger("app")

class SalesforceClient:

    def __init__(self, cred):

        if isinstance(cred, str):
            self.cred = get_credentials_by_name(cred)
        else:
            self.cred = cred
        self.baseurl = self.cred['url']
        self.token = None
        self.salesforce_version = "v58.0"
        
    def get_token(self, force=False):
        """
        Get access token...
        """
        sample_token = {
            'access_token': '00D7j000000H9Ht!AR...',
            'instance_url': 'https://acmecompanycompany--preprod.sandbox.my.salesforce.com',
            'id': 'https://test.salesforce.com/id/00D7j000000H9HtEAK/0057j0000053bRfAAI',
            'token_type': 'Bearer',
            'issued_at': '1697972695996',
            'signature': 'BQ+dEwXSrqZcZtqXYGSYR2B+9+3eftIeBjT92Dv2YYI='
        }

        # Assumption. We dont know when the token will expire. It is
        # said to be 2 hours in documentation
        timeout = 3600*1000
        now = int(1000*time.time())
        if ((not force) and
            (self.token is not None) and
            (isinstance(self.token, dict)) and
            ('access_token' in self.token) and
            (now < (int(self.token['issued_at']) + timeout))):
            return self.token['access_token']

        tokenurl = self.baseurl + "/services/oauth2/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        # Construct the oauth request
        cred = self.cred
        data = {
            "grant_type": "password",
            "client_id": cred['client_id'],
            "client_secret": cred['client_secret'],
            "username": cred['username'],
            "password": cred['password'] + cred['client_security_token']
        }

        msg = ""
        msg += f"Token URL: {tokenurl}\n"
        for k, v in data.items():
            if k != "password":
                msg += f"{k}: {str(v)[:8]}...\n"
            else:
                msg += f"{k}: ****...\n"
            result = requests.post(tokenurl, data=data, headers=headers)
        try:
            self.token = result.json()
            if result.status_code == 200:
                logger.debug("Salesforce token obtained",
                             extra={
                                 'data': msg
                             })
            else:
                logger.error("Failed to obtained Salesforce token",
                             extra={
                             'data': msg + str(result.content)
                             })
        except:
                logger.exception("Failed to obtained Salesforce token",
                             extra={
                             'data': msg + str(result.content)
                             })

        return self.token['access_token']

    def access_salesforce(self, url, method="get",
                          params={}, data={},
                          request=None):

        token = self.get_token()
        url = self.baseurl + url
        headers = {
            'Authorization': f"Bearer {token}"
        }

        if method == "get":
            result = requests.get(url, params=params, headers=headers)
        elif method == "post":
            result = requests.post(url, params=params, headers=headers, json=data)
        elif method == "patch":
            result = requests.patch(url, params=params, headers=headers, json=data)
        else:
            raise Exception(f"Unknown access method: {method}")

        if result.status_code >= 400:
            logger.error("Failed to access Salesforce",
                         extra={

                             'data': f"URL: {url}\nOutput: {result.content}"
                         })
        try:
            if method != "patch":
                status, result = result.status_code, result.json()
            else:
                status, result = result.status_code, {}

            # [{"message":"Jurisdiction: bad value for restricted picklist field: State of Washington","errorCode":"INVALID_OR_NULL_FOR_RESTRICTED_PICKLIST","fields":["Jurisdiction__c"]}]
            if ((request is not None) and
                (isinstance(result, (dict, list))) and
                (len(result) > 0)):
                res = result
                if isinstance(res, list):
                    res = res[0]
                if isinstance(res, dict) and ("message" in res):
                    messages.error(request, "Salesforce message: " + res['message'])

            if 'nextRecordsUrl' in result:
                messages.error(request, "Internal error. A few search results were not processed. Please contact support")

            return status, result
        except:
            logger.exception("Failed to access Salesforce",
                             extra={
                                 'data': f"URL: {url}\n"
                             })

        raise Exception("Failed to access Salesforce")

    def run_query(self, query, request=None):

        query = re.split(r"\s+", query)
        query = "+".join(query)
        opurl = f"/services/data/{self.salesforce_version}/query/?q={query}"

        status, result = self.access_salesforce(opurl, request=request)
        if status >= 400:
            raise Exception("Failed to run query")
        return result

    def get_opportunity_by_id(self, oppid, request=None):

        opurl = f"/services/data/{self.salesforce_version}/sobjects/Opportunity/{oppid}"
        status, result = self.access_salesforce(opurl, request=request)
        if status >= 400:
            raise Exception("Failed to get opportunity")
        return result

    def describe_opportunity(self, request=None):

        opurl = f"/services/data/{self.salesforce_version}/sobjects/Opportunity/describe"
        status, result = self.access_salesforce(opurl, request=request)
        if status >= 400:
            raise Exception("Failed to describe opportunity")
        return result

    def get_opportunities(self, limit=200, columns=None, request=None):

        fields = "FIELDS(ALL)"
        if columns is not None:
            fields = ",".join(columns)

        opurl = f"/services/data/{self.salesforce_version}/query/?q=SELECT+{fields}+FROM+Opportunity+ORDER+BY+LastModifiedDate+DESC+LIMIT+{limit}"

        status, result = self.access_salesforce(opurl, request=request)
        if status >= 400:
            raise Exception("Failed to query for opportunities")
        return result

    def get_opportunity_detail(self, oppid, request=None):

        opurl = f"/services/data/{self.salesforce_version}/sobjects/Opportunity/{oppid}"

        status, result = self.access_salesforce(opurl, request=request)
        if status >= 400:
            raise Exception("Failed to get opportunity detail")
        return result

    def add_opportunity(self, data, request=None):
        opurl = f"/services/data/{self.salesforce_version}/sobjects/Opportunity"
        status, result = self.access_salesforce(opurl, method="post", data=data, request=request)
        if status >= 400:
            raise Exception("Failed to add opportunity")
        return result

    def update_opportunity(self, oppid, data, request=None):
        opurl = f"/services/data/{self.salesforce_version}/sobjects/Opportunity/{oppid}"
        status, result = self.access_salesforce(opurl,
                                                method="patch",
                                                data=data,
                                                request=request)
        if status >= 400:
            raise Exception("Failed to add opportunity")
        return result

    def get_accounts(self, limit=200, columns=None, request=None):

        fields = "FIELDS(ALL)"
        if columns is not None:
            fields = ",".join(columns)

        opurl = f"/services/data/{self.salesforce_version}/query/?q=SELECT+{fields}+FROM+Account+ORDER+BY+LastModifiedDate+DESC+LIMIT+{limit}"

        status, result = self.access_salesforce(opurl, request=request)
        if status >= 400:
            raise Exception("Failed to query for opportunities")
        return result

    def add_account(self, data, request=None):
        opurl = f"/services/data/{self.salesforce_version}/sobjects/Account"
        status, result = self.access_salesforce(opurl,
                                                method="post",
                                                data=data, request=request)
        if status >= 400:
            raise Exception("Failed to add account")
        return result

    def get_account_by_id(self, accid, request=None):

        opurl = f"/services/data/{self.salesforce_version}/sobjects/Account/{accid}"
        status, result = self.access_salesforce(opurl, request=request)
        if status >= 400:
            raise Exception(f"Failed to get account details: {accid}")
        return result

#############################################
#=> Fields in Salesforce Opportunity Object
#############################################
# Account_Name__c: null,
# Account_Region__c: null,
# Active_Headcount__c: null,
# Amount: 4810308.0,
# Amount_Lost__c: 0.0,
# Amount_M__c: 5.0,
# LastActivityDate: null,
# LastAmountChangedHistoryId: null,
# LastCloseDateChangedHistoryId: null,
# LastModifiedById: 0057j0000053bRfAAI,
# LastModifiedDate: 2023-10-19T17:37:53.000+0000,
# ....

class SalesforceBaseMixin:

    def salesforce_update_urlpatterns(self, prefix, urlpatterns):
        urlpatterns.extend([
            url(f'^{prefix}[/]?$', self.salesforce_index, name="salesforce_index"),
            url(f'^{prefix}/detail/(?P<oppid>[a-zA-Z0-9]+)[/]?$', self.salesforce_detail, name="salesforce_detail"),
        ])

    def salesforce_update_templates(self, templates):
        templates.update({
            'salesforce_index': 'sharedapp/generic_index.html',
            'salesforce_detail': 'sharedapp/generic_index.html',
        })

    def get_client(self, request, spec):

        # Get the salesforce client...
        cred = spec['cred']
        cred = get_credentials_by_name(cred)
        if hasattr(self, "salesforce_client"):
            client = self.salesforce_client
        else:
            client = self.salesforce_client = SalesforceClient(cred)

        return cred, client

    #################################################################
    # All Salesforce
    #################################################################
    def salesforce_index_get_extra_header_components(self, request, spec):

        r = resolve(request.path)
        return []

    def salesforce_index_finalize_entry(self, request, spec, opportunity, entry):
        return entry

    def salesforce_index_finalize_widgets(self, request, spec,
                                          opportunities, widgets):
        return widgets

    def salesforce_index_get_extra_actions(self, request, spec,
                                           opportunity,
                                           entry):
        return {}, []

    def salesforce_index_get_opportunities(self, request, spec):

        cred, client = self.get_client(request, spec)

        opportunities = client.get_opportunities(columns=[
            "Name",
            "Amount",
            "Id",
            "CreatedDate"
        ], request=request)

        return opportunities
    
    def salesforce_index_get_columns(self, request, spec, data):

        columns = [
            "Added", 'Name', "Amount (M$)",
        ]

        workflowcols = []
        detailcols = []
        
        if len(data) > 0: 
            for k in data[0].keys():
                if k in columns:
                    continue
                if k.startswith("ACTION_"):
                    detailcols.append(k)
                else:
                    workflowcols.append(k)
        columns += [
            ('Workflow', workflowcols),
            ('Details', detailcols)
        ]
        return columns

    def salesforce_index_finalize_data(self, request, spec, data):
        return data
    
    def salesforce_index(self, request, spec):

        r = resolve(request.path)

        usecase = spec['usecase']
        namespace = spec['namespace']
        cred = get_credentials_by_name(spec['cred'])
        
        # First get the opportunities
        opportunities = self.salesforce_index_get_opportunities(request, spec)
        
        workflowcols = []
        data = []
        for o in opportunities.get('records',[]):

            amount = o['Amount']
            if amount is None:
                amount = 0
            amount = round(amount/10**6, 1)
            
            dt = dateparser.parse(o['CreatedDate'])
            detailurl = reverse(r.namespace + ":salesforce_detail",
                                kwargs={
                                    'oppid': o['Id']
                                })
            entry = {
                "Added": dt.replace(microsecond=0).strftime("%Y-%m-%d"),
                "Amount (M$)": amount,
                "ACTION_SALESFORCE": {
                    "title": "Details",
                    "alt": "",
                    "class": "",
                    "template": "action_icon_compact",
                    "target": "_blank",
                    "icon": "salesforce_24x24",
                    "url": f"{cred['url']}/{o['Id']}"
                },
            }

            # Any cleanup before adding extra actions...
            entry = self.salesforce_index_finalize_entry(request, spec, o, entry)

            # Now add actions...
            extra, order = self.salesforce_index_get_extra_actions(request, spec, o, entry)
            entry.update(extra)

            data.append(entry)


        # How should I structure the output columns
        columns = self.salesforce_index_get_columns(request, spec, data)
        
        # Any header actions..
        extra_header_components = self.salesforce_index_get_extra_header_components(request, spec)

        widget = {
            "name": "Opportunities in Salesforce",
            "description": f"Recent entries and not the complete list",
            "type": "full_width_table_compact_actions",
            "columns": columns,
            "search": True,
            "rows": data,
            "order": [[0, "desc"]],
            "td_class": "white-space-normal wordwrap",
            "thead_th_class": "",
            "header_components": {
                "components": [
                    {
                        "template": "action_search"
                    }
                ]
            }
        }

        widgets = [widget]

        # Do any extra cleanup
        widgets = self.salesforce_index_finalize_widgets(request, spec,
                                                         opportunities,
                                                         widgets)

        clean_and_validate_widgets(widgets)

        data = {
            "title": "Salesforce",
            "sidebar_targets": self.get_sidebar(request, spec),
            "breadcrumb": "Salesforce",
            "widgets": widgets
        }

        # Cleanup and add any final note..
        data = self.salesforce_index_finalize_data(request, spec, data)
        
        template = self.get_template(spec, 'salesforce_index')
        return render(request,
                      template,
                      {
                          'app': self,
                          'usecase': usecase,
                          'spec': spec,
                          'basenamespace': r.namespace,
                          'data': data
                      })

    def salesforce_detail(self, request, spec, oppid):

        cred, client = self.get_client(request, spec)

        r = resolve(request.path)

        usecase = spec['usecase']
        namespace = spec['namespace']

        widgetspecs = []

        # => Get the opportunity object...
        detail = client.get_opportunity_by_id(oppid, request=request)
        accounts = {}
        data = []
        for name, value in detail.items():
            if not isinstance(value, str):
                value = str(value)
            data.append({
                "Attribute": name,
                "Value": value
            })

        plan_name = detail['Plan_Names_and_Registration_Numbers__c']
        plan_name = str(plan_name)
        widgetspecs.append({
            "name": plan_name,
            "description": "Opportunity detail in Salesforce",
            "data": data
        })

        # Get the consultant and plan sponsor objects as well..
        for name, label in [
                ['AccountId', "Plan Sponsor"],
                ['Intermediary__c', "Consultant"]
        ]:
            idval = detail[name]
            if idval is None:
                continue
            accdetail = client.get_account_by_id(idval, request)
            data = []
            for name, value in accdetail.items():
                if not isinstance(value, str):
                    value = str(value)
                data.append({
                    "Attribute": name,
                    "Value": value
                })
            widgetspecs.append({
                "name": f"{label} - {accdetail['Account_Short_Name__c']}",
                "description": "Details of account",
                "data": data
            })

        columns = [
            "Attribute", "Value"
        ]

        widgets = []
        for widgetspec in widgetspecs:
            widget = {
                "name": widgetspec['name'],
                "description": widgetspec['description'],
                "type": "full_width_table_compact_actions",
                "columns": columns,
                "search": True,
                "rows": widgetspec['data'],
                "order": [[0, "asc"]],
                "td_class": "white-space-normal wordwrap",
                "thead_th_class": "",
                "header_components": {
                    "components": [
                        {
                            "template": "action_search"
                        }
                    ]
                }
            }
            widgets.append(widget)

        clean_and_validate_widgets(widgets)

        data = {
            "title": "Salesforce",
            "sidebar_targets": self.get_sidebar(request, spec),
            "breadcrumbs": [
                {
                    "name": "Salesforce",
                    "url": reverse(r.namespace + ":salesforce_index"),
                },
                {
                    "name": "Detail"
                }
            ],
            "widgets": widgets
        }

        template = self.get_template(spec, 'salesforce_detail')
        return render(request,
                      template,
                      {
                          'app': self,
                          'usecase': usecase,
                          'spec': spec,
                          'basenamespace': r.namespace,
                          'data': data
                      })


class SalesforceDatasetMixin:
    """
    Code had handles the integration between salesforce and Dataset
    """
    def salesforce_dataset_update_urlpatterns(self, prefix, urlpatterns):

        urlpatterns.extend([
            url(f'^{prefix}/post/(?P<datasetpk>[0-9a-zA-Z-_ .]+)/action[/]?$', self.salesforce_dataset_action, name="salesforce_dataset_action"),
            url(f'^{prefix}/post/(?P<datasetpk>[0-9a-zA-Z-_ .]+)/select[/]?$', self.salesforce_dataset_select, name="salesforce_dataset_select"),
            url(f'^{prefix}/post/(?P<datasetpk>[0-9a-zA-Z-_ .]+)/verify[/]?$', self.salesforce_dataset_verify, name="salesforce_dataset_verify"),
        ])

    def salesforce_dataset_update_templates(self, templates):
        templates.update({
            'salesforce_dataset_action': 'sharedapp/generic_index.html',
            'salesforce_dataset_verify': 'sharedapp/generic_index.html',
            'salesforce_dataset_select': 'sharedapp/generic_index.html'
        })

    def get_salesforce_fieldmapping(self, ):

        # Map each local name to the Salesforce fields..
        filename = os.path.join(os.path.dirname(__file__),
                                "fieldmapping.csv")
        mapping = {}
        for row in list(csv.DictReader(open(filename))):
            if row['Name'] in ['']:
                continue
            mapping[row.pop("Name")] = row

        return mapping

    def find_overlap(self, new, existing):

        if not isinstance(existing, str) or len(existing) == 0:
            return 0

        skip = ['pension', 'plan', 'inc']

        new = re.split(r"[\s\.,]+", new.lower().strip())
        new = [n for n in new if len(n) >= 3 and (n not in skip)]
        if len(new) == 0:
            return 0

        existing = re.split(r"[\s\.,]+", existing.lower().strip())
        existing = [n for n in existing if len(n) >= 3 and (n not in skip)]
        if len(existing) == 0:
            return 0

        overlap = len([x for x in new if x in existing])/len(existing)
        overlap = int(overlap * 100)

        return overlap

    def find_closest(self, lookup, names):

        overlaps = []
        for name in names:
            overlap = self.find_overlap(lookup, name)
            overlaps.append((name, overlap))

        overlaps = sorted(overlaps, key=lambda x: x[1], reverse=True)
        if ((len(overlaps) > 0) and (overlaps[0][1] > 50)):
            return overlaps[0]
        return None, 0

    def salesforce_dataset_select(self, request, spec, datasetpk):
        """
        Select whether to create or update
        """

        usecase = spec['usecase']
        namespace = spec['namespace']
        r = resolve(request.path)

        cred, client = self.get_client(request, spec)

        dataseturl = reverse(r.namespace + ":dataset_index")
        validateurl = reverse(r.namespace + ":dataset_validate",
                              kwargs={
                                  'pk': datasetpk
                              })
        verifyurl = reverse(r.namespace + ":salesforce_dataset_verify",
                        kwargs={
                                'datasetpk': datasetpk
                        })

        redirect = HttpResponseRedirect(validateurl)

        # => Get models
        LLMDatasetModel = self.get_model(spec, 'llmdataset')

        # Get the dataset
        try:
            dataset = LLMDatasetModel.objects.get(pk=datasetpk)
        except LLMDatasetModel.DoesNotExist:
            messages.error(request, 'Invalid dataset')
            return HttpResponseRedirect(reverse(r.namespace + ":dataset_index"))

        ##########################################################
        # => First get all the model parameters
        ##########################################################
        try:
            modelvars = dataset.values.get('modelvar', [])
            if len(modelvars) == 0:
                messages.error(request, "Not posted. Please save first")
                return redirect

            # Convery into a dictionary
            modelvars = { v['name'] : v['value'] for v in modelvars}

        except:
            logger.exception("Unable to post to salesforce")
            messages.error(request, 'Internal error. Unable to post to salesforce')
            return redirect

        ##########################################################
        #=> Extract Some basic information...
        ##########################################################
        plan_name = modelvars['Plan Name']
        plan_sponsor = modelvars['Plan Sponsor']
        consultant = modelvars['Consultant']

        ##########################################################
        #=> Now search last 200 or so opportunities
        ##########################################################
        opportunities = client.get_opportunities(columns=[
            "Plan_Names_and_Registration_Numbers__c",
            "Account_Name__c",
            "Active_Headcount__c",
            'Product_Type__c',
            "CreatedDate",
            "Amount",
            "Situs_State__c",
            "Intermediary_Short_Name__c",
            "Id"
        ], request=request)
        data = []
        for o in opportunities.get('records',[]):
            dt = dateparser.parse(o['CreatedDate'])
            actives = o["Active_Headcount__c"]
            if actives is not None:
                actives = int(actives)
            amount = o['Amount']
            if amount is None:
                amount = 0
            amount = round(amount/10**6, 1)
            detailurl = reverse(r.namespace + ":salesforce_detail",
                                kwargs={
                                    'oppid': o['Id']
                                })

            overlap = self.find_overlap(plan_name, o['Plan_Names_and_Registration_Numbers__c'])

            data.append({
                "Conflict Score": overlap,
                "Added": dt.replace(microsecond=0).strftime("%Y-%m-%d %H:%M"),
                "Name": f'<a href="{detailurl}">{o["Plan_Names_and_Registration_Numbers__c"]}</a>',
                "Plan Sponsor": o['Account_Name__c'],
                "Consultant": o['Intermediary_Short_Name__c'],
                "Product Type": o['Product_Type__c'],
                "State": o["Situs_State__c"],
                "Actives": actives,
                "Amount (M$)": amount,
                "ACTION_EDIT": {
                    "title": "Edit This Opportunity",
                    "alt": "",
                    "class": "btn",
                    "template": "action_icon_compact",
                    "icon": "edit_24dp_1",
                    "text": "Update",
                    "url": verifyurl + f"?action=edit&opportunityid={o['Id']}"
                },
            })

        columns = [
            "Conflict Score", "Added", 'Name', "Plan Sponsor",
            "Consultant", "Product Type", "State", "Actives",
            "Amount (M$)",
            ("Action", ["ACTION_EDIT"])
        ]

        widget = {
            "name": "Existing Opportunities in Salesforce",
            "description": "Select opportunity to edit. Note that this shows ONLY the most recent 200 opportunities",
            "type": "full_width_table_compact_actions",
            "columns": columns,
            "search": True,
            "rows": data,
            "order": [[0, "desc"], [1, "desc"]],
            "td_class": "white-space-normal wordwrap",
            "thead_th_class": "",
            "header_components": {
                "components": [
                    {
                        "template": "action_search"
                    }
                ]
            }
        }

        widgets = [widget]

        #=> Add notes..
        widget = {
            "name": f"Opportunity - {plan_name}",
            "description": "Notes on the post",
            "type": "full_width_form",
            "submit": "Create",
            "action": verifyurl,
            "hidden_vars": {
                "action": "create"
            },
            "text": f"""\
<ol>
<li>Plan Name: {plan_name}</li>
<li>Plan Sponsor: {plan_sponsor}</li>
<li>Consultant: {consultant}</li>
</ol>""",
            "td_class": "white-space-normal wordwrap",
            "header_components": {
                "components": [
                    {
                        "template": "action_icon_compact",
                        "icon": "add_circle_outline_24dp_1",
                        "url": verifyurl + f"?action=create",
                        "title": "Create new opportunity",
                    },
                ]
            }
        }
        widgets.insert(0, widget)

        widget = {
            "name": "RFP Workflow",
            "type": "workflow",
            "order": [
                {
                    "name": "Upload RFP",
                    "url": dataseturl
                },
                {
                    "name": "Validate Variables",
                    "url": validateurl
                },
                "Prepare Post to Salesforce",
                "Approve Post to Salesforce",
            ],
            "currpos": 2,
            "class": "mb-2"
        }
        widgets.insert(0, widget)

        clean_and_validate_widgets(widgets)

        data = {
            "title": "Select Whether to Update or Create Opportunity",
            "sidebar_targets": self.get_sidebar(request, spec),
            "breadcrumbs": [
                {
                    "name": "Datasets",
                    "url": reverse(r.namespace + ":dataset_index")
                },
                {
                    "name": "Validate",
                    "url": validateurl
                },
                {
                    "name": "Approve Salesforce Post"
                }
            ],
            "widgets": widgets
        }

        template = self.get_template(spec, 'salesforce_dataset_select')
        return render(request,
                      template,
                      {
                          'app': self,
                          'usecase': usecase,
                          'spec': spec,
                          'basenamespace': r.namespace,
                          'data': data,
                      })

    def salesforce_dataset_verify(self, request, spec, datasetpk):
        """
        Post to salesforce
        """

        usecase = spec['usecase']
        namespace = spec['namespace']
        r = resolve(request.path)

        action = request.GET.get('action', None)
        action_oppid = request.GET.get('opportunityid', None)
        action_oppid = None if str(action_oppid).lower() == "none" else action_oppid

        dataseturl = reverse(r.namespace + ":dataset_index")
        validateurl = reverse(r.namespace + ":dataset_validate",
                              kwargs={
                                  'pk': datasetpk
                              })
        redirect = HttpResponseRedirect(validateurl)
        selecturl = reverse(r.namespace + ":salesforce_dataset_select",
                              kwargs={
                                  'datasetpk': datasetpk
                              })
        selectredirect = HttpResponseRedirect(selecturl)

        # => Is this an edit or create...
        if action not in ['create', 'edit']:
            messages.error(request, f"Invalid salesforce action. Should be create or edit. Not {action}")
            return selectredirect

        if ((action == "edit") and
            ((not isinstance(action_oppid, str)) or
             (len(action_oppid) <= 16))):
            messages.error(request, f"Invalid salesforce opportunity ID. Should have atleast 16 characters {len(action_oppid)}")
            return selectredirect

        cred, client = self.get_client(request, spec)

        # => Get models
        LLMDatasetModel = self.get_model(spec, 'llmdataset')

        # Get the dataset
        try:
            dataset = LLMDatasetModel.objects.get(pk=datasetpk)
        except LLMDatasetModel.DoesNotExist:
            messages.error(request, 'Invalid dataset')
            return HttpResponseRedirect(reverse(r.namespace + ":dataset_index"))

        ##########################################################
        # => First get all the model parameters
        ##########################################################
        try:
            modelvars = dataset.values.get('modelvar', [])
            if len(modelvars) == 0:
                messages.error(request, "Not posted. Please save first")
                return redirect

            # Convery into a dictionary
            modelvars = { v['name'] : v['value'] for v in modelvars}

        except:
            logger.exception("Unable to post to salesforce")
            messages.error(request, 'Internal error. Unable to post to salesforce')
            return redirect

        ##########################################################
        #=> Some basic information...
        ##########################################################
        plan_name = modelvars['Plan Name']
        plan_sponsor = modelvars['Plan Sponsor']
        consultant = modelvars['Consultant']

        ##########################################################
        #=> Add account information
        ##########################################################
        accounts = client.get_accounts()
        accounts = accounts.get('records', [])
        choices = {}
        chosen = {}
        for a in accounts:
            if a['Type'] not in choices: # Plan Sponsor, Legal Counsel
                choices[a['Type']] = { "Create": "Create"}
            choices[a['Type']][a['Name']] = a['Id']

        fieldmap = {
            "Plan Sponsor": "Plan Sponsor",
            "Consultant": "Intermediary",
        }

        for fieldname, account_type in fieldmap.items():
            fieldvalue = modelvars[fieldname]
            if fieldvalue.strip().lower() in ['no', 'none', 'n/a']:
                continue
            # Find closest account name. if nothing is found, then use# create
            closest_name, closest_score = self.find_closest(fieldvalue,
                                                            list(choices[account_type].keys()))
            if closest_score > 50:
                chosen[fieldname] = choices[account_type][closest_name]
            else:
                chosen[fieldname] = "Create"

        ##########################################################
        # => Existing opportunity
        ##########################################################
        opportunity = {}
        if action == "edit":
            try:
                opportunity = client.get_opportunity_by_id(action_oppid, request=request)
            except:
                logger.exception(f"Invalid opportunity ID: {action_oppid}")
                return selectredirect

        ##########################################################
        # => Now construct the widgets...
        ##########################################################
        mapping = self.get_salesforce_fieldmapping()
        def detect_change(e):
            existing = e['Existing Value']
            new = e['Salesforce Field Value']
            # print(e['Column'], existing, new, end="")
            if (((existing in [None, '', "None"]) and (new in [None, '', "None"])) or
                (existing == new)):
                return "<i class='fa fa-check' style='color: green'></i> YES"
            return "<i class='fa fa-exclamation-triangle' style='color: red'></i> NO"

        lookups = []
        unmapped = []
        mapped = []

        # => Add the first entry...
        entry = {
            "Column": "Name",
            "Value": plan_name,
            "Salesforce Field Name": "Plan Name(s) and Registration Number(s)",
            "Salesforce Field API": "Plan_Names_and_Registration_Numbers__c",
            "Salesforce Field Value": plan_name,
            "Existing Value": opportunity.get('Plan_Names_and_Registration_Numbers__c',"")
        }
        entry['Match'] = detect_change(entry)
        # mapped.append(entry)

        error_fields = []
        # => Now add the rest of the entries...
        for k, v in modelvars.items():

            # this is a computed field...
            if k == "Total Participants":
                continue

            #
            is_mapped = mapping.get(k,{}).get("Salesforce Field Name", "") != ""
            notes = mapping.get(k, {}).get("Notes", "")
            field_name = mapping.get(k, {}).get("Salesforce Field Name","Plan Provision Comments2")
            field_api_name = mapping.get(k,{}).get("Salesforce Field API","Plan_Provision_Comments2__c")
            v1 = self.field_specific_cleanup(k, v)

            if (v is not None) and (v1 is None):
                error_fields.append(k)

            entry = {
                "Column": k,
                "Value": v,
                "Salesforce Field Name": field_name,
                "Salesforce Field API": field_api_name,
                "Salesforce Field Value": v1,
                "Existing Value": opportunity.get(field_api_name, "")
            }

            if (("lookup" in notes.lower()) or ("." in mapping.get(k,{}).get("Salesforce Field API",""))):
                # Related fields..
                if k not in ['Plan Sponsor', 'Consultant', "Company Description (Internal)"]:
                    entry.update({
                        "Salesforce Field Name": "Plan Provision Comments2",
                        "Salesforce Field API": "Plan_Provision_Comments2__c"
                    })
                elif k == "Company Description (Internal)":
                    entry.update({
                        "Salesforce Field Name": "Account.Notes__c",
                        "Salesforce Field API": "Account.Notes__c",
                        "Salesforce Field Value": "",
                        "Existing Value": "",
                    })
                elif k == 'Plan Sponsor':
                    field_api_name = "AccountId"
                    if "Account_Name__c" in opportunity:
                        existing = f"{opportunity['Account_Name__c']} ({opportunity['AccountId']})"
                    else:
                        existing = ""
                    entry.update({
                        "Salesforce Field Name": "AccountId",
                        "Salesforce Field API": field_api_name,
                        "Salesforce Field Value": v1 + f" ({chosen[k]})",
                        "Existing Value": existing,
                    })
                elif k == 'Consultant':
                    # Should I include it?
                    if ((v is None) and (opportunity.get('Intermediary_Short_Name__c', None) is None)):
                        # Dont include it...
                        continue

                    if 'Intermediary_Short_Name__c' in opportunity:
                        existing = f"{opportunity['Intermediary_Short_Name__c']} ({opportunity['Intermediary__c']})"
                    else:
                        existing = ""
                    entry.update({
                        "Salesforce Field Name": "Intermediary",
                        "Salesforce Field API": "Intermediary__c",
                        "Salesforce Field Value": v1 + f" ({chosen[k]})",
                        "Existing Value": existing,
                    })
                lookups.append(entry)
            elif is_mapped:
                mapped.append(entry)
            else:
                entry.update({
                    "Salesforce Field Name": "Not Posted",
                    "Salesforce Field API": "N/A",
                    "Existing Value": ""
                })
                unmapped.append(entry)

            # Add a check for all fields...
            entry["Match"] = detect_change(entry)

            if k == "Final Quote":
                entry = {
                    "Column": "Closing Date",
                    "Value" : v,
                    "Salesforce Field Name": "CloseDate",
                    "Salesforce Field API": "CloseDate",
                    "Salesforce Field Value": v1,
                    "Existing Value": opportunity.get("CloseDate",""),
                }
                entry["Match"] = detect_change(entry)
                mapped.append(entry)


        columns = [
            "Column", "Value", "Salesforce Field Name", "Salesforce Field API", "Salesforce Field Value",
        ]

        ordercol = 0
        if action == "edit":
            columns.extend(["Existing Value", "Match"])
            ordercol = 6
        widgets = []
        for name, description, data in [
                ("Mapped", "Posted directly to variables", mapped),
                ("Account", "Not posted. These are special columns that require more work. They are included in Plan Provision Comments for now", lookups),
                ("Unmapped","Not posted. They are included in the Plan Provision Comments2 field via the comment form at the bottom", unmapped)
        ]:
            if len(data) == 0:
                continue

            # Cleanup the unmapped table.This is not posted...
            if name == "Unmapped":
                for d in data:
                    d['Match'] = ""

            widget = {
                "name": f"{plan_name} - {name} Attributes",
                "description": description,
                "type": "full_width_table_compact_actions",
                "columns": columns,
                "search": True,
                "rows": data,
                "order": [[ordercol, "asc"]],
                "td_class": "white-space-normal wordwrap",
                "thead_th_class": "",
                "header_components": {
                    "components": [
                        {
                            "template": "action_search"
                        }
                    ]
                }
            }

            widgets.append(widget)

        #=> Add notes..
        notes ="""<ol>\n"""
        if action == "edit":
            notes += f"<li><strong>NOTE: You are editing an existing Opportunity ({opportunity['Plan_Names_and_Registration_Numbers__c']})</strong></li>"
        else:
            notes += f"<li><strong>NOTE: You are creating a new Opportunity </strong></li>"
        notes += """\
<li>Fields that require more work or cant be mapped are to be found in the Plan Provision Comments</li>
<li>Please review existing opportunity, intermediary, and sponsor lists</li>
<li>Some fields require default values such as CloseDate (same as Submission date) and Name (dummy value that is rewritten)</li>"""
        notes += """</ol>"""

        widget = {
            "name": f"{plan_name} - Instructions & Notes",
            "description": "Notes on the post",
            "type": "full_width_text",
            "text": notes,
            "td_class": "white-space-normal wordwrap",
        }
        widgets.insert(0, widget)

        widget = {
            "name": "RFP Workflow",
            "type": "workflow",
            "order": [
                {
                    "name": "Upload RFP",
                    "url": dataseturl
                },
                {
                    "name": "Validate Variables",
                    "url": validateurl
                },
                {
                    "name": "Prepare Post to Salesforce",
                    "url": selecturl,
                },
                "Approve Post to Salesforce"
            ],
            "currpos": 3,
            "class": "mb-2"
        }
        widgets.insert(0, widget)

        consultant_select = []
        if consultant not in [None, '', 'None', 'NO', 'N/A']:
            consultant_select = [
                {
                    "type": "select",
                    "name": "consultantid",
                    "id": "consultantid",
                    "label": f"Consultant/Intermediary ({consultant})",
                    "choices": choices['Intermediary'],
                    "selected_choice": chosen['Consultant']
                }
            ]
        else:
            consultant_select = [
                {
                    "type": "donothing",
                    "text": "noop consultant specified"
                }
            ]

        widget = {
            "name": f"{plan_name} - Post to Salesforce?",
            "description": "Take action on the above content",
            "type": "full_width_form",
            "text": """
<ol>
<li>Please check for conflict score in the above widget and proceed only if there is no conflict</li>
<li>If the Plan Sponsor or Intermediary/Consultant is missing, pressing yes will first create those accounts before proceeding</li>
</ol>
            """,
            "hidden_vars": {
                "action": action,
                "opportunityid": action_oppid,
            },
            "elements": [
                {
                    "type": "select",
                    "name": "stagename",
                    "id": "stagename",
                    "label": "StageName",
                    "choices": [
                        "Execution",
                        "Long Term",
                    ],
                    "selected_choice": "Long Term",
                },
                {
                    "type": "select",
                    "name": "accountid",
                    "id": "accountid",
                    "label": f"Plan Sponsor ({plan_sponsor})",
                    "choices": choices['Plan Sponsor'],
                    "selected_choice": chosen['Plan Sponsor']
                }] + consultant_select + [
                {
                    "type": "textarea",
                    "name": "comments",
                    "id": "comments",
                    "rows": 5,
                    "cols": 120,
                    "placeholder": "Please enter any comments here. It will be into the Plan Provision Comments2 field",
                    "label": f"Comments",
                },

            ],
            "action": reverse(r.namespace + ":salesforce_dataset_action",
                              kwargs={
                                  'datasetpk': datasetpk
                              }),
            "submit": "Yes!!",
            "submit_class": "confirmbtn",
            "submit_header": "Confirm Post to Salesforce",
            "submit_body": "By clicking Yes you are confirming the accuracy of the data. Once you click, the data will be sent to salesforce. In case of an update, any prior data will be overwritten in a non reversible manner and for a new record, a duplicate may be created. Please verify on salesforce",
            "td_class": "white-space-normal wordwrap",
        }

        widgets.append(widget)


        clean_and_validate_widgets(widgets)

        data = {
            "title": "Approve Post to Salesforce",
            "sidebar_targets": self.get_sidebar(request, spec),
            "breadcrumbs": [
                {
                    "name": "Datasets",
                    "url": reverse(r.namespace + ":dataset_index")
                },
                {
                    "name": "Validate",
                    "url": validateurl
                },
                {
                    "name": "Approve Salesforce Post"
                }
            ],
            "widgets": widgets
        }

        # Make note of any errors you may have seen
        if len(error_fields) > 0:
            messages.warning(request, f"Please double check the following fields: {','.join(error_fields)}")

        template = self.get_template(spec, 'salesforce_dataset_verify')
        return render(request,
                      template,
                      {
                          'app': self,
                          'usecase': usecase,
                          'spec': spec,
                          'basenamespace': r.namespace,
                          'data': data,
                      })

    def field_specific_cleanup(self, field, value):

        if value in [None,'']:
            return value

        # Boolean fields...
        if field in ["AIK"]:
            value = "Yes" if str(value).lower() in ['yes', 'y'] else "No"

        if field in ["MED"]:
            value = str(value) in ['yes', 'y']

        if field in ['#/% Actives', '#/% Deferred', '#/% In-Pay']:
            try:
                if not isinstance(value, int):
                    value = str(value)
                    value = value.replace(",","")
                    value = int(value)
            except:
                traceback.print_exc()
                value = None

        # Floating point number
        if field in ['Estimated Size']:
            matches = re.findall(r"\d+[\.\d+]?", value.replace(",",""))
            if matches is None:
                value = None
            else:
                value = float(matches[0])
                if value > 10**6:
                    # exact number is mentioned.
                    value = round(value/10**6, 2)

        if field in ['Final Quote', "First Payment (Direct)",
                     "First Payment (Financial)", "Intent Due",
                     "Liability Assumption Date",
                     "Market Conditions Date", "Prelim Quotes Due",
                     "Premium Transfer Due"
        ]:
            try:
                value = dateparser.parse(value).date().isoformat()
            except:
                traceback.print_exc()
                value = None

        if field == "Deal Type":
            if value == "Plan-Termination":
                value = "Plan Termination"

        return value

    def salesforce_dataset_add_account(self, request, spec, datasetpk,
                               name,
                               nature, extra={}):
        # Plan sponsor account....

        action = request.GET.get('action', None)
        action_oppid = request.GET.get('opportunityid', None)
        action_oppid = None if str(action_oppid).lower() == "none" else action_oppid

        usecase = spec['usecase']
        namespace = spec['namespace']
        r = resolve(request.path)
        cred, client = self.get_client(request, spec)

        posturl = reverse(r.namespace + ":salesforce_dataset_verify",
                          kwargs={
                              'datasetpk': datasetpk
                          }) + f"?action={action}&opportunityid={action_oppid}"
        postredirect = HttpResponseRedirect(posturl)

        assert nature in ['Plan Sponsor', 'Intermediary']

        try:
            params = {
                "Name": name, # plan sponsor name
                "Type": nature
            }
            params.update(extra)
            result = client.add_account(params)
            messages.success(request,f"Added {nature}. Please try again")
        except:
            logger.exception(f"Unable to {nature}")
            messages.error(request,f"Unable to add plan sponsor")

        return postredirect

    def salesforce_dataset_action(self, request, spec, datasetpk):
        """
        Post to salesforce
        """

        action = request.GET.get('action', None)
        action_oppid = request.GET.get('opportunityid', None)
        action_oppid = None if str(action_oppid).lower() == "none" else action_oppid

        usecase = spec['usecase']
        namespace = spec['namespace']
        r = resolve(request.path)

        cred, client = self.get_client(request, spec)

        validateurl = reverse(r.namespace + ":dataset_validate",
                              kwargs={
                                  'pk': datasetpk
                              })
        redirect = HttpResponseRedirect(validateurl)
        posturl = reverse(r.namespace + ":salesforce_dataset_verify",
                              kwargs={
                                  'datasetpk': datasetpk
                              })
        postredirect = HttpResponseRedirect(posturl)

        # What should be redirect to...
        if action == "create":
            sfindexredirect = HttpResponseRedirect(reverse(r.namespace + ":salesforce_index"))
        else:
            sfindexredirect = HttpResponseRedirect(reverse(r.namespace + ":salesforce_detail",
                                                           kwargs={
                                                               "oppid": action_oppid
                                                           }))

        # => Get models
        LLMDatasetModel = self.get_model(spec, 'llmdataset')

        # Get the dataset
        try:
            dataset = LLMDatasetModel.objects.get(pk=datasetpk)
        except LLMDatasetModel.DoesNotExist:
            messages.error(request, 'Invalid dataset')
            return HttpResponseRedirect(reverse(r.namespace + ":dataset_index"))

        # => First get all the model parameters
        try:
            modelvars = dataset.values.get('modelvar', [])
            if len(modelvars) == 0:
                messages.error(request, "Not posted. Please save first")
                return redirect

            # Convery into a dictionary
            modelvars = { v['name'] : v['value'] for v in modelvars}

        except:
            logger.exception("Unable to post to salesforce")
            messages.error(request, 'Internal error. Unable to post to salesforce')
            return redirect

        mapping = self.get_salesforce_fieldmapping()
        comments_field = "Plan_Provision_Comments2__c"
        stage_name = request.GET.get("stagename", "Long Term")
        comment = request.GET.get("comments", "")
        postcontent = {
            "StageName": stage_name,
            "Name": "DummyName",
            "CurrencyIsoCode": "USD",
            comments_field: comment
        }

        error_fields = []
        msg = ""
        for k, v in modelvars.items():
            mapping_detail = mapping.get(k,{})
            field_name = mapping_detail.get("Salesforce Field Name", "")
            field_api_name = mapping_detail.get("Salesforce Field API", "")
            is_mapped = field_name != ""
            notes = mapping_detail.get("Notes", "")

            # This goes into the plan sponsor details...
            if k == "Company Description (Internal)":
                continue

            # Override the names...
            if k == "Consultant":
                field_api_name = "Intermediary__c"
            elif k == "Plan Sponsor":
                field_api_name = "AccountId"

            # Should I post it...
            if not is_mapped and v in [None, '']:
                msg += f"{k}: No salesforce field and value is empty\n"
                continue

            if k in ['Total Participants']:
                msg += f"{k}: Skipping\n"
                continue

            # Handle plan sponsor
            account_mapping = {
                "Plan Sponsor": "accountid",
                "Consultant": "consultantid",
            }
            if k in account_mapping:
                accountid = request.GET.get(account_mapping[k], None)
                if accountid is None:
                    if k == "Plan Sponsor":
                        logger.error(f"Invalid {k}")
                        messages.error(request, 'Plan Sponsor not specified')
                        return redirect
                    else:
                        continue
                elif accountid != "Create":
                    # Switch to the account id
                    postcontent[field_api_name] = accountid
                    msg += f"{k}: Added the Id instead of value ({accountid}\n"
                    continue
                else:
                    # Create account
                    notes = ""
                    nature = "Intermediary" if k == "Consultant" else k
                    if nature == "Plan Sponsor":
                        notes = modelvars.get("Company Description (Internal)", "")
                    return self.salesforce_dataset_add_account(request,
                                                       spec,
                                                       datasetpk,
                                                       name=v,
                                                       nature=nature,
                                                       extra={
                                                           "Region__c": "United States",
                                                           "Account_Short_Name__c": v,
                                                           "Notes__c": notes
                                                       })


            # Lookup fields...
            if ((("lookup" in notes.lower()) or (not is_mapped) or ("." in field_api_name)) and
                (k not in ['Plan Sponsor', 'Consultant'])):
                # Lookup field or no field exists..
                #postcontent[comments_field] += f"\n{k}: {v}\n<br>"
                #msg += f"{k}: Added to {comments_field}\n"
                continue

            v = self.field_specific_cleanup(k, v)
            if v in ["", None, "None"]:
                error_fields.append(k)
                msg += f"{k}: Skipped. Empty value\n"
                continue

            # Final
            k = mapping_detail['Salesforce Field API']
            postcontent[k] = v
            msg += f"{k}: Added\n"

            if k == "Submission_Due_Date__c":
                k1 = "CloseDate"
                postcontent[k1] = v
                msg += f"{k1}: Added. Same value as {k}\n"

        # postcontent[comments_field] = postcontent[comments_field]

        # print(json.dumps(postcontent, indent=4))

        # => Now we have the post content ready...
        try:
            if action == "create":
                result = client.add_opportunity(postcontent, request=request)
            else:
                result = client.update_opportunity(action_oppid,
                                                   data=postcontent,
                                                   request=request)

            logger.debug("Posted to server",
                         extra={
                             'data': json.dumps(result, indent=4) + "\nLog:\n" + msg
                         })
        except:
            logger.exception("Failed to add opportunity",
                             extra={
                                 'data': "Log: " + msg
                             })
            messages.error(request, "Error while posting to salesforce. See log")
            return redirect

        messages.success(request, "Added an opportunity successfully")
        return sfindexredirect

if __name__ == "__main__":

    salesforce = SalesforceClient(cred="brookfield-salesforce")

    results = salesforce.get_opportunities()
    print(json.dumps(results, indent=4))

    #results = salesforce.describe_opportunity()
    #print(json.dumps(results, indent=4))

