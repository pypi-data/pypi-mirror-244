"""
Generate synthetic data
"""
import json
import random

# Generating a more realistic dataset with varied company names and details

# List of sample company names
companies = [
    "AlphaTech Solutions", "Beta Enterprises",
    "Gamma Global", "Delta Dynamics", "Epsilon Electronics",
    "Zeta Industries", "Eta Energy", "Theta Transport",
    "Iota Informatics",
    "Kappa Consulting", "Lambda Labs", "Mu Manufacturing",
    "Nu Networks", "Xi Xerography", "Omicron Optics", "Pi Productions",
    "Rho Robotics", "Sigma Systems", "Tau Technologies",
    "Upsilon Utilities"
]

opportunities = []
for i, name in enumerate(companies, start=1):
    month = random.choice(range(1, 12))
    day = random.choice(range(1, 28))
    opportunity = {
        "Id": str(i),
        "Opportunity Name": f"Service Contract - {name}",
        "Account Name": name,
        "CreatedDate": f"2024-{str(month).zfill(2)}-{str(day).zfill(2)}",
        "Stage": "Negotiation" if i % 2 == 0 else "Closed Won",
        "Amount": 100000 + i * 10000,
        "Type": "New Business" if i <= 10 else "Renewal",
        "Lead Source": "Referral" if i % 3 == 0 else "Partner",
        "Next Step": "Finalize terms" if i % 4 == 0 else "Execute contract",
        "Probability (%)": 50 + i * 2,
        "Description": f"Providing {name.split()[0]} services, payment terms: {30 + i} days."
    }
    opportunities.append(opportunity)

    
def get_sample_opportunities():
    return {
        "records": opportunities
    }

def get_opportunity_descriptions():
    return { k: k for k in opportunities.keys()}

