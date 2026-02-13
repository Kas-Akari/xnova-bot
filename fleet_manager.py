#Clase encargada de gestionar los movimientos de flotas
import random
from bs4 import BeautifulSoup   #Para analizar paginas HTML
from constants import BASE_URL

class FleetManager():
    def __init__(self) -> None:
        self.shipsAvailable = []
    
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
        post_data1 = {}
        for ship in self.shipsAvailable:
            cantidad = int(ship["cantidad"])
            cantidad_enviar = random.randint(int(cantidad - (cantidad/4)), cantidad)
            post_data1[ship["input_name"]] = str(cantidad_enviar)
        print("Enviando las siguientes flotas a atacar: " + str(post_data1))
        fleet_url = BASE_URL + 'game.php?page=fleet2'       
        response = session.post(fleet_url, data=post_data1)  #Simula pulsar "Continuar" enviando el formulario
        #print("URL tras el POST:", response.url)
        #print("")

        # Hardcodeamos las coordenadas de destino a 1:1:4
        post_data2 = {
            #ESTOS DATOS SON LOS IMPRESCINDIBLES PARA QUE FUNCIONE. Si no, vuelve a game,php?page=fleet1
            "galaxy": "1",
            "system": "1",
            "planet": "6",
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
        print("Atacando a: " + str(post_data2['galaxy'] + ":" + str(post_data2['system']) + ":" + str(post_data2['planet'])))
        #print("Post data de la selección de destino " + str(post_data2))
        fleet2_url = BASE_URL + 'game.php?page=fleet3'
        response = session.post(fleet2_url, data=post_data2)
        #print("URL tras el POST destino:", response.url)
        #print("")

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
        return