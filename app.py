import json

from flask import Flask, request
from flask_injector import FlaskInjector
from flask_restful import Api
from injector import inject

from settings.settings import CLOSE_WON_STATE, \
    OPPORTUNITY_STATE, PROPOSAL_MADE_CONTACT_STATE, FLASK_ENV, \
    HUBSPOT_BASE_URL, HUBSPOT_APIKEY, TEKTASK_BASE_URL, COMPANY_SPACE, \
    TEKTASK_ORIGIN, CLOSE_LOST_STATE
from tools.hubspot_services import HubSpotServices
from tools.tektask_services import TekTaskServices
from tools.dependencies import configure

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET', ])
# pylint: disable=inconsistent-return-statements
def index():
    """
    Index
    :return:
    """
    if request.method == 'GET':
        return '<div>' \
               '<h1>Hello to Task Synchronizer microservice!</h1>' \
               '<div> ' \
               '<h3>Environment vars</h3><br>' \
               '<h5>{0}</h5>' \
               '<h5>{1}</h5>' \
               '<h5>{2}</h5>' \
               '<h5>{3}</h5>' \
               '<h5>{4}</h5>' \
               '<h5>{5}</h5>' \
               '</div>' \
               '</div>'.format(FLASK_ENV, HUBSPOT_BASE_URL,
                               HUBSPOT_APIKEY, TEKTASK_BASE_URL,
                               TEKTASK_ORIGIN, COMPANY_SPACE)


@app.route('/webhooks', methods=['POST', ])
@inject
# pylint: disable=inconsistent-return-statements
def webhooks(tt_services: TekTaskServices) -> {}:
    """
    Webhooks to receive payload from HubSpot
    :return:
    :param tt_services: TekTaskServices
    :return:
    """
    # pylint: disable=too-many-nested-blocks
    if request.method == 'POST':
        print("""\n
          //------------------------------------------/\n
         //------------WEB-HOOKS-REQUEST!------------>\n
        //------------------------------------------/\n
        """)

        data = json.loads(request.data)
        response = ''
        for obj in data:
            if 'changeFlag' in obj:
                if obj['changeFlag'] == 'NEW':
                    object_type = obj["subscriptionType"].split('.')[0]
                    id_item = obj['objectId']

                    if object_type == 'company':
                        response = tt_services.create_company(
                            id_item=id_item)
                    if object_type == 'deal':
                        response = tt_services.create_project(
                            id_item=id_item)
                    # if object_type == 'contact':
                    #     response = tt_services.create_contact(
                    #         id_item=id_item)
                    continue
            if 'changeSource' in obj:
                if obj['changeSource'] == 'ASSOCIATIONS' or  \
                        obj['changeSource'] == 'CONTACTS':
                    if obj['propertyName'] == 'associatedcompanyid' and \
                            'propertyValue' in obj:

                        property_value = obj['propertyValue']
                        if not property_value:
                            continue

                        object_type = obj["subscriptionType"].split('.')[0]
                        id_item = obj['objectId']

                        if object_type == 'contact':
                            response = tt_services.create_contact(
                                id_item=id_item,
                                associated_to=property_value)
                            # response = \
                            #     tt_services.user_company_association(
                            #     id_item, property_value)

        return response


@app.route('/api/event', methods=['POST', ])
@inject
# pylint: disable=too-many-return statements
def sync_hub_spot(hp_service: HubSpotServices):
    """
    Endpoint to update HubSpot
    :param hp_service:  HubSpotServices
    :return: None
    """
    print("""\n
    \\-------------------------------------------\\\n
     <--------------TEK-TASK-REQUEST!-------------\\\n
      \\---------------------------------------------\\\n
    """)

    PIPE_LINE_ID = 'default'
    data = json.loads(request.data)
    event = request.args['id']
    response = ''

    if event == 'PROJECT_CREATED':
        payload = data['payload'] if data['payload'] else {}
        payload['dealstage'] = OPPORTUNITY_STATE
        payload['pipeline'] = PIPE_LINE_ID
        response = hp_service.create_deal(data=data['payload'])

    if event == 'USER_CREATED':
        response = hp_service.create_user(data=data['payload'])

    if event == 'COMPANY_CREATED':
        response = hp_service.create_company(data=data['payload'])

    if event == 'PROJECT_SCOPE_CREATED':
        payload = data['payload'] if data['payload'] else {}
        payload['dealstage'] = PROPOSAL_MADE_CONTACT_STATE
        response = hp_service.update_deal(data=payload)

    if event == 'PROJECT_SCOPE_ACCEPTED':
        payload = data['payload'] if data['payload'] else {}
        payload['dealstage'] = CLOSE_WON_STATE
        response = hp_service.update_deal(data=payload)

    if event == 'PROJECT_SCOPE_REJECTED':
        payload = data['payload'] if data['payload'] else {}
        payload['dealstage'] = CLOSE_LOST_STATE
        response = hp_service.update_deal(data=payload)

    # TODO waiting for definition
    if event == 'PROJECT_SCOPE_ON_REVIEW':
        response = {"message": "event PROJECT_SCOPE_ON_REVIEW doesn't have "
                           "business definition yet"}

    return response

FlaskInjector(app, modules=[configure])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
