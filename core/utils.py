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