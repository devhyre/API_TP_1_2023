from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.assembly import Assembly as AssemblyModel
from app.models.product import Product as ProductModel
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.models.model import Model as ModelModel
from app.models.brand import Brand as BrandModel

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

#Mejor producto segun producto
@assemblies_pu.get('/obtenerMejorProducto/{producto_id}', status_code=status.HTTP_200_OK, name="Listado de Mejores Recomendaciones de Productos segun Producto")
async def obtener_mejor_producto(producto_id: int, db: Session = Depends(get_db)):
    # Obtener todas las recomendaciones del producto
    assemblies_db = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == producto_id).all()
    # Obtener el producto
    producto_db = db.query(ProductModel).filter(ProductModel.id == producto_id).first()
    # Obtener todas las categorias
    categories_db = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
    categories_db = [{'id': category.id_table, 'description': category.description} for category in categories_db]
    # Obtener todos los modelos
    models_db = db.query(ModelModel).all()
    # Obtener todas las marcas
    brands_db = db.query(BrandModel).all()
    # Obtener todos los estados de los productos
    status_db = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
    status_db = [{'id': status.id_table, 'description': status.description} for status in status_db]

    # Obtener la categoria del producto
    category = [category for category in categories_db if category['id'] == producto_db.category_id]
    # Obtener el modelo del producto
    model = [model for model in models_db if model.id == producto_db.model_id]
    # Obtener la marca del producto
    brand = [brand for brand in brands_db if brand.id == producto_db.brand_id]
    # Obtener el estado del producto
    status = [status for status in status_db if status['id'] == producto_db.status_id]
    
    # Crear el Json de producto
    producto_json = {
        'id': producto_db.id,
        'name': producto_db.name,
        'description': producto_db.description,
        'path_image': producto_db.path_image,
        'quantity': producto_db.quantity,
        'price': producto_db.price,
        'discount': producto_db.discount,
        'warranty': producto_db.warranty,
        'category': category,
        'brand': brand,
        'model': model,
        'status': status,
        'ranking': producto_db.ranking,
        'recommendations': []
    }

    # Recorrer todas las recomendaciones
    for assembly in assemblies_db:
        # Obtener el producto recomendado
        recommended_product = db.query(ProductModel).filter(ProductModel.id == assembly.product_id).first()
        # Obtener la categoria del producto recomendado
        recommended_category = [category for category in categories_db if category['id'] == recommended_product.category_id]
        # Obtener el modelo del producto recomendado
        recommended_model = [model for model in models_db if model.id == recommended_product.model_id]
        # Obtener la marca del producto recomendado
        recommended_brand = [brand for brand in brands_db if brand.id == recommended_product.brand_id]
        # Obtener el estado del producto recomendado
        recommended_status = [status for status in status_db if status['id'] == recommended_product.status_id]
        # Crear el Json del producto recomendado
        recommended_product_json = {
            'id': recommended_product.id,
            'name': recommended_product.name,
            'description': recommended_product.description,
            'path_image': recommended_product.path_image,
            'quantity': recommended_product.quantity,
            'price': recommended_product.price,
            'discount': recommended_product.discount,
            'warranty': recommended_product.warranty,
            'category': recommended_category,
            'brand': recommended_brand,
            'model': recommended_model,
            'status': recommended_status,
            'ranking': recommended_product.ranking,
        }
        # Agregar el producto recomendado al producto
        producto_json['recommendations'].append(recommended_product_json)

    return producto_json

