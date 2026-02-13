#Implementación de estrategia simple
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

class StrategySimple(Strategy, StrategyAbstract):
    def decide_and_build(self, session, resources_manager: ResourcesManager, buildings_resources_manager: BuildingsResourcesManager, facilities_manager: FacilitiesManager, research_manager: ResearchManager,defenses_manager: DefensesManager, shipyard_manager: ShipyardManager) -> None:
        overview_url = BASE_URL + 'game.php?page=overview'
        response = session.post(overview_url, data="")
        resources_manager.fetchResources(session)
        buildings_resources_manager.checkResourcesBuildings(session)
        facilities_manager.checkFacilities(session)
        resources_buildings = buildings_resources_manager.getResourcesBuildings() #Básicamente para mostrar los edificios con show_Reources and buildings
        facilities = facilities_manager.getFacilities()
        self._show_resources_and_buildings(resources_manager, resources_buildings, facilities)

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
        if research_lab is not None and research_lab['level'] >= 1:
            research_manager.checkResearches(session)
            researches = research_manager.getResearches() #Básicamente para mostrar las investigaciones show_researches
            self._show_researches(researches)
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

        #INFO DE DEFENSAS Y NAVES:
        if robot_factory is not None and robot_factory['level'] >= 2:
            if shipyard is not None:
                #No puedo pedir actualizar la info de las defensas o el hangar hasta que no sepa que tengo un hangar
                defenses_manager.checkDefenses(session) 
                defenses = defenses_manager.getDefenses()   #Básicamente para mostrar las defensas show_defenses
                self._show_defenses(defenses)
                shipyard_manager.checkShipyard(session)
                ships = shipyard_manager.getShips()
                self._show_ships(ships)                     #Básicamente para mostrar las naves con show_ships
        #RECUPERA INFO DEFENSAS:
        rocket_launchers = defenses_manager.getRocketLaunchers()
        light_lasers = defenses_manager.getLightLasers()
        heavy_lasers = defenses_manager.getHeavyLasers()
        small_shield_dome = defenses_manager.getSmallShieldDome()
        
        #RECUPERA INFO NAVES:
        light_fighters = shipyard_manager.getLightFighters()
        heavy_fighters = shipyard_manager.getHeavyFighters()
        cruisers = shipyard_manager.getCruisers()


        #Si ya hay una construcción en curso, no hagas nada.
        if(buildings_resources_manager.isConstructionInProgress()):
            print("Ya hay una construcción en curso: " + str(buildings_resources_manager.getBuildingBeingConstructed()) + ".")
            end_date = buildings_resources_manager.getBuildingDateToEndConstruction()
            if end_date:
                print("Fecha de finalización " + end_date.strftime('%Y-%m-%d %H:%M:%S') + "\n")
            return
        
        if(facilities_manager.isConstructionInProgress()):
            print("Ya hay una construcción en curso: " + str(facilities_manager.getBuildingBeingConstructed()) + ".")
            end_date = facilities_manager.getBuildingDateToEndConstruction()
            if end_date:
                print("Fecha de finalización " + end_date.strftime('%Y-%m-%d %H:%M:%S') + "\n")
            return
        

        #PRIORIDAD Nº1: Si no tienes energía, construye una planta de energía solar si puedes.
        if resources_manager.get_available_energy() <= 0:
            target = solar_plant
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        
        #PRIORIDAD Nº2: Si no tienes la mina de metal al menos a nivel 5, súbela
        if metal_mine is not None and metal_mine['level'] < 5:
            target = metal_mine
            self._build_target(target, resources_buildings, resources_manager, session)
            return
            
        #PRIORIDAD Nº3: Si no tienes la mina de cristal al menos a nivel 2, súbela
        if crystal_mine is not None and crystal_mine['level'] < 2:
            target = crystal_mine
            self._build_target(target, resources_buildings, resources_manager, session)
            return

        #PRIORIDAD Nº4: Si no tienes el sintetizador de deuterio al menos al nivel 3, súbelo
        if deuterium_synthesizer is not None and deuterium_synthesizer['level'] < 3:
            target = deuterium_synthesizer
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        
        #PRIORIDAD Nº5: Construir defensas, para ello subir la fábrica de robots para poder construir luego el hangar.
        if robot_factory is not None and robot_factory['level'] < 2:
            target = robot_factory
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        if shipyard is not None and shipyard['level'] < 1:
            target = shipyard
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        if shipyard is not None and shipyard['level'] >= 1:
            if rocket_launchers is not None and rocket_launchers['cantidad'] < 20:
                target = rocket_launchers
                quantity = 2
                self._build_defense(session, resources_manager, target, cantidad=quantity)
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return

        #PRIORIDAD Nº6: Boostear la producción de recursos
        if metal_mine is not None and metal_mine['level'] < 14:
            target = metal_mine
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        if crystal_mine is not None and crystal_mine['level'] < 12:
            target = crystal_mine
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        if deuterium_synthesizer is not None and deuterium_synthesizer['level'] < 7:
            target = deuterium_synthesizer
            self._build_target(target, resources_buildings, resources_manager, session)
            return

        #PRIORIDAD Nº7: Boostear la velocidad de construcción de naves, edificios e investigaciones
        #Primero sube el hangar para boostear la producción de defensas y luego primera etapa de subir el laboratorio de investigación:
        if shipyard is not None and shipyard['level'] < 4:
            if defenses_manager.isConstructionInProgress() is True:
                print("Hay una cola pendiente en el hangar, no se puede mejorar el hangar ahora")
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return
            target = shipyard
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        if robot_factory is not None and robot_factory['level'] < 4:
            target = robot_factory
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        if research_lab is not None and research_lab['level'] < 4:
            target = research_lab
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        
        #PRIORIDAD Nº8: Subir tecnologías
        if researches is not None:
            if energy_technology is not None and energy_technology['level'] < 2:
                target = energy_technology
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
            if laser_technology is not None and laser_technology['level'] < 3:
                target = laser_technology
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
            if armour_technology is not None and armour_technology['level'] < 2:
                target = armour_technology
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
            if weapons_technology is not None and weapons_technology['level'] < 3:
                target = weapons_technology
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
            if espionage_technology is not None and espionage_technology['level'] < 3:
                target = espionage_technology
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return

        #PRIORIDAD Nº9: Boostear puntos con cosas que realmente no vas a usar a priori
            if combustion_drive is not None and combustion_drive['level'] < 2:
                target = combustion_drive
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
            if computer_technology is not None and computer_technology['level'] < 2:
                target = computer_technology
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
        if robot_factory is not None and robot_factory['level'] < 5:
            target = robot_factory
            self._build_target(target, resources_buildings, resources_manager, session)
            return

        #PRIORIDAD Nº10: Aumentar más las defensas
        if shipyard is not None and shipyard['level'] >= 1:
            if light_lasers is not None and light_lasers['cantidad'] < 10:
                target = light_lasers
                quantity = 2
                self._build_defense(session, resources_manager, target, cantidad=quantity)
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return

        #PRIORIDAD Nº11: Aumentar las investigaciones para poder construir láseres grandes y las de defensa, militar y blindaje
        if research_lab is not None and research_lab['level'] < 6:   #Ve preparando poder meter la tecnología de defensa más adelante
            target = research_lab
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        if researches is not None:
            if energy_technology is not None and energy_technology['level'] < 3:
                target = energy_technology
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
            if laser_technology is not None and laser_technology['level'] < 6:
                target = laser_technology
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
            if shielding_technology is not None and shielding_technology['level'] < 4:
                target = shielding_technology
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
            if armour_technology is not None and armour_technology['level'] < 4:
                target = armour_technology
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
            if weapons_technology is not None and  weapons_technology['level'] < 4:
                target = weapons_technology
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return

        #PRIORIDAD Nº12: Boostear la producción de recursos
        if robot_factory is not None and robot_factory['level'] < 6:
            target = robot_factory
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        if metal_mine is not None and metal_mine['level'] < 16:
            target = metal_mine
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        if crystal_mine is not None and crystal_mine['level'] < 14:
            target = crystal_mine
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        if deuterium_synthesizer is not None and deuterium_synthesizer['level'] < 10:
            target = deuterium_synthesizer
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        
        #PRIORIDAD Nº13: Boostear puntos
        if fusion_reactor is not None and fusion_reactor['level'] < 4:
            target = fusion_reactor
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        if shipyard is not None and shipyard['level'] < 6:
            if defenses_manager.isConstructionInProgress() is True:
                print("Hay una cola pendiente en el hangar, no se puede mejorar el hangar ahora")
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return
            target = shipyard
            self._build_target(target, resources_buildings, resources_manager, session)
            return
        if researches is not None:
            if impulse_drive is not None and impulse_drive['level'] < 2:
                target = impulse_drive
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
            if combustion_drive is not None and combustion_drive['level'] < 3:
                target = combustion_drive
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
            if computer_technology is not None and computer_technology['level'] < 3:
                target = computer_technology
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return

        #PRIORIDAD Nº10: Aumentar más las defensas
        if shipyard is not None and shipyard['level'] >= 1:
            if small_shield_dome is not None and small_shield_dome['cantidad'] < 1:
                target = small_shield_dome
                quantity = 1
                self._build_defense(session, resources_manager, target, cantidad=quantity)
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return
            if heavy_lasers is not None and heavy_lasers['cantidad'] < 5:
                target = heavy_lasers
                quantity = 1
                self._build_defense(session, resources_manager, target, cantidad=quantity)
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return
            

        #PRIORIDAD Nº14: Construir naves
        if shipyard is not None and shipyard['level'] >= 3:
            if light_fighters is not None and light_fighters['cantidad'] < 20:
                target = light_fighters
                quantity = 2
                self._build_ship(session, resources_manager, target, cantidad=quantity)
                end_date = shipyard_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return
            if heavy_fighters is not None and heavy_fighters['cantidad'] < 12:
                target = heavy_fighters
                quantity = 1
                self._build_ship(session, resources_manager, target, cantidad=quantity)
                end_date = shipyard_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return

        #PRIORIDAD Nº15: Aumentar la velocidad de producción de naves y defensas
        if shipyard is not None and shipyard['level'] < 7:
            if defenses_manager.isConstructionInProgress() is True:
                print("Hay una cola pendiente en el hangar, no se puede mejorar el hangar ahora")
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return
            target = shipyard
            self._build_target(target, resources_buildings, resources_manager, session)
            return

        #PRIORIDAD Nº16: Desbloquear el motor de impulso para desbloquear los cruceros y construir aún más naves
        if researches is not None:
            if impulse_drive is not None and impulse_drive['level'] < 4:
                target = impulse_drive
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
            if energy_technology is not None and energy_technology['level'] < 4:
                target = energy_technology
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
            if ion_technology is not None and ion_technology['level'] < 2:
                target = ion_technology
                self._research_technology(target, resources_manager, resources_buildings, research_manager, session)
                return
        if shipyard is not None and shipyard['level'] >= 1:
            if light_fighters is not None and light_fighters['cantidad'] < 25:
                target = light_fighters
                quantity = 2
                self._build_ship(session, resources_manager, target, cantidad=quantity)
                end_date = shipyard_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return
            if heavy_fighters is not None and heavy_fighters['cantidad'] < 20:
                target = heavy_fighters
                quantity = 1
                self._build_ship(session, resources_manager, target, cantidad=quantity)
                end_date = shipyard_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return
            if cruisers is not None and cruisers['cantidad'] < 1:
                target = cruisers
                quantity = 1
                self._build_ship(session, resources_manager, target, cantidad=quantity)
                end_date = shipyard_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return

        #EN CUALQUIER OTRO CASO: Prioriza mina de metal 1 nivel por encima de la de cristal
        if (metal_mine is not None and metal_mine['level']) < (crystal_mine is not None and crystal_mine['level'] + 1):
            target = metal_mine
        else:
            target = crystal_mine
        self._build_target(target, resources_buildings, resources_manager, session)

    def decide_and_attack(self, session, fleet_manager: FleetManager):
        fleet_manager.checkAvailableShips(session)
        available_ships = fleet_manager.getShipsAvailable()
        print("\n\nNaves disponibles para enviar:")
        for ship in available_ships:
            print(ship)
        print("")
        attack_dice = int(random.random() * 100)
        if attack_dice > 95:
            if (fleet_manager.getHeavyFightersQuantity() > 19):      #Ataca sólo si tienes más de esta cantidad de fighters
                fleet_manager.sendRandomFleetToAttack(session)
            else:
                print("Intenté atacar, pero sólo tengo " + str(fleet_manager.getHeavyFightersQuantity()) + " cazadores pesados, y necesito por lo menos " + str(20) + " para atacar")
                print("")
        pass
