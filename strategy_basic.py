#Implementación de estrategia básica:
#Esta estrategia debe completarse por cada bot antes de que pueda pasar a estrategias específicas
#GARANTIZA QUE SI HAY UNA CONSTRUCCIÓN DE EDIFICIO O INSTALACIÓN EN CURSO, NO SE HACE NADA.
#(No es necesario comprobar eso en las estrategias que vengan detrás de esta)
#################################################################
# Esta estrategia básica garantiza que tras completarla tienes: #
# (Si aparece con 0, es que es construible aunque tenga 0)      #
# Edificios:                                                    #
#       - Mina de metal:                18                      #
#       - Mina de cristal:              16                      #
#       - Sintetizador de deuterio:     12                      #
#       - Planta de energía solar:      ?                       #
#       - Planta de fusión:             4                       #
#       - Almacén de metal:             ?                       #
#       - Almacén de cristal:           ?                       #
#       - Contenedor de deuterio:       ?                       #
# Instalaciones:                                                #
#       - Fábrica de robots:            6                       #
#       - Hangar:                       7                       #
#       - Laboratorio de investigación: 7                       #
#       - Depósito de la alianza:       0                       #
#       - Silo:                         0                       #
# Investigaciones:                                              #
#       - Tecnología de espionaje:      3                       #
#       - Tecnología de computación:    3                       #
#       - Tecnología militar:           4                       #
#       - Tecnología de defensa:        4                       #
#       - Tecnología de blindaje:       4                       #
#       - Tecnología de energía:        6                       #
#       - Motor de combustión:          3                       #
#       - Motor de impulso:             4                       #
#       - Tecnología láser:             6                       #
#       - Tecnología iónica:            4                       #
# Defensas:                                                     #
#       - Lanzamisiles:                 20                      #
#       - Láser pequeño:                10                      #
#       - Láser grande:                 20                      #
#       - Cañon Gauss:                  5                       #
#       - Cañon iónico:                 5                       #
#       - Cúpula pequeña de protección: 1                       #
# Naves:                                                        #
#       - Nave pequeña de carga:        0                       #
#       - Cazador ligero:               20                      #
#       - Cazador pesado:               12                      #
#       - Crucero:                      0                       #
#       - Colonizador:                  0                       #
#       - Sonda de espionaje:           0                       #
#       - Satélite solar:               0                       #
#################################################################
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

