#Clase abstracta que dicta las diferentes funciones que deben implementar cada estrategia.
from abc import ABC, abstractmethod
from resources_manager import ResourcesManager
from buildings_resources_manager import BuildingsResourcesManager
from buildings_facilities_manager import FacilitiesManager
from research_manager import ResearchManager
from defenses_manager import DefensesManager
from shipyard_manager import ShipyardManager
from fleet_manager import FleetManager

class StrategyAbstract(ABC):
    @abstractmethod
    def decide_and_build(self, session, resources_manager: ResourcesManager, buildings_resources_manager: BuildingsResourcesManager, facilities_manager: FacilitiesManager, research_manager: ResearchManager, defenses_manager: DefensesManager, shipyard_manager: ShipyardManager) -> None:
        pass

    @abstractmethod
    def decide_and_attack(self, session, fleet_manager: FleetManager):
        pass