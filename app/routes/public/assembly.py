from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.assembly import Assembly as AssemblyModel
from app.models.product import Product as ProductModel

assemblies_pu = APIRouter()

#!OBTENER ASSEMBLLIES POR EL ID DEL MAJOR PRODUCT
#CASE
#PLACA
#PROCESADOR
#RAM
#ALMACENAMIENTO
#CPU_COOLER(*)
#GPU(*)
#FAN(*)
#FUENTE(*)

@assemblies_pu.get('/obtenerAssemblies', status_code=status.HTTP_200_OK)
async def obtener_assemblies(case_id: int, placa_id: int = None, procesador_id: int = None, ram_id: int=None,
                             gpu_id: int = None, db: Session = Depends(get_db)):
    #!OBTENER TODOS LOS PRODUCTOS
    productos = db.query(ProductModel).all()
    #!RECOMENDACIONES DE SOLO CASES
    assemblys = db.query(ProductModel).filter(ProductModel.category_id == 11).all()
    
    #SOLO MOSTRAR LAS PLACAS QUE SON COMPATIBLES CON EL CASE
    if case_id:
        #Busco en AssemblyModel el assembly que tenga el case_id
        assembly = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == case_id).all()
        #Busco los productos con assembly.product_id en la lista de productos
        for product in productos:
            if product.id == assembly[0].product_id:
                assemblys.append(product)
        #Filtro que los productos solo tengan la category_id = 7
        assemblys = list(filter(lambda x: x.category_id == 7, assemblys))
        return assemblys
    #SOLO MOSTRAR LOS PROCESADORES QUE SON COMPATIBLES CON LA PLACA
    if placa_id and case_id:
        #Busco en AssemblyModel el assembly que tenga el placa_id
        assembly = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == placa_id).all()
        #Busco los productos con assembly.product_id en la lista de productos
        for product in productos:
            if product.id == assembly[0].product_id:
                assemblys.append(product)
        #Filtro que los productos solo tengan la category_id = 8
        assemblys = list(filter(lambda x: x.category_id == 8, assemblys))
        return assemblys
    #SOLO MOSTRAR LAS RAMS QUE SON COMPATIBLES CON LA PLACA Y EL PROCESADOR
    if placa_id and procesador_id:
        #Busco en AssemblyModel el assembly que tenga el placa_id
        assembly = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == placa_id).all()
        #Busco en AssemblyModel el assembly que tenga el procesador_id
        assembly2 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == procesador_id).all()
        lista_unida = []
        #Busco los product_id iguales en ambas listas
        for product in assembly:
            for product2 in assembly2:
                if product.product_id == product2.product_id:
                    lista_unida.append(product.product_id)
        #Busco los productos con assembly.product_id en la lista de productos
        for product in productos:
            if product.id in lista_unida:
                assemblys.append(product)
        #Filtro que los productos solo tengan la category_id = 13
        assemblys = list(filter(lambda x: x.category_id == 13, assemblys))
        return assemblys
    #SOLO MOSTRAR LOS ALMACENAMIENTOS QUE SON COMPATIBLES CON LA PLACA PERO TIENEN QUE HABER PEDIDO TODOS LOS COMPONENTES ANTERIORES
    if placa_id and procesador_id and ram_id and case_id:
        #Busco en AssemblyModel el assembly que tenga el placa_id
        assembly = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == placa_id).all()
        #Busco los productos con assembly.product_id en la lista de productos
        for product in productos:
            if product.id == assembly[0].product_id:
                assemblys.append(product)
        #Filtro que los productos solo tengan la category_id = 9 y 12
        assemblys = list(filter(lambda x: x.category_id == 9 and x.category_id == 12, assemblys))
        return assemblys
    #SOLO MOSTRAR LAS GPUS QUE SON COMPATIBLES CON LA PLACA Y EL PROCESADOR
    if placa_id and procesador_id:
        #Busco en AssemblyModel el assembly que tenga el placa_id
        assembly = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == placa_id).all()
        #Busco en AssemblyModel el assembly que tenga el procesador_id
        assembly2 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == procesador_id).all()
        lista_unida = []
        #Busco los product_id iguales en ambas listas
        for product in assembly:
            for product2 in assembly2:
                if product.product_id == product2.product_id:
                    lista_unida.append(product.product_id)
        #Busco los productos con assembly.product_id en la lista de productos
        for product in productos:
            if product.id in lista_unida:
                assemblys.append(product)
        #Filtro que los productos solo tengan la category_id = 23
        assemblys = list(filter(lambda x: x.category_id == 23, assemblys))
        return assemblys
    #SOLO MOSTRAR LAS FUENTES QUE SON COMPATIBLES CON LA PLACA, PROCESADOR Y  EN CASO DE TENER GPU CON LA GPU
    if placa_id and procesador_id and gpu_id:
        #Busco en AssemblyModel el assembly que tenga el placa_id
        assembly = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == placa_id).all()
        #Busco en AssemblyModel el assembly que tenga el procesador_id
        assembly2 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == procesador_id).all()
        #Busco en AssemblyModel el assembly que tenga el gpu_id
        assembly3 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == gpu_id).all()
        lista_unida = []
        #Busco los product_id iguales en ambas listas
        for product in assembly:
            for product2 in assembly2:
                for product3 in assembly3:
                    if product.product_id == product2.product_id == product3.product_id:
                        lista_unida.append(product.product_id)
        #Busco los productos con assembly.product_id en la lista de productos
        for product in productos:
            if product.id in lista_unida:
                assemblys.append(product)
        #Filtro que los productos solo tengan la category_id = 10
        assemblys = list(filter(lambda x: x.category_id == 10, assemblys))
        return assemblys
    #SOLO MOSTRAR LOS COOLERS QUE SON COMPATIBLES CON LA PLACA, EL PROCESADOR Y EN CASO DE TENER GPU CON LA GPU
    if placa_id and procesador_id and gpu_id and case_id:
        #Busco en AssemblyModel el assembly que tenga el placa_id
        assembly = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == placa_id).all()
        #Busco en AssemblyModel el assembly que tenga el procesador_id
        assembly2 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == procesador_id).all()
        #Busco en AssemblyModel el assembly que tenga el gpu_id
        assembly3 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == gpu_id).all()
        #Busco en AssemblyModel el assembly que tenga el case_id
        assembly4 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == case_id).all()
        lista_unida = []
        #Busco los product_id iguales que tengan en comun las 4 listas
        for product in assembly:
            for product2 in assembly2:
                for product3 in assembly3:
                    for product4 in assembly4:
                        if product.product_id == product2.product_id == product3.product_id == product4.product_id:
                            lista_unida.append(product.product_id)
        #Busco los productos con assembly.product_id en la lista de productos
        for product in productos:
            if product.id in lista_unida:
                assemblys.append(product)
        #Filtro que los productos solo tengan la category_id = 15 y 16
        assemblys = list(filter(lambda x: x.category_id == 15 and x.category_id == 16, assemblys))
        return assemblys