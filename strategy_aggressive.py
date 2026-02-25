#Implementación de estrategia agresiva.
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

class StrategyAggressive(Strategy, StrategyAbstract):
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
        cruisers = shipyard_manager.getCruisers()

        #PASO 1: Aumenta la cantidad de cruceros y cazadores ligeros:
        if shipyard is not None and shipyard['level'] >= 1:
            if light_fighters is not None and light_fighters['cantidad'] < 50:
                target = light_fighters
                quantity = 2
                self._build_ship(session, resources_manager, target, cantidad=quantity)
                end_date = shipyard_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False
            if heavy_fighters is not None and heavy_fighters['cantidad'] < 50:
                target = heavy_fighters
                quantity = 1
                self._build_ship(session, resources_manager, target, cantidad=quantity)
                end_date = shipyard_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False
            if cruisers is not None and cruisers['cantidad'] < 10:
                target = cruisers
                quantity = 1
                self._build_ship(session, resources_manager, target, cantidad=quantity)
                end_date = shipyard_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False
        
        if researches is not None:
            if weapons_technology is not None and  weapons_technology['level'] < 7:
                target = weapons_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if shielding_technology is not None and shielding_technology['level'] < 7:
                target = shielding_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if armour_technology is not None and armour_technology['level'] < 7:
                target = armour_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if energy_technology is not None and energy_technology['level'] < 8:
                target = energy_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if laser_technology is not None and laser_technology['level'] < 10:
                target = laser_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if ion_technology is not None and ion_technology['level'] < 5:
                target = ion_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            #Tecnología de plasma desbloqueada (Requiere: Lab 5, Energía 8, Láser 10, Ion 5)
            if plasma_technology is not None and plasma_technology['level'] < 5:
                target = plasma_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False

        print(">>>> Estrategia agresiva completada <<<<")
        return True

    def decide_and_attack(self, session, fleet_manager: FleetManager):
        minimum_cruisers_to_attack = 10
        probability_of_attack = 10 #%

        fleet_manager.checkAvailableShips(session)
        available_ships = fleet_manager.getShipsAvailable()
        print("\n\nNaves disponibles para enviar:")
        for ship in available_ships:
            print(ship)
        print("")
        attack_dice = int(random.random() * 100)
        if attack_dice > 100 - probability_of_attack:
            if (fleet_manager.getCruisersQuantity() >= minimum_cruisers_to_attack):
                fleet_manager.sendRandomFleetToAttack(session)
            else:
                print("Intenté atacar, pero sólo tengo " + str(fleet_manager.getCruisersQuantity()) + " cruceros, y necesito por lo menos " + str(minimum_cruisers_to_attack) + " para atacar")
                print("")