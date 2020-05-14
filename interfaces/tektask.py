"""Tek-Task module to manage the sinchronization service"""
import json

import requests

from settings.settings import TEKTASK_BASE_URL, TEKTASK_ORIGIN


class TekTask:
    """
    Tek-Task Class
    """

    @staticmethod
    def search_company(space: str, name: str) -> dict:
        """
        look for a company on Tek-Task
        :return: dict
        """
        query = """
            query{
              CompanyFindOne(filter: {
                space:"%s",
                name:"%s"}){
                space
                owner
                name
                logo
                url
                phoneNumber
                members{
                  user{
                    firstName
                    lastName
                    email
                  }
                }
                deleted
                _id
                updatedAt
                createdAt
                role
              }
            }
            """ % (space, name)

        url = TEKTASK_BASE_URL
        data = requests.post(url, json={'query': query})
        json_data = json.loads(data.text)
        return json_data

    @staticmethod
    def modify_role(space: str, user_id: str, role_id: str) -> {}:
        """
        modify user role on Tek-Task
        :return: None
        """
        query = """
            mutation{
              UserhasroleCreateOne(record: 
                {space:"%s",
                userId:"%s",
                roleId:"%s",
                owner:"%s"}){
                recordId
                record{
                  space
                  owner
                  userId
                }
              }
            }
        """ % (space, user_id, role_id, user_id)

        url = TEKTASK_BASE_URL
        data = requests.post(url, json={'query': query})
        json_data = json.loads(data.text)
        return json_data['data']['UserhasroleCreateOne']

    @staticmethod
    def search_user(email: str) -> {}:
        """
        look for an user on Tek-Task
        :return: None
        """
        query = """
            query{
              userFindOne(filter: {email:"%s"}){
                space
                firstName
                lastName
                avatar
                connected
                email
                phone
                oauth0Provider
                refreshTokenProvider
                roles
                companyRole
                agreeTC
                validated
                activateCode
                employee
                rate
                _id
                updatedAt
                createdAt
                fullName
                company{
                  name
                }
              }
            }
        """ % email

        url = TEKTASK_BASE_URL
        data = requests.post(url, json={'query': query})
        json_data = json.loads(data.text)
        return json_data

    @staticmethod
    # pylint: disable=too-many-arguments
    def create_company(name: str, space: str, url: str = '',
                       owner_id: str = '', logo: str = '',
                       phone_number: str = '') -> {}:
        """
        crate a company on Tek-Task
        :return: None
        """

        query = """
            mutation{
              CompanyCreateOne(record: 
              { name:"%s", 
                space:"%s",
                owner:"%s",
                logo:"%s",
                url:"%s",
                phoneNumber:"%s",
                 }){
                recordId
                ...company_fragment
              }
            }
            fragment company_fragment on CreateOneCompanyPayload{
              record{
                owner
                name
                logo
                url
                phoneNumber
                updatedAt
                createdAt
                role
                _id
              }
            }
        """ % (name, space, owner_id, logo, url, phone_number)

        url = TEKTASK_BASE_URL
        data = requests.post(url, json={'query': query})
        json_data = json.loads(data.text)
        return json_data['data']['CompanyCreateOne']

    @staticmethod
    # pylint: disable=too-many-arguments
    def associate_user_company(first_name: str, last_name: str,
                               email: str, role: str, company_id: str) \
            -> {}:
        """
        
        :param first_name: str
        :param last_name: str
        :param email: str
        :param role: str
        :param company_id: str
        :return: {}
        """
        query = """
            mutation{
              CompanyAddMember(
                firstName: "%s", 
                lastName: "%s",
                email: "%s",
                role:"%s",
                companyId: "%s")
              {
                memberId
              }
            }
        """ % (first_name, last_name, email, role, company_id)

        url = TEKTASK_BASE_URL
        data = requests.post(url, json={'query': query})
        json_data = json.loads(data.text)
        return json_data['data']['CompanyAddMember']

    @staticmethod
    # pylint: disable=too-many-arguments
    def create_user(email: str, role: str, space: str, first_name: str,
                    company: str, company_id: str,
                    last_name: str = '') -> {}:
        """
        create user on Tek-Task
        :return: None
        """
        query = """
            mutation{
              userAddToSpace(
              firstName: "%s", 
              lastName: "%s", 
              email: "%s", 
              companyId: "%s", 
              company: "%s", 
                role: "%s"){
                result {
                  space
                  firstName
                  lastName
                  avatar
                  connected
                  email
                  phone
                  _id
                }
                code
                message
              }
            }
            """ % (first_name, last_name, email, company_id, company, role)

        url = TEKTASK_BASE_URL
        response = requests.post(
            url, json={'query': query},
            headers={'origin-cross': TEKTASK_ORIGIN})
        json_data = json.loads(response.text)

        if json_data['data']['userAddToSpace']:
            TekTask.modify_role(
                space=space,
                user_id=json_data['data']['userAddToSpace']['result']['_id'],
                role_id=role,
            )

        return json_data['data']['userAddToSpace']

    @staticmethod
    # pylint: disable=too-many-arguments
    def create_project(space: str, company_id: str, deal_id: str,
                       name: str, type: str, status: str,
                       fixed_price: float = 0, percent_discount: float = 0,
                       extra: float = 0, description: str = '',
                       ) -> {}:
        """
        crate a project on Tek-Task
        :param deal_id:
        :param space:
        :param company_id:
        :param name:
        :param type:
        :param status:
        :param fixed_price:
        :param percent_discount:
        :param extra:
        :param description:
        :return: str
        """
        query = """
            mutation{
              projectCreateOne(record: 
              { space:"%s", 
                companyId:"%s", 
                hubspotData: {dealId: "%s"},
                name: "%s", 
                type:"%s", 
                status:"%s", 
                fixedPrice:%.2f, 
                porcentDiscount:%.2f, 
                extra:%.2f, 
                description:"%s"})
                {
                recordId
                record {
                  space
                  owner
                  name
                  description
                  startDate
                  endDate
                  type
                  status
                  freeCharge
                  planningAccessAll
                  fixedPrice
                  porcentDiscount
                  extra
                  companyId
                  updatedAt
                  createdAt
                  _id
                } 
              }
            }
        """ % (space, company_id, deal_id, name, type, status, fixed_price,
               percent_discount, extra, description)

        url = TEKTASK_BASE_URL
        data = requests.post(url, json={'query': query})
        json_data = json.loads(data.text)
        return json_data['data']['projectCreateOne']


    @staticmethod
    # pylint: disable=too-many-arguments
    def search_project(space: str, name: str) -> {}:
        """
        crate a project on Tek-Task
        :param space:
        :param name:
        :return: str
        """
        query = """
            query{
              projectFindOne(filter: {
                space:"%s",
                name:"%s"
              }){
                space
                owner
                name
                description
                startDate
                endDate
                type
                status
                freeCharge
                planningAccessAll
                fixedPrice
                porcentDiscount
                extra
                companyId
                deleted
                _id
                updatedAt
                createdAt
                cost
                automaticPrice
              }
            }
        """ % (space, name)

        url = TEKTASK_BASE_URL
        data = requests.post(url, json={'query': query})
        json_data = json.loads(data.text)
        return json_data
