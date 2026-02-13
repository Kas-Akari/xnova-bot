#Clase encargada de instanciar y devolver la estrategia a usar según el nombre de la estrategia
from strategy_simple import StrategySimple

def get_strategy_instance(strategy_name: str):
    # Diccionario de mapeo de nombre a clase de estrategia
    strategy_map = {
        "simple": StrategySimple,
        #"agressive": StrategyAgressive,
        #"paceful": StrategyPacefull
    }
    #Devuelve una instancia de la clase correspondiente, o la estrategia por defecto
    strategy_class = strategy_map.get(strategy_name, StrategySimple)
    return strategy_class()