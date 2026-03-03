#Encargado de instanciar y devolver la estrategia a usar según el nombre de la estrategia
from .strategy_abstract import StrategyAbstract
from .strategy_normal import StrategyNormal
from .strategy_aggressive import StrategyAggressive

def get_strategy_instance(strategy_name: str) -> StrategyAbstract:
    # Diccionario de mapeo de nombre a clase de estrategia
    strategy_map = {
        "normal": StrategyNormal,
        "aggressive": StrategyAggressive,
        #"paceful": StrategyPaceful
    }
    #Devuelve una instancia de la clase correspondiente, o la estrategia por defecto
    strategy_class = strategy_map.get(strategy_name, StrategyNormal)
    return strategy_class()