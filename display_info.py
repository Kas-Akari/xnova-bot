def display_info(resources_manager, buildings_resources_manager, facilities_manager, research_manager, defenses_manager, shipyard_manager):
    show_resources(resources_manager)
    show_buildings(buildings_resources_manager.getResourcesBuildings(), facilities_manager.getFacilities())
    show_researches(research_manager.getResearches())
    show_defenses(defenses_manager.getDefenses())
    show_ships(shipyard_manager.getShips())

def show_resources(resources_manager):
    print("Recursos actuales/capacidad:")
    print(f"Metal: {resources_manager.get_metal()} | {resources_manager.get_metal_capacity()} | {resources_manager.get_metal_production_h()}/h")
    print(f"Cristal: {resources_manager.get_crystal()} | {resources_manager.get_crystal_capacity()} | {resources_manager.get_crystal_production_h()}/h")
    print(f"Deuterio: {resources_manager.get_deuterium()} | {resources_manager.get_deuterium_capacity()} | {resources_manager.get_deuterium_production_h()}/h")
    print(f"Energía disponible: {resources_manager.get_available_energy()}\n")
    print("") #Separador

def show_buildings(resources_buildings, facilities):
    print("Edificios de recursos disponibles:")
    for building in resources_buildings.values():
        print(building)
    print("\nInstalaciones disponibles:")
    for facility in facilities.values():
        print(facility)
    print("") #Separador

def show_researches(researches):
    print("Investigaciones disponibles para desarrollar:")
    for research in researches.values():
        print(research)
    print("") #Separador

def show_defenses(defenses):
    print("Defensas construibles:")
    for defense in defenses.values():
        print(defense)
    print("") #Separador

def show_ships(ships):
    print("Naves construibles:")
    for ship in ships.values():
        print(ship)
    print("") #Separador

