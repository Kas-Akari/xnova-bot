#Clase encargada de gestionar los movimientos de flotas
import random
import json
import os
from bs4 import BeautifulSoup   #Para analizar paginas HTML
from constants import BASE_URL

class FleetManager():
    def __init__(self) -> None:
        self.shipsAvailable = []
        self.known_planets_path = os.path.join(os.path.dirname(__file__), 'known_planets.json')
        self.memory_path = os.path.join(os.path.dirname(__file__), 'bot_memory.json')
        self.known_planets = self.__load_known_planets()
        self.memory = self.__load_memory()
    
    def checkAvailableShips(self, session):
        self.shipsAvailable = []         #Limpia la lista de naves

        fleet_url = BASE_URL + 'game.php?page=fleet1'
        response = session.post(fleet_url, data="")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content_div = soup.find('div', id='content') #Encuentra el div con el id 'content'
        if content_div is None:
            print("No se encontró el div con id='content' en " + response.url)
            return
        ships_form = content_div.find('form')          #Dentro del div busca el formulario
        if ships_form is None:
            print("No se encontró la tabla de naves en el div con id='content' en " + response.url)
            return
        ships_table = ships_form.find('table')
        if ships_table is None:
            print("No se encontró la tabla de naves disponibles")
            return
        
        for row in ships_table.find_all('tr'):                #Los primeros tr en la tabla dan info, los siguientes las naves disponibles
            ths = row.find_all('th')                               #Dentro de cada tr, hay varios th
            if not ths:
                continue
            name = ths[0].get_text(strip=True)                      #El primer th es el nombre de la nave
            if name == "Tipo de nave":
                continue
            if name == "Ninguna nave":
                break
            if name == "No hay naves":
                print("No hay ninguna nave disponible en la página de flota")
                print("")
                return
            quantity_available = ths[1].get_text(strip=True)        #El segundo la cantidad
            input_tag = row.find('input')                           #Busca el primer input de la fila y obtiene el atributo 'name'
            input_name = input_tag['name'] if input_tag else None



            #Crea el diccionario del grupo de naves
            ships = {
                "name": name,
                "cantidad": quantity_available,
                "input_name": input_name
            }
            self.shipsAvailable.append(ships)

    def getShipsAvailable(self) -> list[dict]:
        return self.shipsAvailable

    def getLightFightersQuantity(self) -> int:
        for ship in self.shipsAvailable:
            if ship["name"] == "Cazador ligero":
                return int(ship["cantidad"])
        return 0
    
    def getHeavyFightersQuantity(self) -> int:
        for ship in self.shipsAvailable:
            if ship["name"] == "Cazador pesado":
                return int(ship["cantidad"])
        return 0

    def getCruisersQuantity(self) -> int:
        for ship in self.shipsAvailable:
            if ship["name"] == "Crucero":
                return int(ship["cantidad"])
        return 0
    
    def sendRandomFleetToAttack(self, session) -> None:
        #Selecciona un planeta válido para atacar
        last_user = self.memory.get('last_attacked_user', None)
        valid_planets = [p for p in self.known_planets if p['user'] != last_user]
        if not valid_planets:
            print("No hay planetas válidos para atacar (todos ya atacados o filtrados por 'TheBot')")
            return
        planet = random.choice(valid_planets)
        
        #1º Página de "Flota"
        post_data1 = {}
        for ship in self.shipsAvailable:
            cantidad = int(ship["cantidad"])
            cantidad_enviar = random.randint(int(cantidad - (cantidad/4)), cantidad)
            post_data1[ship["input_name"]] = str(cantidad_enviar)
        print("Enviando las siguientes flotas a atacar: " + str(post_data1))
        fleet_url = BASE_URL + 'game.php?page=fleet2'       
        response = session.post(fleet_url, data=post_data1)  #Simula pulsar "Continuar" enviando el formulario

        #2º Página de "Flota"
        post_data2 = {
            #ESTOS DATOS SON LOS IMPRESCINDIBLES PARA QUE FUNCIONE. Si no, vuelve a game,php?page=fleet1
            "galaxy": str(planet["galaxy"]),
            "system": str(planet["system"]),
            "planet": str(planet["planet"]),
            "planettype": "1",  # 1 = Planeta
            "speed": "10",       # 10 = 100%
            "target_mission": "0",
            "fleet_group": "0",
            "acs_target": "0:0:0",

            #"consumption202": "10",
            #"speed202": "7000",
            #"capacity202": "5000",
            #"ship202": "1",
            #"speedfactor": "1",
            #"thisgalaxy": "1",
            #"thissystem": "1",
            #"thisplanet": "1",
            #"thisplanettype": "1",
            #"colonies": "0"
        }
        print(f"Atacando a: {post_data2['galaxy']}:{post_data2['system']}:{post_data2['planet']} (Propietario: {planet['user']})")
        #print("Post data de la selección de destino " + str(post_data2))
        fleet2_url = BASE_URL + 'game.php?page=fleet3'
        response = session.post(fleet2_url, data=post_data2)
        #print("URL tras el POST destino:", response.url)
        #print("")

        #3º Página de "Flota"
        post_data3 = {
            #"thisresource1": "173272",
            #"thisresource2": "73312",
            #"thisresource3": "8325",
            #"thisgalaxy": "1",
            #"thissystem": "1",
            #"thisplanet": "1",
            #"thisplanettype": "1",
            #"galaxy": "1",
            #"system": "1",
            #"planet": "4",
            #"planettype": "1",
            #"speed": "10",
            #"speedfactor": "1",
            #"consumption205": "75",   # Ajusta según la nave seleccionada
            #"speed205": "14000",      # Ajusta según la nave seleccionada
            #"capacity205": "100",     # Ajusta según la nave seleccionada
            #"ship205": "1",           # Ajusta según la nave seleccionada y cantidad
            "mission": "1",           # 1 = Atacar
            "resource1": "",
            "resource2": "",
            "resource3": "",
            "holdingtime": "1"
        }
        fleet3_url = BASE_URL + 'game.php?page=fleet4'
        response = session.post(fleet3_url, data=post_data3)
        #print("URL tras el POST final:", response.url)
        print("")

        #Actualiza la memoria con el último usuario atacado
        self.memory['last_attacked_user'] = planet['user']
        self.__save_memory()
        return
    
    def __load_known_planets(self):
        #Lee el archivo de planetas conocidos y filtra los que no terminan en 'TheBot'
        try:
            with open(self.known_planets_path, 'r', encoding='utf-8') as f:
                planets = json.load(f)
        except Exception as e:
            print(f"Error leyendo known_planets.json: {e}")
            return []
        filtered = [p for p in planets if not p['user'].endswith('TheBot')]
        return filtered

    def __load_memory(self):
        #Crea el archivo si no existe, lo carga y lo devuelve
        if not os.path.exists(self.memory_path):
            with open(self.memory_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)
        try:
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error leyendo bot_memory.json: {e}")
            return {}

    def __save_memory(self):
        #Guarda el diccionario que hace de memoria
        try:
            with open(self.memory_path, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=4)
        except Exception as e:
            print(f"Error guardando bot_memory.json: {e}")