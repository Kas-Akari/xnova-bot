#Clase abstracta que dicta las diferentes funciones que deben implementar cada estrategia.
from abc import ABC, abstractmethod
from managers.resources_manager import ResourcesManager
from managers.buildings_resources_manager import BuildingsResourcesManager
from managers.buildings_facilities_manager import FacilitiesManager
from managers.research_manager import ResearchManager
from managers.defenses_manager import DefensesManager
from managers.shipyard_manager import ShipyardManager
from managers.fleet_manager import FleetManager

class StrategyAbstract(ABC):
    @abstractmethod
    def decide_and_build(self, session, resources_manager: ResourcesManager, buildings_resources_manager: BuildingsResourcesManager, facilities_manager: FacilitiesManager, research_manager: ResearchManager, defenses_manager: DefensesManager, shipyard_manager: ShipyardManager) -> bool:
        pass

    @abstractmethod
    def decide_and_attack(self, session, fleet_manager: FleetManager) -> None:
        pass