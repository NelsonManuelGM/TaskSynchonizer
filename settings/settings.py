"""Setting module for the application"""
import os

FLASK_ENV = os.environ.get('FLASK_ENV')

# HubSpot environment vars
HUBSPOT_BASE_URL = os.environ.get('HUBSPOT_BASE_URL',
                                  default="https://api.hubapi.com/")
HUBSPOT_APIKEY = os.environ.get('HUBSPOT_APIKEY')

# TekTask environment vars
TEKTASK_BASE_URL = os.environ.get(
    'TEKTASK_BASE_URL')
TEKTASK_ORIGIN = os.environ.get(
    'TEKTASK_ORIGIN')
COMPANY_SPACE = os.environ.get('COMPANY_SPACE')

if FLASK_ENV == 'development':
    # develop stages ids
    CONTACT_MADE_STATE = "appointmentscheduled"
    OPPORTUNITY_STATE = "qualifiedtobuy"
    PROPOSAL_MADE_CONTACT_STATE = "presentationscheduled"
    RENEWAL_STATE = "decisionmakerboughtin"
    CLOSE_WON_STATE = "closedwon"
    CLOSE_LOST_STATE = "closedlost"
else:
    # production stages ids
    CONTACT_MADE_STATE = "presentationscheduled"
    OPPORTUNITY_STATE = "decisionmakerboughtin"
    PROPOSAL_MADE_CONTACT_STATE = "contractsent"
    RENEWAL_STATE = "980f45f1-a73c-48de-8be5-86b4a19eb3e7"
    CLOSE_WON_STATE = "60eeaceb-1ebd-4cdb-9a48-2326347bb738"
    CLOSE_LOST_STATE = "66fb8f98-f3a3-4f37-b004-420f5c377781"


ROLE_DIC = {"ADMIN_ALMIGHTY": "5c9051368435581d89eb4412",
            "ADMIN_SPACE": "5c9051a08435581d89eb4413",
            "CLIENT": "5c92963e20ddbc24adaeaf53",
            "CLIENT_OWNER": "5c92964420ddbc24adaeaf54",
            "CLIENT_MANAGER": "5c92964c20ddbc24adaeaf55",
            "CLIENT_EMPLOYEED": "5c92965220ddbc24adaeaf56",
            "EMPLOYEED": "5c92965820ddbc24adaeaf57",
            "EMPLOYEED_CEO": "5c92965f20ddbc24adaeaf58",
            "EMPLOYEED_CTO": "5c92966620ddbc24adaeaf59",
            "EMPLOYEED_TLEADER": "5c92966c20ddbc24adaeaf5a",
            "EMPLOYEED_DESIGNER": "5c92967320ddbc24adaeaf5b",
            "EMPLOYEED_DEVELOPER": "5c92967a20ddbc24adaeaf5c"}
