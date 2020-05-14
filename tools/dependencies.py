""" dependency inversion module"""

from injector import singleton
from interfaces.hubspot import HubSpot
from interfaces.tektask import TekTask
from tools.hubspot_services import HubSpotServices
from tools.tektask_services import TekTaskServices


def configure(binder) -> None:
    """
    function to configure the dependency inversion
    :param binder:
    :return: none
    """
    binder.bind(HubSpot, to=HubSpot, scope=singleton)
    binder.bind(TekTask, to=TekTask, scope=singleton)
    binder.bind(TekTaskServices, to=TekTaskServices, scope=singleton)
    binder.bind(HubSpotServices, to=HubSpotServices, scope=singleton)
