#Implementación de la estrategia a largo plazo
import random
from strategy import Strategy
from strategy_abstract import StrategyAbstract
from resources_manager import ResourcesManager
from buildings_resources_manager import BuildingsResourcesManager
from buildings_facilities_manager import FacilitiesManager
from defenses_manager import DefensesManager
from research_manager import ResearchManager
from shipyard_manager import ShipyardManager
from fleet_manager import FleetManager
from constants import BASE_URL

class StrategyLongTerm(Strategy, StrategyAbstract):
    def decide_and_build(self, session, resources_manager: ResourcesManager, buildings_resources_manager: BuildingsResourcesManager, facilities_manager: FacilitiesManager, research_manager: ResearchManager,defenses_manager: DefensesManager, shipyard_manager: ShipyardManager) -> bool:
        #INFO DE EDIFICIOS
        metal_mine = buildings_resources_manager.getMetalMine()
        crystal_mine = buildings_resources_manager.getCrystalMine()
        deuterium_synthesizer = buildings_resources_manager.getDeuteriumSynthesizer()
        solar_plant = buildings_resources_manager.getSolarPlant()
        fusion_reactor = buildings_resources_manager.getFusionReactor()

        #INFO DE INSTALACIONES
        robot_factory = facilities_manager.getRoboticsFactory()
        research_lab= facilities_manager.getResearchLab()
        shipyard = facilities_manager.getShipyard()
        
        #INFO DE INVESTIGACIONES:
        researches = research_manager.getResearches()
        espionage_technology = research_manager.getEspionageTechnology()
        computer_technology = research_manager.getComputerTechnology()
        weapons_technology = research_manager.getWeaponsTechnology()
        shielding_technology = research_manager.getShieldingTechnology()
        armour_technology = research_manager.getArmourTechnology()
        energy_technology = research_manager.getEnergyTechnology()
        hyperspace_technology = research_manager.getHyperspaceTechnology()
        combustion_drive = research_manager.getCombustionDrive()
        impulse_drive = research_manager.getImpulseDrive()
        hyperspace_drive = research_manager.getHyperspaceDrive()
        laser_technology = research_manager.getLaserTechnology()
        ion_technology = research_manager.getIonTechnology()
        plasma_technology = research_manager.getPlasmaTechnology()
        intergalactic_research_network = research_manager.getIntergalacticResearchNetwork()
        astrophysics = research_manager.getAstrophysic()
        graviton_technology = research_manager.getGravitonTechnology()

        #RECUPERA INFO DEFENSAS:
        rocket_launchers = defenses_manager.getRocketLaunchers()
        light_lasers = defenses_manager.getLightLasers()
        heavy_lasers = defenses_manager.getHeavyLasers()
        small_shield_dome = defenses_manager.getSmallShieldDome()
        gauss_cannons = defenses_manager.getGaussCannons()
        ion_cannons = defenses_manager.getIonCannons()

        #RECUPERA INFO NAVES:
        light_fighters = shipyard_manager.getLightFighters()
        heavy_fighters = shipyard_manager.getHeavyFighters()

        print(">>>> Ejecutando estrategia a largo plazo <<<<")
        #Símplemente a largo plazo prioriza mina de metal 1 nivel por encima de la de cristal
        if (metal_mine is not None and metal_mine['level']) < (crystal_mine is not None and crystal_mine['level'] + 1):
            target = metal_mine
        else:
            target = crystal_mine
        self._build_target(target, buildings_resources_manager, resources_manager, session)
        return True

    def decide_and_attack(self, session, fleet_manager: FleetManager):
        pass
