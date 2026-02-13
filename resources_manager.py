#Recupera los recursos disponibles (Metal, cruistal, deuterio, energía disponible)
from bs4 import BeautifulSoup   #Para analizar paginas HTML
from constants import BASE_URL

class ResourcesManager():
    def __init__(self) -> None:
        self.metal = 0
        self.crystal = 0
        self.deuterium = 0
        self.dark_matter = 0
        self.available_energy = 0
        self.metal_capacity = 0
        self.crystal_capacity = 0
        self.deuterium_capacity = 0
        self.metal_production_h = 0
        self.crystal_production_h = 0
        self.deuterium_production_h = 0

    def fetchResources(self, session) -> bool:
        #Ve a la página de opciones de recursos
        resources_url = BASE_URL + 'game.php?page=resourceSettings'
        response = session.post(resources_url, data="")

        #Analiza la respuesta HTML, todas las paginas tienen los recursos en el mismo sitio asi que da igual la ultima respuesta
        soup = BeautifulSoup(response.text, 'html.parser')

        # Busca la tabla de recursos por su id
        resources_table = soup.find('table', id='resources')  # Devuelve el elemento <table ... id="resources" ...>

        if resources_table is not None:
            # Busca todas las filas de la tabla
            rows = resources_table.find_all('tr')

            # La tercera fila (índice 2) tiene los valores numéricos de los recursos
            resource_values = rows[2].find_all('td') # Esto nos da una lista de <td>

            #Extrae el texto de cada <td> (quita espacios) y convirtelo a int
            self.metal               = int(resource_values[0].get_text(strip=True).replace('.',''))
            self.crystal             = int(resource_values[1].get_text(strip=True).replace('.',''))
            self.deuterium           = int(resource_values[2].get_text(strip=True).replace('.',''))
            self.dark_matter         = int(resource_values[3].get_text(strip=True).replace('.',''))
            self.available_energy    = int(resource_values[4].get_text(strip=True).split('/')[0])

            # Muestra los resultados por pantalla
            #print(f"Metal: {self.metal}")
            #print(f"Cristal: {self.crystal}")
            #print(f"Deuterio: {self.deuterium}")
            #print(f"Materia Oscura: {self.dark_matter}")
            #print(f"Energía disponible: {self.available_energy}\n")
            
            ##############################################################################################################
            #Obten la capacidad de almacenamiento:
            # Busca todas las filas de la tabla principal (la que contiene la capacidad de almacenamiento)
            all_rows = soup.find_all('tr')

            for row in all_rows:
                th = row.find('th')                                                     #La primera celda de la fila de la tabla es un th
                if th and th.get_text(strip=True) == "Capacidad de almacenamiento":     #Si encuentras la que pone "Capacidad de almacenamiento"
                    tds = row.find_all('td')                                            #Los tds que acompañan al th contienen las capacidades de almacenamiento
                    # Ahora tds[0] es metal, tds[1] es cristal, tds[2] es deuterio, tds[3] es energía
                    self.metal_capacity = self._parse_capacity(tds[0].get_text(strip=True))
                    self.crystal_capacity = self._parse_capacity(tds[1].get_text(strip=True))
                    self.deuterium_capacity = self._parse_capacity(tds[2].get_text(strip=True))
                    #print("Capacidad Metal:", self.metal_capacity)
                    #print("Capacidad Cristal:", self.crystal_capacity)
                    #print("Capacidad Deuterio:", self.deuterium_capacity)
                    #print("")
                if th and th.get_text(strip=True) == "Total por hora:":                  #Si encuentras la que pone "Total por hora"
                    tds = row.find_all('td')                                            #Los tds que acompañan al th contienen las producciones por hora
                    # Ahora tds[0] es metal, tds[1] es cristal, tds[2] es deuterio, tds[3] es energía
                    self.metal_production_h = int(tds[0].get_text(strip=True).replace('.',''))
                    self.crystal_production_h = int(tds[1].get_text(strip=True).replace('.',''))
                    self.deuterium_production_h = int(tds[2].get_text(strip=True).replace('.',''))
                    #print("Producción Metal/h:", self.metal_production_h)
                    #print("Producción Cristal/h:", self.crystal_production_h)
                    #print("Producción Deuterio/h:", self.deuterium_production_h)
                    #print("")
            return True
        else:
            print(f"No se encontro la tabla con los recursos")
            return False
        
    def get_metal(self) -> int:
        return self.metal
    
    def get_crystal(self) -> int:
        return self.crystal
    
    def get_deuterium(self) -> int:
        return self.deuterium
    
    def get_dark_matter(self) -> int:
        return self.dark_matter
    
    def get_available_energy(self) -> int:
        return self.available_energy
    
    def get_metal_capacity(self) -> int:
        return self.metal_capacity
    
    def get_crystal_capacity(self) -> int:
        return self.crystal_capacity
    
    def get_deuterium_capacity(self) -> int:
        return self.deuterium_capacity
    
    def get_metal_production_h(self) -> int:
        return self.metal_production_h
    
    def get_crystal_production_h(self) -> int:
        return self.crystal_production_h
    
    def get_deuterium_production_h(self) -> int:
        return self.deuterium_production_h

    def _parse_capacity(self, text: str) -> int:
        """Convierte de notación k a int (140k = 140000)."""
        return int(text[:-1]) * 1000    #Coge todo menos la última letra (la k), multiplícalo por 1000 y devuélvelo como int