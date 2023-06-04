from urllib import response
from fastapi import HTTPException, status
import requests

"""
nro_doc: Número de documento
tipo_doc: 1 = DNI o 8 = RUC
"""
def get_peruvian_card(nro_doc:str, tipo_doc:int):
    url = 'https://api.apis.net.pe/v1/'
    tipo_map = {
        1: 'dni',
        6: 'ruc'
    }
    tipo = tipo_map[tipo_doc]
    url += tipo + '/?numero=' + nro_doc
    response = requests.get(url)
    data_map = {
        1: ['nombre', 'tipoDocumento', 'numeroDocumento', 'apellidoPaterno', 'apellidoMaterno', 'nombres'],
        6: ['nombre', 'tipoDocumento', 'numeroDocumento', 'estado', 'condicion']
    }
    data = data_map[tipo_doc]
    if response.status_code == 200:
        data = response.json()
        filtered_data = {key: data[key] for key in data_map[tipo_doc]}
        return filtered_data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurso no encontrado")

        