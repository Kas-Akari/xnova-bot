#Contiene funciones de utilidad comunes
import re

def extract_seconds_from_script(script_text: str) -> int:
    """
    Extrae el valor de 'ss' (segundos restantes) de un bloque de script.
    Ejemplo: ss = 24715;
    """
    match = re.search(r'ss\s*=\s*(\d+);', script_text)
    if match:
        return int(match.group(1))
    return -1