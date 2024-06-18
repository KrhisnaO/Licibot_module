import requests
from django.core.exceptions import ValidationError

## SE AGREGAN ACÁ LAS APIS PARA NO TENER QUE AGREGARLAS EN VIEWS #
# YA QUE SE EXTENDERIAN MUCHO EL CODIGO DE LA MISMA #

# Función para obtener licitaciones desde la API de Mercado Público con filtros
def obtener_licitaciones(filtro_id=None):
    """
    Obtiene licitaciones desde la API de Mercado Público.
    :return: Lista de diccionarios con info de las licitaciones, o None si hay un error en la solicitud.
    """
    ticket = "F8537A18-6766-4DEF-9E59-426B4FEE2844" ##TICKET API MERCADO PUBLICO
    base_url = "https://api.mercadopublico.cl/servicios/v1/Publico/Licitaciones.json?"

    if filtro_id:
        url_api = f"{base_url}codigo={filtro_id}&ticket={ticket}"
    else:
        return None

    try:
        respuesta = requests.get(url_api)
        respuesta.raise_for_status()
        
        datos = respuesta.json()
        listado = datos.get('Listado', [])

        licitaciones = []
        for licitacion in listado:
            fecha_cierre = licitacion.get('FechaCierre', None)
            if fecha_cierre is None:
                fechas = licitacion.get('Fechas', {})
                fecha_cierre = fechas.get('FechaCierre', 'No encontrada')
                
            comprador = licitacion.get('Comprador', {})
            nombre_organismo = comprador.get('NombreOrganismo', 'No encontrado')
            
            licitaciones.append({
                'CodigoExterno': licitacion.get('CodigoExterno', ''),
                'Nombre': licitacion.get('Nombre', ''),
                'FechaCierre': fecha_cierre,
                'Descripcion': licitacion.get('Descripcion', ''),
                'Estado': licitacion.get('Estado', ''),
                'NombreOrganismo': nombre_organismo,
                'DiasCierreLicitacion': licitacion.get('DiasCierreLicitacion', None)
            })

        return licitaciones

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