#Mejor placa segun case
@assemblies_pu.get('/obtenerMejorPlaca', status_code=status.HTTP_200_OK, name="Listado de Mejores Recomendaciones de Placas")
async def obtener_mejor_placa(case_id: int, db: Session = Depends(get_db)):
    #!OBTENER TODOS LOS PRODUCTOS
    productos = db.query(ProductModel).all()
    #!OBTENER TODOS LOS ASSEMBLIES RECOMENDADOS PARA EL CASE
    assemblies = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == case_id).all()
    #!DATA A MOSTRAR
    data = {
        "Id": [],
        "Name": [],
        "Price": [],
        "Discount": [],
        "Ranking": [],
        "Warranty": [],
        "Description": []
    }
    #!BUSCAR QUE TODOS LOS PRODUCTOS SEAN DE LA CATEGORIA PLACA
    for assembly in assemblies:
        for producto in productos:
            if assembly.product_id == producto.id and producto.category_id == 7:
                data["Id"].append(producto.id)
                data["Name"].append(producto.name)
                data["Price"].append(producto.price)
                data["Discount"].append(producto.discount)
                data["Ranking"].append(producto.ranking)
                data["Warranty"].append(producto.warranty)
                data["Description"].append(assembly.description)
    #!DEVOLVER DATA
    return data

#Mejor procesador segun placa
@assemblies_pu.get('/obtenerMejorProcesador', status_code=status.HTTP_200_OK, name="Listado de Mejores Recomendaciones de Procesadores")
async def obtener_mejor_procesador(placa_id: int, db: Session = Depends(get_db)):
    #!OBTENER TODOS LOS PRODUCTOS
    productos = db.query(ProductModel).all()
    #!OBTENER TODOS LOS ASSEMBLIES RECOMENDADOS PARA LA PLACA
    assemblies = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == placa_id).all()
    #!DATA A MOSTRAR
    data = {
        "Id": [],
        "Name": [],
        "Price": [],
        "Discount": [],
        "Ranking": [],
        "Warranty": [],
        "Description": []
    }
    #!BUSCAR QUE TODOS LOS PRODUCTOS SEAN DE LA CATEGORIA PROCESADOR
    for assembly in assemblies:
        for producto in productos:
            if assembly.product_id == producto.id and producto.category_id == 8:
                data["Id"].append(producto.id)
                data["Name"].append(producto.name)
                data["Price"].append(producto.price)
                data["Discount"].append(producto.discount)
                data["Ranking"].append(producto.ranking)
                data["Warranty"].append(producto.warranty)
                data["Description"].append(assembly.description)
    #!DEVOLVER DATA
    return data

#Mejor ram segun placa y procesador
@assemblies_pu.get('/obtenerMejorRam', status_code=status.HTTP_200_OK, name="Listado de Mejores Recomendaciones de Ram")
async def obtener_mejor_ram(placa_id: int, procesador_id: int, db: Session = Depends(get_db)):
    #!OBTENER TODOS LOS PRODUCTOS
    productos = db.query(ProductModel).all()
    #!OBTENER TODOS LOS ASSEMBLIES RECOMENDADOS PARA LA PLACA
    assemblies = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == placa_id).all()
    #!OBTENER TODOS LOS ASSEMBLIES RECOMENDADOS PARA EL PROCESADOR
    assemblies2 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == procesador_id).all()
    #!DATA A MOSTRAR
    data = {
        "Id": [],
        "Name": [],
        "Price": [],
        "Discount": [],
        "Ranking": [],
        "Warranty": [],
        "Description": []
    }
    #!BUSCAR QUE LAS RAM SEAN COMPATIBLES CON LA PLACA Y PROCESADOR
    #Unir las dos listas y quedarme con los que se repiten
    for assembly in assemblies:
        for assembly2 in assemblies2:
            if assembly.product_id == assembly2.product_id:
                for producto in productos:
                    if assembly.product_id == producto.id and producto.category_id == 13:
                        data["Id"].append(producto.id)
                        data["Name"].append(producto.name)
                        data["Price"].append(producto.price)
                        data["Discount"].append(producto.discount)
                        data["Ranking"].append(producto.ranking)
                        data["Warranty"].append(producto.warranty)
                        data["Description"].append(assembly.description)
    #!DEVOLVER DATA
    return data

