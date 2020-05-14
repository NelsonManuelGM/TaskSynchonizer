"""HubSpot module to manage the sinchronization service"""
import json

import requests

from settings.settings import HUBSPOT_BASE_URL, HUBSPOT_APIKEY

DEAL_URL = 'deals/v1/deal'
COMPANY_URL = 'companies/v2/companies'
COMPANY_DOMAIN = 'companies/v2/domains'
CONTACT_URL = 'contacts/v1/contact'
QUERY_STRING = {'hapikey': HUBSPOT_APIKEY}
HEADERS = {'Content-Type': 'application/json'}
CONTACTS_SEARCH = 'contacts/v1/search/query?q='


class HubSpot:
    """
    HubSpot Class
    """

    # pylint: disable=too-many-arguments
    @staticmethod
    def create_company(name: str, description: str, domain: str) -> {}:
        """
        Create a company on HubSpot
        :param domain: str
        :param name: str
        :param description: str
        """
        url = HUBSPOT_BASE_URL + COMPANY_URL

        payload = json.dumps(
            {
                "properties": [
                    {
                        "name": "name",
                        "value": name
                    },
                    {
                        "name": "description",
                        "value": description
                    },
                    {
                        "name": "domain",
                        "value": domain
                    }
                ]
            }
        )
        response = requests.request("POST", url, data=payload,
                                    headers=HEADERS,
                                    params=QUERY_STRING)
        json_response = json.loads(response.text)

        return json_response

    @staticmethod
    def search_company(domain: str) -> {}:
        """
        Search for a company by domain
        :param domain:
        :return:
        """

        _domain = ''

        if domain.startswith('http'):
            _domain = domain.split('/')[2]
        else:
            _domain = domain.split('/')[0]

        url = HUBSPOT_BASE_URL + COMPANY_DOMAIN + f'/{_domain}/companies'

        payload = json.dumps(
            {
                "limit": 2,
                "requestOptions": {
                    "properties": [
                        "domain",
                        "createdate",
                        "name"
                    ]
                },
                "offset": {
                    "isPrimary": True,
                    "companyId": 0
                }
            }
        )
        response = requests.request("POST", url, data=payload,
                                    headers=HEADERS,
                                    params=QUERY_STRING)

        json_response = json.loads(response.text)

        return json_response

    @staticmethod
    def get_company(id_company: int) -> {}:
        """
        Return a company by ID
        :param id_company: int
        :return: {}
        """
        url = HUBSPOT_BASE_URL + COMPANY_URL + f"/{id_company}"

        response = requests.get(url=url, params=QUERY_STRING,
                                headers=HEADERS)

        data = json.loads(response.text)

        return data

    @staticmethod
    def create_user(first_name: str, last_name: str, email: str,
                    phone: str = None, company: str = None) -> int:
        """
        Create an user on HubSpot
        :param first_name:
        :param last_name:
        :param email: str
        :param phone: str
        :param company: str
        :return: user id
        """

        url = HUBSPOT_BASE_URL + CONTACT_URL
        data = json.dumps({
            "properties": [
                {
                    "property": "email",
                    "value": email
                },
                {
                    "property": "firstname",
                    "value": first_name
                },
                {
                    "property": "lastname",
                    "value": last_name
                },
                {
                    "property": "company",
                    "value": company
                },
                {
                    "property": "phone",
                    "value": phone
                },
            ]
        })

        response = requests.post(url, data=data, headers=HEADERS,
                                 params=QUERY_STRING)
        json_response = json.loads(response.text)

        return json_response

    @staticmethod
    def search_user(email: str) -> {}:
        """
        search user contact by email
        :param email:
        :return:
        """
        url = HUBSPOT_BASE_URL + CONTACTS_SEARCH + f'{email}'

        response = requests.get(url, headers=HEADERS, params=QUERY_STRING)

        json_response = json.loads(response.text)

        return json_response

    @staticmethod
    def get_user(id_user: int) -> {}:
        """
        Return an user by ID
        :param id_user: int
        :return: {}
        """

        url = HUBSPOT_BASE_URL + CONTACT_URL + f"/vid/{id_user}/profile"

        response = requests.get(url=url, params=QUERY_STRING,
                                headers=HEADERS)

        data = json.loads(response.text)

        return data

    @staticmethod
    # pylint: disable=too-many-locals
    def update_user(user_id: int, first_name: str, last_name: str,
                    email: str,
                    phone: str = None, company: str = None,
                    address: str = None,
                    city: str = None, state: str = None,
                    website: str = None,
                    zip_code: str = None) -> int:
        """
        Create an user on HubSpot
        :param user_id: int
        :param first_name: str
        :param last_name: str
        :param zip_code: str
        :param email: str
        :param phone: str
        :param company: str
        :param address: str
        :param city: str
        :param state: str
        :param website: str
        :return: user id
        """
        url = HUBSPOT_BASE_URL + CONTACT_URL + f"/vid/{user_id}/profile"

        properties = [
            {
                "property": "email",
                "value": email
            },
            {
                "property": "firstname",
                "value": first_name
            },
            {
                "property": "lastname",
                "value": last_name
            },
            {
                "property": "website",
                "value": website
            },
            {
                "property": "company",
                "value": company
            },
            {
                "property": "phone",
                "value": phone
            },
            {
                "property": "address",
                "value": address
            },
            {
                "property": "city",
                "value": city
            },
            {
                "property": "state",
                "value": state
            },
            {
                "property": "zip",
                "value": zip_code
            }
        ]

        for index, item in enumerate(properties):
            if not item['value']:
                properties.__delitem__(index)
                continue

        data = json.dumps({
            "properties": properties
        })

        requests_response = requests.post(url, data=data, headers=HEADERS,
                                          params=QUERY_STRING)

        response = ''
        if requests_response.status_code == 204:
            response = requests_response.status_code
            return response
        if requests_response.status_code == 400:
            response = json.loads(requests_response.text)['message']

        return response

    @staticmethod
    def create_deal(associated_company_ids: [], associated_vids: [],
                    dealname: str, dealstage: str, amount: str = None,
                    pipeline: str = None, dealtype: str = None,
                    closedate: int = None) -> {}:
        """
        Crate a deal on HubSpot

        :param associated_company_ids: str
        :param associated_vids: str
        :param dealname: str
        :param dealstage: str
        :param amount: str
        :param pipeline: str
        :param dealtype: str
        :param closedate: str
        :return: deal id
        """

        url = HUBSPOT_BASE_URL + DEAL_URL

        data = json.dumps({
            "associations": {
                "associatedCompanyIds": associated_company_ids,
                "associatedVids": associated_vids
            },
            "properties": [
                {
                    "value": dealname,
                    "name": "dealname"
                },
                {
                    "value": dealstage,
                    "name": "dealstage"
                },
                {
                    "value": pipeline,
                    "name": "pipeline"
                },
                {
                    "value": closedate,
                    "name": "closedate"
                },
                {
                    "value": amount,
                    "name": "amount"
                },
                {
                    "value": amount,
                    "name": "amount"
                },
                {
                    "value": dealtype,
                    "name": "dealtype"
                }
            ]
        })

        response = requests.post(url, headers=HEADERS, data=data,
                                 params=QUERY_STRING)

        response_json = json.loads(response.text)

        return response_json

    @staticmethod
    def update_deal(deal_id: int, dealname: str = None,
                    dealstage: str = None, pipeline: str = None,
                    amount: str = None) -> {}:
        """
        Create user on HubSpot
        :param deal_id:
        :param dealname:
        :param dealstage:
        :param pipeline:
        :param amount:
        :return: deal_id
        """

        if not any([dealname, dealstage, pipeline, amount]):
            return {"message": "you need to enter at least one element "}

        url = HUBSPOT_BASE_URL + DEAL_URL + f'/{deal_id}'

        properties = [
            {
                "value": dealname,
                "name": "dealname"
            },
            {
                "value": dealstage,
                "name": "dealstage"
            },
            {
                "value": pipeline,
                "name": "pipeline"
            },
            {
                "value": amount,
                "name": "amount"
            }
        ]

        for index, item in enumerate(properties):
            if not item['value']:
                properties.__delitem__(index)
                continue

        data = json.dumps({
            "properties": properties
        })

        response = requests.put(url, headers=HEADERS, data=data,
                                params=QUERY_STRING)

        response_json = json.loads(response.text)

        return response_json

    @staticmethod
    def get_deal(id_deal: int) -> {}:
        """
        Return a Deal by ID
        :param id_deal: int
        :return: {}
        """

        url = HUBSPOT_BASE_URL + DEAL_URL + f"/{id_deal}"

        headers = {
            'Content-Type': "application/json"
        }
        response = requests.get(url=url, params=QUERY_STRING,
                                headers=headers)

        data = json.loads(response.text)

        return data
