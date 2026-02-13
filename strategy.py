#Métodos comunes a todas las estrategias:
from constants import BASE_URL

class Strategy():
    def _show_resources_and_buildings(self, resources_manager, resources_buildings, facilities):
        print("Recursos actuales/capacidad:")
        print(f"Metal: {resources_manager.get_metal()} | {resources_manager.get_metal_capacity()} | {resources_manager.get_metal_production_h()}/h")
        print(f"Cristal: {resources_manager.get_crystal()} | {resources_manager.get_crystal_capacity()} | {resources_manager.get_crystal_production_h()}/h")
        print(f"Deuterio: {resources_manager.get_deuterium()} | {resources_manager.get_deuterium_capacity()} | {resources_manager.get_deuterium_production_h()}/h")
        print(f"Energía disponible: {resources_manager.get_available_energy()}\n")
        print("Edificios de recursos disponibles:")
        for building in resources_buildings.values():
            print(building)
        print("\nInstalaciones disponibles:")
        for facility in facilities.values():
            print(facility)
        print("") #Separador

    def _show_defenses(self, defenses):
        print("Defensas construibles:")
        for defense in defenses.values():
            print(defense)
        print("") #Separador

    def _show_ships(self, ships):
        print("Naves construibles:")
        for ship in ships.values():
            print(ship)
        print("") #Separador

    def _show_researches(self, researches):
        print("Investigaciones disponibles para desarrollar:")
        for research in researches.values():
            print(research)
        print("") #Separador

    def _build_target(self,target, resources_buildings, resources_manager, session) -> None:
        if (resources_manager.get_metal() >= target['metal_price'] and
            resources_manager.get_crystal() >= target['crystal_price'] and
            target['url_mejorar']):
            #Pide construirla
            session.get(BASE_URL + target['url_mejorar'])
            print(f"Construyendo {target['name']}")
        elif (resources_manager.get_metal_capacity() <= target['metal_price']):
            print("Tengo " + str(resources_manager.get_metal_capacity()) + " de capacidad de metal, y necesito " + str(target['metal_price']) + " para construir " + str(target['name']) + ".")
            print("Cambio el objetivo a construir un almacén de metal.\n")
            self._build_target(resources_buildings['Almacén de Metal'], resources_buildings, resources_manager, session)
        elif (resources_manager.get_crystal_capacity() <= target['crystal_price']):
            print("Tengo " + str(resources_manager.get_crystal_capacity()) + " de capacidad de cristal, y necesito " + str(target['crystal_price']) + " para construir " + str(target['name']) + ".\n")
            print("Cambio el objetivo a construir un almacén de cristal.\n")
            self._build_target(resources_buildings['Almacén de Cristal'], resources_buildings, resources_manager, session)
        elif (resources_manager.get_deuterium_capacity() <= target['deuterium_price']):
            print("Tengo " + str(resources_manager.get_deuterium_capacity()) + " de capacidad de deuterio, y necesito " + str(target['deuterium_price']) + " para construir " + str(target['name']) + ".\n")
            print("Cambio el objetivo a construir un contenedor de deuterio.\n")
            self._build_target(resources_buildings['Contenedor de deuterio'], resources_buildings, resources_manager, session)
        else:
            print("No hay recursos suficientes para " + target['name'] +".")
            print("Tengo " + str(resources_manager.get_metal()) + " de metal, y necesito " + str(target['metal_price']) +
                  ". Tengo " + str(resources_manager.get_crystal()) + " de cristal, y necesito " + str(target['crystal_price']) +
                  ". Tengo " + str(resources_manager.get_deuterium()) + " de deuterio, y necesito " + str(target['deuterium_price']) + ".")
            metal_needed = max(0, target['metal_price'] - resources_manager.get_metal())
            crystal_needed = max(0, target['crystal_price'] - resources_manager.get_crystal())
            deuterium_needed = max(0, target['deuterium_price'] - resources_manager.get_deuterium())
            print("Me falta " + str(metal_needed) + " de metal, " + str(crystal_needed) + " de cristal y " + str(deuterium_needed) + " de deuterio.\n")
            time_to_metal_needed = metal_needed / resources_manager.get_metal_production_h()
            time_to_crystal_needed = crystal_needed / resources_manager.get_crystal_production_h()
            time_to_deuterium_needed = deuterium_needed / resources_manager.get_deuterium_production_h()
            print("Tardaré aproximadamente " + "{:.2f}".format(time_to_metal_needed) + " horas en conseguir el metal necesario.")
            print("Tardaré aproximadamente " + "{:.2f}".format(time_to_crystal_needed) + " horas en conseguir el cristal necesario.")
            print("Tardaré aproximadamente " + "{:.2f}".format(time_to_deuterium_needed) + " horas en conseguir el deuterio necesario.")

    def _build_defense(self, session, resources_manager, target, cantidad: int) -> None:
        data = {target['input_name']: cantidad}
        if (resources_manager.get_metal() >= target['metal_price'] * cantidad and
            resources_manager.get_crystal() >= target['crystal_price'] * cantidad):
            response = session.post(BASE_URL + "game.php?page=defense", data=data)
            print("Construyendo " + str(cantidad) + " " + target['name'] + ".")
            print("Precio: " + str(target['metal_price'] * cantidad) + " de metal y " + str(target['crystal_price'] * cantidad) + " de cristal.")
        else:
            print("No hay recursos suficientes para " + target['name'] +".")
            print("Tengo " + str(resources_manager.get_metal()) + " de metal, y necesito " + str(target['metal_price'] * cantidad) +
                  ". Tengo " + str(resources_manager.get_crystal()) + " de cristal, y necesito " + str(target['crystal_price'] * cantidad) +
                  ". Tengo " + str(resources_manager.get_deuterium()) + " de deuterio, y necesito " + str(target['deuterium_price'] * cantidad) + ".")
            metal_needed = max(0, target['metal_price'] * cantidad - resources_manager.get_metal())
            crystal_needed = max(0, target['crystal_price'] * cantidad - resources_manager.get_crystal())
            deuterium_needed = max(0, target['deuterium_price'] * cantidad - resources_manager.get_deuterium())
            print("Me falta " + str(metal_needed) + " de metal, " + str(crystal_needed) + " de cristal y " + str(deuterium_needed) + " de deuterio.\n")
            time_to_metal_needed = metal_needed / resources_manager.get_metal_production_h()
            time_to_crystal_needed = crystal_needed / resources_manager.get_crystal_production_h()
            time_to_deuterium_needed = deuterium_needed / resources_manager.get_deuterium_production_h()
            print("Tardaré aproximadamente " + "{:.2f}".format(time_to_metal_needed) + " horas en conseguir el metal necesario.")
            print("Tardaré aproximadamente " + "{:.2f}".format(time_to_crystal_needed) + " horas en conseguir el cristal necesario.")
            print("Tardaré aproximadamente " + "{:.2f}".format(time_to_deuterium_needed) + " horas en conseguir el deuterio necesario.")
            
    def _build_ship(self, session, resources_manager, target, cantidad: int) -> None:
        data = {target['input_name']: cantidad}
        if (resources_manager.get_metal() >= target['metal_price'] * cantidad and
            resources_manager.get_crystal() >= target['crystal_price'] * cantidad):
            response = session.post(BASE_URL + "game.php?page=shipyard", data=data)
            print("Construyendo " + str(cantidad) + " " + target['name'] + ".")
            print("Precio: " + str(target['metal_price'] * cantidad) + " de metal y " + str(target['crystal_price'] * cantidad) + " de cristal.")
        else:
            print("No hay recursos suficientes para " + str(cantidad) + " " + str(target['name']) + ".")
            print("Tengo " + str(resources_manager.get_metal()) + " de metal, y necesito " + str(target['metal_price'] * cantidad) +
                  ". Tengo " + str(resources_manager.get_crystal()) + " de cristal, y necesito " + str(target['crystal_price'] * cantidad) +
                  ". Tengo " + str(resources_manager.get_deuterium()) + " de deuterio, y necesito " + str(target['deuterium_price'] * cantidad) + ".")
            metal_needed = max(0, target['metal_price'] * cantidad - resources_manager.get_metal())
            crystal_needed = max(0, target['crystal_price'] * cantidad - resources_manager.get_crystal())
            deuterium_needed = max(0, target['deuterium_price'] * cantidad - resources_manager.get_deuterium())
            print("Me falta " + str(metal_needed) + " de metal, " + str(crystal_needed) + " de cristal y " + str(deuterium_needed) + " de deuterio.\n")
            time_to_metal_needed = metal_needed / resources_manager.get_metal_production_h()
            time_to_crystal_needed = crystal_needed / resources_manager.get_crystal_production_h()
            time_to_deuterium_needed = deuterium_needed / resources_manager.get_deuterium_production_h()
            print("Tardaré aproximadamente " + "{:.2f}".format(time_to_metal_needed) + " horas en conseguir el metal necesario.")
            print("Tardaré aproximadamente " + "{:.2f}".format(time_to_crystal_needed) + " horas en conseguir el cristal necesario.")
            print("Tardaré aproximadamente " + "{:.2f}".format(time_to_deuterium_needed) + " horas en conseguir el deuterio necesario.")

    def _research_technology(self, target, resources_manager, resources_buildings, research_manager, session) -> None:
        if self._check_research_in_progress(research_manager):
            return
        if (resources_manager.get_metal() >= target['metal_price'] and
            resources_manager.get_crystal() >= target['crystal_price'] and
            target['url_investigar']):
            session.get(BASE_URL + target['url_investigar'])
            print(f"Investigando {target['name']}")
        elif (resources_manager.get_metal_capacity() <= target['metal_price']):
            print("Tengo " + str(resources_manager.get_metal_capacity()) + " de capacidad de metal, y necesito " + str(target['metal_price']) + " para construir " + str(target['name']) + ".")
            print("Cambio el objetivo a construir un almacén de metal.\n")
            self._build_target(resources_buildings['Almacén de Metal'], resources_buildings, resources_manager, session)
        elif (resources_manager.get_crystal_capacity() <= target['crystal_price']):
            print("Tengo " + str(resources_manager.get_crystal_capacity()) + " de capacidad de cristal, y necesito " + str(target['crystal_price']) + " para construir " + str(target['name']) + ".\n")
            print("Cambio el objetivo a construir un almacén de cristal.\n")
            self._build_target(resources_buildings['Almacén de Cristal'], resources_buildings, resources_manager, session)
        elif (resources_manager.get_deuterium_capacity() <= target['deuterium_price']):
            print("Tengo " + str(resources_manager.get_deuterium_capacity()) + " de capacidad de deuterio, y necesito " + str(target['deuterium_price']) + " para construir " + str(target['name']) + ".\n")
            print("Cambio el objetivo a construir un contenedor de deuterio.\n")
            self._build_target(resources_buildings['Contenedor de deuterio'], resources_buildings, resources_manager, session)
        else:
            print("No hay recursos suficientes para " + target['name'] +".")
            print("Tengo " + str(resources_manager.get_metal()) + " de metal, y necesito " + str(target['metal_price']) +
                  ". Tengo " + str(resources_manager.get_crystal()) + " de cristal, y necesito " + str(target['crystal_price']) +
                  ". Tengo " + str(resources_manager.get_deuterium()) + " de deuterio, y necesito " + str(target['deuterium_price']) + ".")
            metal_needed = max(0, target['metal_price'] - resources_manager.get_metal())
            crystal_needed = max(0, target['crystal_price'] - resources_manager.get_crystal())
            deuterium_needed = max(0, target['deuterium_price'] - resources_manager.get_deuterium())
            print("Me falta " + str(metal_needed) + " de metal, " + str(crystal_needed) + " de cristal y " + str(deuterium_needed) + " de deuterio.\n")
            time_to_metal_needed = metal_needed / resources_manager.get_metal_production_h()
            time_to_crystal_needed = crystal_needed / resources_manager.get_crystal_production_h()
            time_to_deuterium_needed = deuterium_needed / resources_manager.get_deuterium_production_h()
            print("Tardaré aproximadamente " + "{:.2f}".format(time_to_metal_needed) + " horas en conseguir el metal necesario.")
            print("Tardaré aproximadamente " + "{:.2f}".format(time_to_crystal_needed) + " horas en conseguir el cristal necesario.")
            print("Tardaré aproximadamente " + "{:.2f}".format(time_to_deuterium_needed) + " horas en conseguir el deuterio necesario.")

    #Básicamente para poder estar construyendo mientras algo se investiga, pero no poder investigar si algo ya se está investigando
    def _check_research_in_progress(self, research_manager) -> bool:
        if(research_manager.isResearchInProgress()):
            print("Ya hay una investigación en curso: " + str(research_manager.getResearchBeingResearched()) + ".")
            end_date = research_manager.getResearchDateToEnd()
            if end_date:
                print("Fecha de finalización " + end_date.strftime('%Y-%m-%d %H:%M:%S') + "\n")
                return True
        return False