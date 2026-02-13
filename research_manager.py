#Gestiona la obtención de los datos sobre los edificios relaccionados con recuros del menú de "recursos"
import re                           #Importa la librería para comprobar expresiones regulares
from bs4 import BeautifulSoup   #Para analizar paginas HTML
from datetime import datetime, timedelta
from constants import BASE_URL
from utils import extract_seconds_from_script

class ResearchManager():
    def __init__(self) -> None:
        self.researches = {}
        self.isResearchActive = False
        self.date_to_end_research = None
        self.research_being_researched = None

    def checkResearches(self, session) -> None:
        self.researches = {}         #Limpia la lista de investigaciones

        researches_url = BASE_URL + 'game.php?page=research'
        response = session.post(researches_url, data="")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content_div = soup.find('div', id='content') #Encuentra el div con el id 'content'
        if content_div is None:
            print("No se encontró el div con id='content' en " + response.url)
            return
        researches_table = content_div.find('table') #Dentro del div busca la tabla
        if researches_table is None:
            print("No se encontró la tabla de instalaciones en el div con id='content' en " + response.url)
            return
        
        self.isResearchActive = False                         #Inicializa que se esté construyendo en false, si no encuentra los enlaces de mejorar levantará la flag a True
        self.date_to_end_research = None
        self.research_being_researched = None
        for row in researches_table.find_all('tr'):               #Para cada fila en la tabla de edificios, cada fila (tr) representa un edificio
            td = row.find('td')                             #En la tabla de investigaciones sólo hay 1 td y 2 th. El td contiene la info, el 2do th el enlace a investigar
            if not td:
                continue
            link = td.find('a')                             #Busca el enlace a la info de la investigación
            if not link:
                continue
            name = link.get_text(strip=True)                      #Extrae el nombre de la investigación eliminando los espacios del inicio y final (strip=True)
            level = 0                                             #Por defecto, si no encuentra luego el texto "Nivel", el nivel es 0
            next = link.next_sibling                              #Busca el texto que vene detrás del <a> al mismo nivel del árbol
            if next and 'Nivel' in str(next):                     #Si existe el texto y contiene la palabra "Nivel"
                match = re.search(r'Nivel (\d+)', str(next))      #Busca el número del nivel
                if match:                                         #Si lo encuentra, conviértelo a entero.
                    level = int(match.group(1))

            #Extrae los costes de construcción
            td_info_research_text = td.get_text(separator=' ', strip=True)
            metal_price = 0
            crystal_price = 0
            deuterium_price = 0
            m = re.search(r'Metal: ([\d\.]+)', td_info_research_text)
            if m:
                metal_price = int(m.group(1).replace('.', ''))
            c = re.search(r'Cristal: *([\d\.]+)', td_info_research_text)
            if c:
                crystal_price = int(c.group(1).replace('.', ''))
            d = re.search(r'Deuterio: *([\d\.]+)', td_info_research_text)
            if d:
                deuterium_price = int(d.group(1).replace('.', ''))

            #Extrae el enlace de "Investigar"
            url_investigar = None
            remaining_time = None
            ths = row.find_all('th')                    #Encuentra todas las celdas th de la fila actual de la tabla
            action_cell = ths[1]                      #La celda que contiene o el botón "Investigar" o "-" o el tiempo restante es el 2do th.
            investigar_link = action_cell.find('a')     #Si se puede investigar, existirá dentro del la celda de acción un <a> (enlace para investigar)
            script = action_cell.find('script')         #Si hay un edificio en contrucción, habrá un JavaScript con el código del timer
            if investigar_link:
                url_investigar = investigar_link.get('href')  #Guarda la URL de la acción de investigar esta investigación
            elif script and 'ss =' in script.text:      #Si no hay enlace, puede haber "-" o un script con el tiempo que está en segundos tras "ss ="
                self.isResearchActive = True
                self.research_being_researched = name
                remaining_time = extract_seconds_from_script(script.text)
                self.date_to_end_research = datetime.now() + timedelta(seconds=remaining_time)
                #print("Construcción de " + self.building_being_constructed + " en progreso. Tiempo restante (segundos): " + str(remaining_time))
                #print("Fecha de finalización: "+ self.date_to_end_construction.strftime('%Y-%m-%d %H:%M:%S') + "\n")
            
            #Crea el diccionario del edificio
            research = {
                "name": name,
                "level": level,
                "metal_price": metal_price,
                "crystal_price": crystal_price,
                "deuterium_price": deuterium_price,
                "url_investigar": url_investigar
            }
            self.researches[name] = research
        return
        
    
    def getResearches(self) -> dict[str, dict]:
        return self.researches
    
    def getEspionageTechnology(self) -> dict | None:
        return self.researches.get("Tecnología de espionaje")    
    
    def getComputerTechnology(self) -> dict | None:
        return self.researches.get("Tecnología de computación")
    
    def getWeaponsTechnology(self) -> dict | None:
        return self.researches.get("Tecnología militar")
    
    def getShieldingTechnology(self) -> dict | None:
        return self.researches.get("Tecnología de defensa")
    
    def getArmourTechnology(self) -> dict | None:
        return self.researches.get("Tecnología de blindaje")
    
    def getEnergyTechnology(self) -> dict | None:
        return self.researches.get("Tecnología de energía")
    
    def getHyperspaceTechnology(self) -> dict | None:
        return self.researches.get("Tecnología de hiperespacio")
    
    def getCombustionDrive(self) -> dict | None:
        return self.researches.get("Motor de combustión")
    
    def getImpulseDrive(self) -> dict | None:
        return self.researches.get("Motor de impulso")
    
    def getHyperspaceDrive(self) -> dict | None:
        return self.researches.get("Propulsor hiperespacial")
    
    def getLaserTechnology(self) -> dict | None:
        return self.researches.get("Tecnología láser")
    
    def getIonTechnology(self) -> dict | None:
        return self.researches.get("Tecnología iónica")
    
    def getPlasmaTechnology(self) -> dict | None:
        return self.researches.get("Tecnología de plasma")
    
    def getIntergalacticResearchNetwork(self) -> dict | None:
        return self.researches.get("Red de investigación intergaláctica")
    
    def getAstrophysic(self) -> dict | None:
        return self.researches.get("Astrofísica")
    
    def getGravitonTechnology(self) -> dict | None:
        return self.researches.get("Tecnología de gravitón")
    
    def isResearchInProgress(self) -> bool:
        return self.isResearchActive
    
    def getResearchDateToEnd(self) -> datetime | None:
        return self.date_to_end_research
    
    def getResearchBeingResearched(self) -> str | None:
        return self.research_being_researched
    