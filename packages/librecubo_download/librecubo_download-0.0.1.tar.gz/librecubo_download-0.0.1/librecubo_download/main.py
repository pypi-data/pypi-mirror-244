'''
Descripción de adc_download:
    Este paquete permite descargar imágenes satelitales utilizando la API de descarga de Planetary Computer,
    luego los apila con STAC stack y los guarda en un cubo de datos.
    La diferencia entre este paquete y y cubo.create es que lo guarda de forma estructurada en carpetas separado
    por id, sensores (de cada plataforma), data y metadata, etc. Además, permite descargar imágenes de varios sensores a la vez.    
    La estructura es la siguiente:
    - id
        - sensor1 (MSS)
            - data
                -.npy
            - metadata
                -.json
        - sensor2 (TM)
            - data
                -.npy
            - metadata
                -.json
        ...
        - sensorN (OLI)
            - data
                -.npy
            - metadata
                -.json
    Args:
        id (str): Identificador del cubo.
        lat (float): Latitud central del cubo.
        lon (float): Longitud central del cubo.
        collection (str): Lista de colecciones a descargar. Por defecto ["modis", "landsat", "sentinel-2"]
        bands (list): Bandas a descargar.
        start_date (str): Fecha de inicio del cubo.
        end_date (str): Fecha de fin del cubo.
        edge_size (int): Tamaño del borde del cubo (px).
        resolution (int): Tamaño del pixel del cubo (m).
        chunk (int): Periodo de tiempo para la descarga de las imágenes.
Principales dificultades:
    - El chunk debe ser dinámico, es decir, que para un periodo dado se debe descargar un numero igual de imágenes.
    - Si el token de PC caduca, se debe iniciar desde donde se detuvo la descarga.
'''

### Estructura ------------
def create(
    id: str,
    lat: float,
    lon: float,
    collection: list = ["modis-43A4-061", "landsat-c2-l2", "sentinel-2-l2a"],
    bands: list = None,
    start_date: str = "2021-04-01",
    end_date: str = "2021-06-10",
    edge_size: int = 512,
    resolution: int = 500,
    chunk: str
    ):
    """_summary_

    Args:
        id (str): _description_
        lat (float): _description_
        lon (float): _description_
        chunk (str): _description_
        collection (list, optional): _description_. Defaults to ["modis-43A4-061", "landsat-c2-l2", "sentinel-2-l2a"].
        bands (list, optional): _description_. Defaults to None.
        start_date (str, optional): _description_. Defaults to "2021-04-01".
        end_date (str, optional): _description_. Defaults to "2021-06-10".
        edge_size (int, optional): _description_. Defaults to 512.
        resolution (int, optional): _description_. Defaults to 500.

    Returns:
        _type_: _description_
    """    

    return None
### -----------------------