#Mejor almacenamiento segun placa
@assemblies_pu.get('/obtenerMejorAlmacenamiento', status_code=status.HTTP_200_OK, name="Listado de Mejores Recomendaciones de Almacenamiento")
async def obtener_mejor_almacenamiento(placa_id: int, db: Session = Depends(get_db)):
    #!OBTENER TODOS LOS PRODUCTOS
    productos = db.query(ProductModel).all()
    #!OBTENER TODOS LOS ASSEMBLIES RECOMENDADOS PARA LA PLACA
    assemblies = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == placa_id).all()
    #!DATA A MOSTRAR
    data = {
        "Id": [],
        "Name": [],
        "Price": [],
        "Discount": [],
        "Ranking": [],
        "Warranty": [],
        "Description": []
    }

    #!BUSCAR QUE TODOS LOS PRODUCTOS SEAN DE LA CATEGORIA ALMACENAMIENTO
    for assembly in assemblies:
        for producto in productos:
            if assembly.product_id == producto.id and (producto.category_id == 9 or producto.category_id == 12):
                data["Id"].append(producto.id)
                data["Name"].append(producto.name)
                data["Price"].append(producto.price)
                data["Discount"].append(producto.discount)
                data["Ranking"].append(producto.ranking)
                data["Warranty"].append(producto.warranty)
                data["Description"].append(assembly.description)
    #!DEVOLVER DATA
    return data


#Mejor Cooler segun placa, procesador y case, si hubiera gpu tambien
@assemblies_pu.get('/obtenerMejorCooler', status_code=status.HTTP_200_OK, name="Listado de Mejores Recomendaciones de Cooler")
async def obtener_mejor_cooler(placa_id: int, procesador_id: int, case_id: int, gpu_id: int = None, db: Session = Depends(get_db)):
    # Obtener todos los productos
    productos = db.query(ProductModel).all()

    # Obtener todos los assemblies recomendados para la placa
    assemblies = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == placa_id).all()

    # Obtener todos los assemblies recomendados para el procesador
    assemblies2 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == procesador_id).all()

    # Obtener todos los assemblies recomendados para el case
    assemblies3 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == case_id).all()

    # Crear un conjunto para almacenar los IDs de productos repetidos
    productos_repetidos = set()

    if gpu_id is None:
        for assembly in assemblies:
            if assembly.product_id in {a.product_id for a in assemblies2} and assembly.product_id in {a.product_id for a in assemblies3}:
                productos_repetidos.add(assembly.product_id)
    else:
        assemblies4 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == gpu_id).all()

        for assembly in assemblies:
            if assembly.product_id in {a.product_id for a in assemblies2} and assembly.product_id in {a.product_id for a in assemblies3} and assembly.product_id in {a.product_id for a in assemblies4}:
                productos_repetidos.add(assembly.product_id)

    data = {
        "Id": [],
        "Name": [],
        "Price": [],
        "Discount": [],
        "Ranking": [],
        "Warranty": [],
        "Description": []
    }

    for producto in productos:
        if producto.id in productos_repetidos and (producto.category_id == 15 or producto.category_id == 16):
            data["Id"].append(producto.id)
            data["Name"].append(producto.name)
            data["Price"].append(producto.price)
            data["Discount"].append(producto.discount)
            data["Ranking"].append(producto.ranking)
            data["Warranty"].append(producto.warranty)
            data["Description"].append(assembly.description)

    return data