class StrategyBasic(Strategy, StrategyAbstract):
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


        #Si ya hay una construcción en curso, no hagas nada.
        if(buildings_resources_manager.isConstructionInProgress()):
            print("Ya hay una construcción en curso: " + str(buildings_resources_manager.getBuildingBeingConstructed()) + ".")
            end_date = buildings_resources_manager.getBuildingDateToEndConstruction()
            if end_date:
                print("Fecha de finalización " + end_date.strftime('%Y-%m-%d %H:%M:%S') + "\n")
            return False
        
        if(facilities_manager.isConstructionInProgress()):
            print("Ya hay una construcción en curso: " + str(facilities_manager.getBuildingBeingConstructed()) + ".")
            end_date = facilities_manager.getBuildingDateToEndConstruction()
            if end_date:
                print("Fecha de finalización " + end_date.strftime('%Y-%m-%d %H:%M:%S') + "\n")
            return False
        

        #PRIORIDAD Nº1: Si no tienes energía, construye una planta de energía solar si puedes.
        if resources_manager.get_available_energy() <= 0:
            target = solar_plant
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        
        #PRIORIDAD Nº2: Si no tienes la mina de metal al menos a nivel 5, súbela
        if metal_mine is not None and metal_mine['level'] < 5:
            target = metal_mine
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
            
        #PRIORIDAD Nº3: Si no tienes la mina de cristal al menos a nivel 2, súbela
        if crystal_mine is not None and crystal_mine['level'] < 2:
            target = crystal_mine
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False

        #PRIORIDAD Nº4: Si no tienes el sintetizador de deuterio al menos al nivel 3, súbelo
        if deuterium_synthesizer is not None and deuterium_synthesizer['level'] < 3:
            target = deuterium_synthesizer
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        
        #PRIORIDAD Nº5: Construir defensas, para ello subir la fábrica de robots para poder construir luego el hangar.
        if robot_factory is not None and robot_factory['level'] < 2:
            target = robot_factory
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        if shipyard is not None and shipyard['level'] < 1:
            target = shipyard
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        if shipyard is not None and shipyard['level'] >= 1:
            if rocket_launchers is not None and rocket_launchers['cantidad'] < 20:
                target = rocket_launchers
                quantity = 2
                self._build_defense(session, resources_manager, target, cantidad=quantity)
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False

        #PRIORIDAD Nº6: Boostear la producción de recursos
        if metal_mine is not None and metal_mine['level'] < 14:
            target = metal_mine
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        if crystal_mine is not None and crystal_mine['level'] < 12:
            target = crystal_mine
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        if deuterium_synthesizer is not None and deuterium_synthesizer['level'] < 7:
            target = deuterium_synthesizer
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False

        #PRIORIDAD Nº7: Boostear la velocidad de construcción de naves, edificios e investigaciones
        #Primero sube el hangar para boostear la producción de defensas y luego primera etapa de subir el laboratorio de investigación:
        if shipyard is not None and shipyard['level'] < 4:
            if defenses_manager.isConstructionInProgress() is True:
                print("Hay una cola pendiente en el hangar, no se puede mejorar el hangar ahora")
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False
            target = shipyard
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        if robot_factory is not None and robot_factory['level'] < 4:
            target = robot_factory
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        if research_lab is not None and research_lab['level'] < 4:
            target = research_lab
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        
        #PRIORIDAD Nº8: Subir tecnologías
        if researches is not None:
            if energy_technology is not None and energy_technology['level'] < 2:
                target = energy_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if laser_technology is not None and laser_technology['level'] < 3:
                target = laser_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if armour_technology is not None and armour_technology['level'] < 2:
                target = armour_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if weapons_technology is not None and weapons_technology['level'] < 3:
                target = weapons_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if espionage_technology is not None and espionage_technology['level'] < 3:
                target = espionage_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False

        #PRIORIDAD Nº9: Boostear puntos con cosas que realmente no vas a usar a priori
            if combustion_drive is not None and combustion_drive['level'] < 2:
                target = combustion_drive
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if computer_technology is not None and computer_technology['level'] < 2:
                target = computer_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
        if robot_factory is not None and robot_factory['level'] < 5:
            target = robot_factory
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False

        #PRIORIDAD Nº10: Aumentar más las defensas
        if shipyard is not None and shipyard['level'] >= 1:
            if light_lasers is not None and light_lasers['cantidad'] < 10:
                target = light_lasers
                quantity = 2
                self._build_defense(session, resources_manager, target, cantidad=quantity)
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False

        #PRIORIDAD Nº11: Aumentar las investigaciones para poder construir láseres grandes y las de defensa, militar y blindaje
        if research_lab is not None and research_lab['level'] < 6:   #Ve preparando poder meter la tecnología de defensa más adelante
            target = research_lab
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        if researches is not None:
            if energy_technology is not None and energy_technology['level'] < 3:
                target = energy_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if laser_technology is not None and laser_technology['level'] < 6:
                target = laser_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if shielding_technology is not None and shielding_technology['level'] < 4:
                target = shielding_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if armour_technology is not None and armour_technology['level'] < 4:
                target = armour_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if weapons_technology is not None and  weapons_technology['level'] < 4:
                target = weapons_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False

        #PRIORIDAD Nº12: Boostear la producción de recursos
        if robot_factory is not None and robot_factory['level'] < 6:
            target = robot_factory
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        if metal_mine is not None and metal_mine['level'] < 16:
            target = metal_mine
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        if crystal_mine is not None and crystal_mine['level'] < 14:
            target = crystal_mine
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        if deuterium_synthesizer is not None and deuterium_synthesizer['level'] < 10:
            target = deuterium_synthesizer
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        
        #PRIORIDAD Nº13: Boostear puntos
        if fusion_reactor is not None and fusion_reactor['level'] < 4:
            target = fusion_reactor
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        if shipyard is not None and shipyard['level'] < 6:
            if defenses_manager.isConstructionInProgress() is True:
                print("Hay una cola pendiente en el hangar, no se puede mejorar el hangar ahora")
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False
            target = shipyard
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        if researches is not None:
            if impulse_drive is not None and impulse_drive['level'] < 2:
                target = impulse_drive
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if combustion_drive is not None and combustion_drive['level'] < 3:
                target = combustion_drive
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if computer_technology is not None and computer_technology['level'] < 3:
                target = computer_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False

        #PRIORIDAD Nº14: Aumentar más las defensas
        if shipyard is not None and shipyard['level'] >= 1:
            if small_shield_dome is not None and small_shield_dome['cantidad'] < 1:
                target = small_shield_dome
                quantity = 1
                self._build_defense(session, resources_manager, target, cantidad=quantity)
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False
            if heavy_lasers is not None and heavy_lasers['cantidad'] < 5:
                target = heavy_lasers
                quantity = 1
                self._build_defense(session, resources_manager, target, cantidad=quantity)
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False
            
        #PRIORIDAD Nº15: Construir naves
        if shipyard is not None and shipyard['level'] >= 3:
            if light_fighters is not None and light_fighters['cantidad'] < 20:
                target = light_fighters
                quantity = 2
                self._build_ship(session, resources_manager, target, cantidad=quantity)
                end_date = shipyard_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False
            if heavy_fighters is not None and heavy_fighters['cantidad'] < 12:
                target = heavy_fighters
                quantity = 1
                self._build_ship(session, resources_manager, target, cantidad=quantity)
                end_date = shipyard_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False

        #PRIORIDAD Nº16: Aumentar la velocidad de producción de naves y defensas
        if shipyard is not None and shipyard['level'] < 7:
            if defenses_manager.isConstructionInProgress() is True:
                print("Hay una cola pendiente en el hangar, no se puede mejorar el hangar ahora")
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False
            target = shipyard
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        
        #PRIORIDAD Nº17: Aumenta la producción de recursos.    
        if metal_mine is not None and metal_mine['level'] < 18:
            target = metal_mine
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        if crystal_mine is not None and crystal_mine['level'] < 16:
            target = crystal_mine
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        if deuterium_synthesizer is not None and deuterium_synthesizer['level'] < 12:
            target = deuterium_synthesizer
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False

        #PRIORIDAD Nº18: Investiga lo necesario para desbloquear los cruceros, los cañones gauss y los cañones iónicos.
        if researches is not None:
            if impulse_drive is not None and impulse_drive['level'] < 4:
                target = impulse_drive
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if energy_technology is not None and energy_technology['level'] < 6:
                target = energy_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
            if ion_technology is not None and ion_technology['level'] < 4:
                target = ion_technology
                self._research_technology(target, resources_manager, buildings_resources_manager, research_manager, session)
                return False
        
        #PRIORIDAD Nº19: Aumenta la cantidad de defensas
        if shipyard is not None and shipyard['level'] >= 6:
            if heavy_lasers is not None and heavy_lasers['cantidad'] < 20:
                target = heavy_lasers
                quantity = 1
                self._build_defense(session, resources_manager, target, cantidad=quantity)
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False
            if gauss_cannons is not None and gauss_cannons['cantidad'] < 5:
                target = gauss_cannons
                quantity = 1
                self._build_defense(session, resources_manager, target, cantidad=quantity)
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False
            if ion_cannons is not None and ion_cannons['cantidad'] < 5:
                target = ion_cannons
                quantity = 1
                self._build_defense(session, resources_manager, target, cantidad=quantity)
                end_date = defenses_manager.getBuildingDateToEndConstruction()
                if end_date:
                    print("Fecha de finalización de la cola del hangar " + end_date.strftime('%Y-%m-%d %H:%M:%S'))
                return False
        
        #PRIORIDAD Nº20: Deja el laboratorio al menos al 7 para poder investigar la tecnología de hiperespacio y el propulsor hiperespacial
        if research_lab is not None and research_lab['level'] < 7:
            target = research_lab
            self._build_target(target, buildings_resources_manager, resources_manager, session)
            return False
        
        print(">>>> Estrategia básica completada <<<<")
        return True

    def decide_and_attack(self, session, fleet_manager: FleetManager):
        pass