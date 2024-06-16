import requests


## SE AGREGAN ACÁ LAS APIS PARA NO TENER QUE AGREGARLAS EN VIEWS #
# YA QUE SE EXTENDERIAN MUCHO EL CODIGO DE LA MISMA #

# Función para obtener licitaciones desde la API de Mercado Público con filtros
def obtener_licitaciones(filtro_id=None, filtro_palabra_clave=None):
    """
    Obtiene licitaciones desde la API de Mercado Público con filtros opcionales por ID y palabra clave.
    
    :param filtro_id: ID de la licitación a buscar (opcional).
    :param filtro_palabra_clave: Palabra clave para filtrar las licitaciones por nombre o descripción (opcional).
    :return: Lista de licitaciones que cumplen con los filtros, o None si hay un error en la solicitud.
    """
    ticket = "F8537A18-6766-4DEF-9E59-426B4FEE2844"
    base_url = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
    
    # Construcción de la URL con los filtros adecuados
    if filtro_id:
        url_api = f"{base_url}?codigo={filtro_id}&estado=activas&ticket={ticket}"
    else:
        url_api = f"{base_url}?ticket={ticket}&estado=activas"
    
    try:
        respuesta = requests.get(url_api)
        respuesta.raise_for_status()  # Lanza una excepción para códigos de estado HTTP
        
        datos = respuesta.json()
        listado = datos.get('Listado', [])
        
        if filtro_palabra_clave:
            palabra_clave_upper = filtro_palabra_clave.upper()
            listado = [
                lic for lic in listado 
                if palabra_clave_upper in lic.get('Nombre', '').upper() or 
                   palabra_clave_upper in lic.get('Descripcion', '').upper()
            ]
        return listado
    
    except requests.exceptions.RequestException as e:
        # Manejo de excepciones en caso de error en la solicitud
        print(f"Error al obtener las licitaciones: {e}")
        return None
    


###################################################################################
# API_KEY = "sec_tK5rAXVkeTNOhFjQUfJNeLq0rMlyFkjy"
# API_KEY = "sec_toBfXEfGs83YOLY2RTr63iBC9jtiZGfg"

# FUNCIÓN PARA LLAMAR API DE CHATPDF
    
# Función para subir un archivo PDF a ChatPDF y obtener el sourceId
def subir_chatpdf(file_path):
    """
    Sube un archivo PDF a ChatPDF y obtiene el sourceId.

    :param file_path: Ruta del archivo PDF a subir.
    :return: sourceId del archivo subido, o None si hay un error en la solicitud.
    """
    api_key = 'sec_toBfXEfGs83YOLY2RTr63iBC9jtiZGfg'  # Utiliza la API_KEY correcta
    url = 'https://api.chatpdf.com/v1/sources/add-file'
    
    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            headers = {'x-api-key': api_key}
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
            
            data = response.json()
            return data.get('sourceId')
    
    except requests.exceptions.RequestException as e:
        print(f"Error al subir el archivo PDF: {e}")
        return None

# Función para hacer una pregunta sobre un PDF subido a ChatPDF
def preguntar_chatpdf(source_id, pregunta, id_only=False):
    """
    Hace una pregunta sobre un PDF subido a ChatPDF utilizando el sourceId.

    :param source_id: ID del source del archivo PDF.
    :param pregunta: Pregunta a realizar sobre el PDF.
    :param id_only: Indicador para obtener solo el ID de la licitación.
    :return: Respuesta de ChatPDF a la pregunta, o None si hay un error en la solicitud.
    """
    api_key = 'sec_toBfXEfGs83YOLY2RTr63iBC9jtiZGfg'  # Utiliza la API_KEY correcta
    url = 'https://api.chatpdf.com/v1/chats/message'
    
    content = pregunta
    if id_only:
        content = f"{pregunta} Por favor, responde solo con el ID de la licitación sin texto adicional."

    question_data = {
        "sourceId": source_id,
        "messages": [
            {"role": "user", "content": content}
        ]
    }
    
    try:
        headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=question_data)
        response.raise_for_status()
        
        data = response.json()
        return data.get('content')
    
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la pregunta: {e}")
        return None