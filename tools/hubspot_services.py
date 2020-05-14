""" services module to consume HubSpot interface"""

from injector import inject

from interfaces.hubspot import HubSpot
from tools.exeptions import InvalidUsage
from tools.tools import create_hash


class HubSpotServices:
    """
    Class for consume the TekTask interface and separate the logic process
    """

    @inject
    def __init__(self, hp: HubSpot):
        self.hp = hp

    def create_company(self, data: {}) -> {}:
        """
        Service to create a company on HubSpot
        :param data: {}
        :return: {}
        """

        company_name = data['name']
        company_domain = data['domain'] if 'domain' in data else ''

        company_domain_hash = create_hash(company_domain)
        new_company_domain = company_name.replace(" ", "-").lower()\
                             + company_domain_hash + '.com'

        domain = company_domain if company_domain \
            else new_company_domain

        try:
            company = self.hp.search_company(domain=domain)

            if company['results']:
                return {
                    "None": f"The company with domain {domain} "
                    f"already exist"}

            new_company = self.hp.create_company(
                name=data['name'],
                description=data['description'],
                domain=domain)
        except KeyError:
            return {"message": "For create a company the name and "
                               "description are necessary"}

        return new_company

    def create_user(self, data: {}) -> {}:
        """
        Service to create a user on HubSpot
        :param data: {}
        :return: {}
        """

        try:
            user = self.hp.search_user(data['email'])

            if user['total']:
                return {
                    "message": f"The user with email {data['email']} "
                    f"already exist"}

            new_user = self.hp.create_user(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                phone=data['phone'] if 'phone' in data else None,
                company=data['company'] if 'company' in data else None
            )
        except Exception:
            return InvalidUsage('To create an user the fields first_name, '
                                'last_name and email are necessary!') \
                .to_dict()
        return new_user

    def update_user(self, data: {}) -> {}:
        """
        Service to update a user on HubSpot
        :param data: {}
        :return: {}
        """

        try:
            user_response = self.hp.get_user(data['user_id'])

            if 'status' in user_response \
                    and user_response['status'] == 'error':
                return {
                    "message": user_response['errors'][0]['message']}
            try:
                response = self.hp.update_user(
                    user_id=data['user_id'],
                    first_name=data[
                        'first_name'] if 'first_name' in data else None,
                    last_name=data[
                        'last_name'] if 'last_name' in data else None,
                    email=data['email'] if 'email' in data else None,
                    phone=data['phone'] if 'phone' in data else None,
                    company=data['company'] if 'company' in data else None,
                    address=data['address'] if 'address' in data else None,
                    city=data['city'] if 'city' in data else None,
                    state=data['state'] if 'state' in data else None,
                    website=data['website'] if 'website' in data else None,
                    zip_code=data[
                        'zip_code'] if 'zip_code' in data else None
                )
                return {"message": f'User {data["user_id"]} updated',
                        "status_code": response}
            except Exception as e:
                return e

        except KeyError:
            return InvalidUsage('To update an user the fields email is '
                                'mandatory!').to_dict()

    def create_deal(self, data: {}) -> {}:
        """
        Service to create a deal on HubSpot
        :param data: {}
        :return:
        """
        company_id = ''
        associated_company = None
        user_list = []

        if 'associated_company' in data and \
                list(data['associated_company'].items()).__len__() > 0:
            associated_company = data['associated_company']

            description = associated_company['description']
            company_domain = associated_company[
                'domain'] if 'domain' in associated_company else ''
            company_name = associated_company['name']

            company_domain_hash = create_hash(company_domain)
            new_company_domain = company_name.replace(" ", "-").lower() \
                                 + company_domain_hash + '.com'

            domain = company_domain if company_domain \
                else new_company_domain

            company_response = self.hp.search_company(
                domain=domain)['results']
            if company_response:
                company_id = company_response[0]['companyId']
            else:
                try:
                    company_data = self.hp.create_company(
                        name=company_name,
                        description=description,
                        domain=domain)

                    if 'status' in company_data:
                        return {"message": company_data[
                            'validationResults'][0]['message']}
                    company_id = company_data['companyId']
                except KeyError as ex:
                    raise ex
        else:
            return {"message": "to make a deal most be a company "
                               "associated"}

        if 'associated_vids' in data:
            if data['associated_vids'].__len__() > 0:
                associated_vids = data['associated_vids']
                for item in associated_vids:
                    user = self.hp.search_user(item['email'])
                    if user['contacts']:
                        user_id = user['contacts'][0]['vid']
                        user_list.append(user_id)
                    else:
                        try:
                            user_id = self.hp.create_user(
                                first_name=item['first_name'],
                                last_name=item['last_name'],
                                email=item['email'])['vid']
                            user_list.append(user_id)
                        except Exception as ex:
                            raise ex

        try:
            deal = self.hp.create_deal(
                associated_company_ids=company_id,
                associated_vids=user_list,
                dealname=data["project"],
                dealstage=data[
                    "dealstage"] if "dealstage" in data else None
            )

        except Exception as ex:
            raise ex

        return {"message": "Deal created!", "deal_id": deal['dealId']}

    def update_deal(self, data: {}) -> {}:
        """

        Service to update a deal on HubSpot
        :param data: {}
        :return:
        """

        deal_id = data['id_deal']

        deal_response = self.hp.get_deal(id_deal=deal_id)
        if 'status' in deal_response \
                and deal_response['status'] == 'error':
            return deal_response['message']
        else:
            try:
                deal = self.hp.update_deal(
                    deal_id=deal_id,
                    dealname=data["dealname"] if "dealname" in data
                    else None,
                    dealstage=data["dealstage"] if "dealstage" in data
                    else None,
                    amount=data["budget"] if "budget" in data else None,
                    pipeline=data[
                        "pipeline"] if "pipeline" in data else None
                )
            except Exception as e:
                return e
        return deal
