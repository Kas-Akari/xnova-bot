#Gestiona la obtención de los datos sobre los edificios relaccionados con recuros del menú de "recursos"
import re                           #Importa la librería para comprobar expresiones regulares
from bs4 import BeautifulSoup   #Para analizar paginas HTML
from datetime import datetime, timedelta
from constants import BASE_URL

class ShipyardManager():
    def __init__(self) -> None:
        self.ships = {}
        self.isConstructionActive = False
        self.date_to_end_construction = None
        self.building_being_constructed = None

    def updateShipyardInfo(self, session) -> None:
        self.ships = {}         #Limpia la lista de naves diponibles para construir en el hangar

        shipyard_url = BASE_URL + 'game.php?page=shipyard'
        response = session.post(shipyard_url, data="")
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(response.url)
        
        content_div = soup.find('div', id='content') #Encuentra el div con el id 'content'
        if content_div is None:
            print("No se encontró el div con id='content' en " + response.url)
            return
        shipyard_table = content_div.find('table') #Dentro del div busca la tabla
        if shipyard_table is None:
            print("No se encontró la tabla de instalaciones en el div con id='content' en " + response.url)
            return
        

        for row in shipyard_table.find_all('tr'):                #Para cada fila en la tabla, cada fila (tr) representa un elemento
            td = row.find('td')                            #En la página de naves sólo hay 1 td por nave
            if not td:
                continue
            link = td.find('a')                            #Busca el enlace a la info de la nave.
            if not link:
                continue
            name = link.get_text(strip=True)                      #Extrae el nombre de la nave eliminando los espacios del inicio y final (strip=True)
            # Buscar cantidad disponible (si existe)
            next = link.next_sibling

            cantidad = 0
            if next and 'Disponible:' in str(next):
                match = re.search(r'Disponible: (\d+)', str(next))
                if match:
                    cantidad = int(match.group(1))

            # Extrae el gid de la URL
            gid_match = re.search(r'gid=(\d+)', str(link['href']))
            if not gid_match:
                continue
            gid = gid_match.group(1)
            input_name = f"fmenge[{gid}]"

            #Extrae los costes de construcción
            td_text = td.get_text(separator=' ', strip=True)
            metal_price = 0
            crystal_price = 0
            deuterium_price = 0
            m = re.search(r'Metal: ([\d\.]+)', td_text)
            if m:
                metal_price = int(m.group(1).replace('.', ''))
            c = re.search(r'Cristal: *([\d\.]+)', td_text)
            if c:
                crystal_price = int(c.group(1).replace('.', ''))
            d = re.search(r'Deuterio: *([\d\.]+)', td_text)
            if d:
                deuterium_price = int(d.group(1).replace('.', ''))

            #Crea el diccionario de la nave
            ship = {
                "name": name,
                "cantidad": cantidad,
                "input_name": input_name,
                "metal_price": metal_price,
                "crystal_price": crystal_price,
                "deuterium_price": deuterium_price
            }
            self.ships[name] = ship
        # Busca el tiempo restante de la cola de construcción
        match = re.search(r'(\d+h )?(\d+m )?(\d+s)<br></center>', response.text)
        if match:
            hours = int(match.group(1)[:-2]) if match.group(1) else 0
            minutes = int(match.group(2)[:-2]) if match.group(2) else 0
            seconds = int(match.group(3)[:-1]) if match.group(3) else 0
            total_seconds = int(hours * 3600 + minutes * 60 + seconds)
            self.isConstructionActive = True
            self.date_to_end_construction = datetime.now() + timedelta(seconds=total_seconds)
        else:
            self.isConstructionActive = False
            self.date_to_end_construction = None
        return
        
    
    def getShips(self) -> dict[str, dict]:
        return self.ships
    
    def getLightFighters(self) -> dict | None:
        return self.ships.get("Cazador ligero")
    
    def getHeavyFighters(self) -> dict | None:
        return self.ships.get("Cazador pesado")
    
    def getCruisers(self) -> dict | None:
        return self.ships.get("Crucero")
    
    def getBattleships(self) -> dict | None:
        return self.ships.get("Nave de batalla")
    
    def getBombers(self) -> dict | None:
        return self.ships.get("Bombardero")
    
    def getDestroyers(self) -> dict | None:
        return self.ships.get("Destructor")
    
    def getDeathstars(self) -> dict | None:
        return self.ships.get("Estrella de la muerte")
    
    def getSmallCargos(self) -> dict | None:
        return self.ships.get("Nave pequeña de carga")
    
    def getLargeCargos(self) -> dict | None:
        return self.ships.get("Nave grande de carga")
    
    def getColonyShips(self) -> dict | None:
        return self.ships.get("Colonizador")
    
    def getRecyclers(self) -> dict | None:
        return self.ships.get("Reciclador")
    
    def getEspionageProbes(self) -> dict | None:
        return self.ships.get("Sonda de espionaje")
    
    def getSolarSatellites(self) -> dict | None:
        return self.ships.get("Satélite solar")

    def getBattlecruisers(self) -> dict | None:
        return self.ships.get("Acorazado")

    def isConstructionInProgress(self) -> bool:
        return self.isConstructionActive
    
    def getBuildingDateToEndConstruction(self) -> datetime | None:
        return self.date_to_end_construction

    def getBuildingBeingConstructed(self) -> str | None:
        return self.building_being_constructed
    