#Mejor fuente segun placa, procesador y case, si hubiera gpu tambien
@assemblies_pu.get('/obtenerMejorFuente', status_code=status.HTTP_200_OK, name="Listado de Mejores Recomendaciones de Fuente")
async def obtener_mejor_fuente(placa_id: int, procesador_id: int, case_id: int, gpu_id: int = None, db: Session = Depends(get_db)):
    #!OBTENER TODOS LOS PRODUCTOS
    productos = db.query(ProductModel).all()

    #!OBTENER TODOS LOS ASSEMBLIES RECOMENDADOS PARA LA PLACA
    assemblies = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == placa_id).all()

    #!OBTENER TODOS LOS ASSEMBLIES RECOMENDADOS PARA EL PROCESADOR
    assemblies2 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == procesador_id).all()

    #!OBTENER TODOS LOS ASSEMBLIES RECOMENDADOS PARA EL CASE
    assemblies3 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == case_id).all()

    #!DATA A MOSTRAR
    data = {
        "Id": [],
        "Name": [],
        "Price": [],
        "Discount": [],
        "Ranking": [],
        "Warranty": [],
        "Description": []
    }
    #Si no hay gpu
    if gpu_id == None:
        #!BUSCAR QUE TODOS LOS PRODUCTOS SEAN DE LA CATEGORIA FUENTE
        for assembly in assemblies:
            for assembly2 in assemblies2:
                for assembly3 in assemblies3:
                    if assembly.product_id == assembly2.product_id and assembly2.product_id == assembly3.product_id:
                        for producto in productos:
                            if assembly.product_id == producto.id and producto.category_id == 10:
                                data["Id"].append(producto.id)
                                data["Name"].append(producto.name)
                                data["Price"].append(producto.price)
                                data["Discount"].append(producto.discount)
                                data["Ranking"].append(producto.ranking)
                                data["Warranty"].append(producto.warranty)
                                data["Description"].append(assembly.description)
    #Si hay gpu
    else:
        assemblies4 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == gpu_id).all()
        #!BUSCAR QUE TODOS LOS PRODUCTOS SEAN DE LA CATEGORIA FUENTE
        for assembly in assemblies:
            for assembly2 in assemblies2:
                for assembly3 in assemblies3:
                    for assembly4 in assemblies4:
                        if assembly.product_id == assembly2.product_id and assembly2.product_id == assembly3.product_id and assembly3.product_id == assembly4.product_id:
                            for producto in productos:
                                if assembly.product_id == producto.id and producto.category_id == 10:
                                    data["Id"].append(producto.id)
                                    data["Name"].append(producto.name)
                                    data["Price"].append(producto.price)
                                    data["Discount"].append(producto.discount)
                                    data["Ranking"].append(producto.ranking)
                                    data["Warranty"].append(producto.warranty)
                                    data["Description"].append(assembly.description)
    #!DEVOLVER DATA
    return data

#Mejor gpu segun placa, procesador y case
@assemblies_pu.get('/obtenerMejorGpu', status_code=status.HTTP_200_OK, name="Listado de Mejores Recomendaciones de Gpu")
async def obtener_mejor_gpu(placa_id: int, procesador_id: int, case_id: int, db: Session = Depends(get_db)):
    #!OBTENER TODOS LOS PRODUCTOS
    productos = db.query(ProductModel).all()

    #!OBTENER TODOS LOS ASSEMBLIES RECOMENDADOS PARA LA PLACA
    assemblies = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == placa_id).all()

    #!OBTENER TODOS LOS ASSEMBLIES RECOMENDADOS PARA EL PROCESADOR
    assemblies2 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == procesador_id).all()

    #!OBTENER TODOS LOS ASSEMBLIES RECOMENDADOS PARA EL CASE
    assemblies3 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == case_id).all()

    # Crear un conjunto para almacenar los IDs de productos repetidos
    productos_repetidos = set()

    # Verificar si un assembly está presente en las tres listas
    for assembly in assemblies:
        if assembly.product_id in {a.product_id for a in assemblies2} and assembly.product_id in {a.product_id for a in assemblies3}:
            productos_repetidos.add(assembly.product_id)

    #!DATA A MOSTRAR
    data = {
        "Id": [],
        "Name": [],
        "Price": [],
        "Discount": [],
        "Ranking": [],
        "Warranty": [],
        "Description": []
    }
    #Categoria 23

    # Filtrar los productos repetidos y agregarlos a los datos
    for producto in productos:
        if producto.id in productos_repetidos and producto.category_id == 23:
            data["Id"].append(producto.id)
            data["Name"].append(producto.name)
            data["Price"].append(producto.price)
            data["Discount"].append(producto.discount)
            data["Ranking"].append(producto.ranking)
            data["Warranty"].append(producto.warranty)
            data["Description"].append(assembly.description)

    # Devolver los datos
    return data