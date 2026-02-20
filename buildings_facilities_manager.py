#Gestiona la obtención de los datos sobre los edificios relaccionados con recuros del menú de "recursos"
import re                           #Importa la librería para comprobar expresiones regulares
from bs4 import BeautifulSoup   #Para analizar paginas HTML
from datetime import datetime, timedelta
from constants import BASE_URL
from utils import extract_seconds_from_script

class FacilitiesManager():
    def __init__(self) -> None:
        self.facilities = {}
        self.isConstructionActive = False
        self.date_to_end_construction = None
        self.building_being_constructed = None

    def updateFacilitiesInfo(self, session) -> None:
        self.facilities = {}         #Limpia la lista de edificios

        facilities_url = BASE_URL + 'game.php?page=station'
        response = session.post(facilities_url, data="")
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(response.url)
        
        content_div = soup.find('div', id='content') #Encuentra el div con el id 'content'
        if content_div is None:
            print("No se encontró el div con id='content' en " + response.url)
            return
        facilities_table = content_div.find('table') #Dentro del div busca la tabla
        if facilities_table is None:
            print("No se encontró la tabla de instalaciones en el div con id='content' en " + response.url)
            return
        
        self.isConstructionActive = False                         #Inicializa que se esté construyendo en false, si no encuentra los enlaces de mejorar levantará la flag a True
        self.date_to_end_construction = None
        self.building_being_constructed = None
        for row in facilities_table.find_all('tr'):                #Para cada fila en la tabla de edificios, cada fila (tr) representa un edificio
            cells = row.find_all('td')                            #Encuentra todas las celdas td de la fila actual de la tabla
            #Cada tr (fila de la tabla) tiene 3 td (celdas)
            td_info_building = cells[1]                           #La 2º es donde está el edificio y el nivel
            link = td_info_building.find('a')                     #Busca el enlace a la info del edificio.
            if not link:
                continue
            name = link.get_text(strip=True)                      #Extrae el nombre del edificio eliminando los espacios del inicio y final (strip=True)
            level = 0                                             #Por defecto, si no encuentra luego el texto "Nivel", el nivel es 0
            next = link.next_sibling                              #Busca el texto que vene detrás del <a> al mismo nivel del árbol
            if next and 'Nivel' in str(next):                     #Si existe el texto y contiene la palabra "Nivel"
                match = re.search(r'Nivel (\d+)', str(next))      #Busca el número del nivel
                if match:                                         #Si lo encuentra, conviértelo a entero.
                    level = int(match.group(1))

            #Extrae los costes de construcción
            td_info_facility_text = td_info_building.get_text(separator=' ', strip=True)
            metal_price = 0
            crystal_price = 0
            deuterium_price = 0
            m = re.search(r'Metal: ([\d\.]+)', td_info_facility_text)
            if m:
                metal_price = int(m.group(1).replace('.', ''))
            c = re.search(r'Cristal: *([\d\.]+)', td_info_facility_text)
            if c:
                crystal_price = int(c.group(1).replace('.', ''))
            d = re.search(r'Deuterio: *([\d\.]+)', td_info_facility_text)
            if d:
                deuterium_price = int(d.group(1).replace('.', ''))

            #Extrae el enlace de "Mejorar"
            url_mejorar = None
            remaining_time = None
            action_cell = cells[2]                      #La celda que contiene o el botón "Mejorar" o "-" o el tiempo restante es la 3era.
            mejorar_link = action_cell.find('a')        #Si se puede mejorar, existirá dentro del la celda de acción un <a> (enlace para mejorar)
            script = action_cell.find('script')         #Si hay un edificio en contrucción, habrá un JavaScript con el código del timer
            if mejorar_link:
                url_mejorar = mejorar_link.get('href')  #Guarda la URL de la acción de mejorar este edificio
            elif script and 'ss =' in script.text:      #Si no hay enlace, puede haber "-" o un script con el tiempo que está en segundos tras "ss ="
                self.isConstructionActive = True
                self.building_being_constructed = name
                remaining_time = extract_seconds_from_script(script.text)
                self.date_to_end_construction = datetime.now() + timedelta(seconds=remaining_time)
                #print("Construcción de " + self.building_being_constructed + " en progreso. Tiempo restante (segundos): " + str(remaining_time))
                #print("Fecha de finalización: "+ self.date_to_end_construction.strftime('%Y-%m-%d %H:%M:%S') + "\n")
            
            #Crea el diccionario del edificio
            facility = {
                "name": name,
                "level": level,
                "metal_price": metal_price,
                "crystal_price": crystal_price,
                "deuterium_price": deuterium_price,
                "url_mejorar": url_mejorar
            }
            self.facilities[name] = facility
        return
        
    
    def getFacilities(self) -> dict[str, dict]:
        return self.facilities
    
    def getRoboticsFactory(self) -> dict | None:
        return self.facilities.get("Fábrica de Robots")    

    def getShipyard(self) -> dict | None:
        return self.facilities.get("Hangar")
    
    def getResearchLab(self) -> dict | None:
        return self.facilities.get("Laboratorio de investigación")
    
    def getAllianceDepot(self) -> dict | None:
        return self.facilities.get("Depósito de la Alianza")

    def getSilo(self) -> dict | None:
        return self.facilities.get("Silo")

    def isConstructionInProgress(self) -> bool:
        return self.isConstructionActive
    
    def getBuildingDateToEndConstruction(self) -> datetime | None:
        return self.date_to_end_construction
    
    def getBuildingBeingConstructed(self) -> str | None:
        return self.building_being_constructed
    