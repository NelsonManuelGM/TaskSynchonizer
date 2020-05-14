""" services to consume TekTask interface"""

from injector import inject

from interfaces.hubspot import HubSpot
from interfaces.tektask import TekTask
from settings.settings import COMPANY_SPACE, ROLE_DIC

STATUS = 'in specification'
PROJECT_TYPE = "New Project"


class TekTaskServices:
    """
    Class for consume the TekTask interface and separate the logic process
    """

    @inject
    def __init__(self, tt: TekTask, hp: HubSpot):
        self.tt = tt
        self.hp = hp

    def create_contact(self, id_item: int, associated_to: str) -> {}:
        """
        Create contact using the TekTask interface
        :param id_item: int
        :return: {}
        """
        response = {'message': 'the user already exist!'}

        try:
            user_data = self.hp.get_user(id_user=id_item)

            if 'status' in user_data:
                print(user_data['message'])
                return user_data['message']
            first_name = user_data['properties']['firstname']['value']
            last_name = user_data['properties']['lastname']['value']
            email = user_data['properties']['email']['value']
            hp_company_id = associated_to

            company = self.hp.get_company(int(hp_company_id))
            company_name = company['properties']['name']['value']

            company_tt = self.tt.search_company(space=COMPANY_SPACE,
                                                name=company_name)
            id_company_tt = company_tt['data']['CompanyFindOne']['_id']

            user_tt = self.tt.search_user(email=email)
            if not user_tt['data']['userFindOne']:
                response = self.tt.create_user(email=email,
                                               role=ROLE_DIC['CLIENT'],
                                               space=COMPANY_SPACE,
                                               first_name=first_name,
                                               last_name=last_name,
                                               company_id=id_company_tt,
                                               company=company_name
                                               )

                print("User created: \n", response)
                return {"message": "User created", "data": response}
            print(response['message'])
            return user_tt
        except Exception as ex:
            raise ex

    def user_company_association(self, id_item: int, property_value: str) \
            -> {}:
        """
        Create contact using the TekTask interface
        :param id_item: int
        :param property_value: str
        :return: {}
        """
        user_data = self.hp.get_user(id_user=id_item)

        if 'status' in user_data:
            print(user_data['message'])
            return user_data['message']

        email = user_data['properties']['email']['value']
        first_name = user_data['properties']['firstname']['value']
        last_name = user_data['properties']['lastname']['value']

        associated_company_id = int(property_value)
        company_data = self.hp.get_company(associated_company_id)
        company_name = company_data['properties']['name']['value']

        company_tt = self.tt.search_company(name=company_name,
                                            space=COMPANY_SPACE)
        if not company_tt['data']['CompanyFindOne']:
            return {"message": "We can't fined the company in the process "
                               "to associate user"}

        id_company_tt = company_tt['data']['CompanyFindOne']['_id']

        response = self.tt.associate_user_company(email=email,
                                                  first_name=first_name,
                                                  last_name=last_name,
                                                  role=ROLE_DIC['CLIENT'],
                                                  company_id=id_company_tt)

        return {"message": response}

    def create_company(self, id_item: int) -> {}:
        """
        Create company using the TekTask interface
        :param id_item: int
        :return: {}
        """
        # search company on HubSpot
        company_data = self.hp.get_company(id_company=id_item)
        response = {'message': 'the company already exist!'}

        if 'status' in company_data:
            print(company_data['message'])
            return company_data['message']
        name = company_data['properties']['name']['value']

        # shake to avoid duplicates on TekTask
        tt_company = self.tt.search_company(name=name, space=COMPANY_SPACE)

        if not tt_company['data']['CompanyFindOne']:
            response = self.tt.create_company(name=name,
                                              space=COMPANY_SPACE)
            print("Company Created: \n", response)
            return response

        print(response['message'])
        return tt_company

    def create_project(self, id_item: int) -> {}:
        """
        Create project using the TekTask interface
        :param id_item: int
        :return: {}
        """
        # search deal on HubSpot
        deal_data = self.hp.get_deal(id_deal=id_item)

        deal_name = deal_data['properties']['dealname']['value']
        hp_company_id = \
            deal_data['associations']['associatedCompanyIds'][0]

        # search company on HubSpot
        company_data = self.hp.get_company(id_company=hp_company_id)
        company_name = company_data['properties']['name']['value']
        company_domain = company_data['properties']['domain']['value']

        # shake to avoid duplicates on TekTask
        tt_company = self.tt.search_company(name=company_name,
                                            space=COMPANY_SPACE)
        if 'status' in tt_company:
            print(tt_company['message'])
            return tt_company['message']
        if not tt_company['data']['CompanyFindOne']:
            tt_company = self.tt.create_company(name=company_name,
                                                space=COMPANY_SPACE,
                                                url=company_domain)

        company_id = tt_company['data']['CompanyFindOne']['_id']

        tt_project = self.tt.search_project(name=deal_name,
                                            space=COMPANY_SPACE)

        if not tt_project['data']['projectFindOne']:
            response = self.tt.create_project(space=COMPANY_SPACE,
                                              company_id=company_id,
                                              name=deal_name,
                                              status=STATUS,
                                              type=PROJECT_TYPE,
                                              deal_id=str(id_item))

            print("Deal Created! \n", response)
        print("Deal Already Exist! \n")
        return tt_project
