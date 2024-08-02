import requests
from .models import ErrorHistory
import requests

## SE AGREGAN ACÁ LAS APIS PARA NO TENER QUE AGREGARLAS EN VIEWS #
# YA QUE SE EXTENDERIAN MUCHO EL CODIGO DE LA MISMA #
def obtener_licitaciones(filtro_id=None):
    """
    Obtiene licitaciones desde la API de Mercado Público.
    :return: Lista de diccionarios con info de las licitaciones, o None si hay un error en la solicitud.
    """
    ticket = "E9C79D57-5B5F-42DC-B118-C8172CA3E31E" ##TICKET API MERCADO PUBLICO
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
def subir_chatpdf(file_path):

    api_key = 'sec_tK5rAXVkeTNOhFjQUfJNeLq0rMlyFkjy' 
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
        registrar_error('subir_chatpdf', str(e))
        return None
    except Exception as e:
        registrar_error('subir_chatpdf', str(e))
        return None

def preguntar_chatpdf(source_id, pregunta, id_only=False):
    result= subir_chatpdf(source_id)
    api_key = 'sec_tK5rAXVkeTNOhFjQUfJNeLq0rMlyFkjy'  # Reemplaza con tu clave API real
    url = 'https://api.chatpdf.com/v1/chats/message'
    
    # Modificar contenido de la pregunta si es necesario
    content = pregunta
    if id_only:
        content = f"{pregunta} Por favor, responde solo con el ID de la licitación sin texto adicional, cabe mencionar que hay casos en que el ID se menciona como Número de Adquisición."

    # Datos para la solicitud
    question_data = {
        "sourceId": result,
        "messages": [
            {"role": "user", "content": content}
        ]
    }

    try:
        # Encabezados de la solicitud
        headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        }
        
        # Realizar la solicitud POST
        response = requests.post(url, headers=headers, json=question_data)
        response.raise_for_status()  # Lanzar una excepción para códigos de estado 4xx/5xx
        print(response.json())
        
        # Manejo de la respuesta
        data = response.json()
        if isinstance(data, dict) and 'content' in data:
            return data.content
        else:
            registrar_error('preguntar_chatpdf', f"Respuesta inesperada de la API: {data}")
            return None
    except requests.exceptions.RequestException as e:
        registrar_error('preguntar_chatpdf', str(e))
        return None
    except ValueError as e:
        registrar_error('preguntar_chatpdf', str(e))
        return None
    except Exception as e:
        registrar_error('preguntar_chatpdf', str(e))
        return None

def registrar_error(tipo_vista, descripcion):
    try:
        ErrorHistory.objects.create(
            tipo_vista=tipo_vista,
            descripcion=descripcion,
        )
    except Exception as e:
        print(f"Error al registrar el error en el historial: {str(e)}")
