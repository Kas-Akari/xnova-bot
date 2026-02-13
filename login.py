import requests                 #Librera para mandar peticiones HTTP
from constants import BASE_URL
from login_credentials import LOGIN_CREDENTIALS

def login(session, user_key: str) -> requests.Response | None:
    login_data = LOGIN_CREDENTIALS.get(user_key)    #Obten los datos de login según el usuario
    if not login_data:
        print(f"No se encontraron credenciales para el usuario '{user_key}' en login_credentials.py")
        return None
    login_url = BASE_URL + 'index.php'
    response = session.post(login_url, data=login_data)

    # Analizar la respuesta HTML (pagina que se carga tras intentar login)
    #soup = BeautifulSoup(response.text, 'html.parser')

    # Busca un texto o elemento único que solo exista si el login fue exitoso.
    if 'Jugadores: ' in response.text:
        return response
    else:
        return None





