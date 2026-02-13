#Clase principal
import requests #Para mandar/recibir peticiones HTTP
import datetime
import sys      #Para procesar los argumentos de entrada
from user_config import USER_CONFIG
from strategy_selector import get_strategy_instance
from login import login
from resources_manager import ResourcesManager
from buildings_resources_manager import BuildingsResourcesManager
from strategy_simple import StrategySimple
from buildings_facilities_manager import FacilitiesManager
from defenses_manager import DefensesManager
from research_manager import ResearchManager
from shipyard_manager import ShipyardManager
from fleet_manager import FleetManager

class Bot:
    def __init__(self):
        self.session = requests.Session()   #Crea una sesión HTTP como instancia de objeto

    def doLogin(self, username):
        return login(self.session, username)

if __name__ == "__main__":
    #Cada archivo Python tiene una variable interna llamada __name__
    #Si ejecutas el archivo directamente (por ejemplo, python bot_login.py), entonces __name__ toma el valor "__main__"
    #Si importas el archivo desde otro script (import bot_login), entonces __name__ es el nombre real del archivo (bot_login)
    print(f"\n====================================================================\nBot ejecutado a las {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if len(sys.argv) < 2:
        print("Proporciona el nombre de usuario en minúsculas como argumento al ejecutar el bot. Por ej: python bot.py akari")
        sys.exit()
    username = sys.argv[1]
    bot = Bot()     #Crea el objeto principal
    response = bot.doLogin(username)
    if (response is not None):
        print("Login exitoso\n")
        resources_manager = ResourcesManager()
        buildings_resources_manager = BuildingsResourcesManager()
        facilities_manager = FacilitiesManager()
        research_manager = ResearchManager()
        defenses_manager = DefensesManager()
        shipyard_manager = ShipyardManager()      
        fleet_manager = FleetManager()
        #Obten la estrategia a utilizar en función del usuario que hizo login
        strategy_name = USER_CONFIG.get(username, {}).get("strategy", "simple")  #Por defecto 'simple'
        strategy = get_strategy_instance(strategy_name)
        strategy.decide_and_build(bot.session, resources_manager, buildings_resources_manager, facilities_manager, research_manager, defenses_manager, shipyard_manager)
        strategy.decide_and_attack(bot.session, fleet_manager)
    else:
        print("Login fallido o usuario/contraseña incorrectos")
