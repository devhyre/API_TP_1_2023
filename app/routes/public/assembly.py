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

#Mejor placa segun case
@assemblies_pu.get('/obtenerMejorPlaca', status_code=status.HTTP_200_OK)
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
@assemblies_pu.get('/obtenerMejorProcesador', status_code=status.HTTP_200_OK)
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
@assemblies_pu.get('/obtenerMejorRam', status_code=status.HTTP_200_OK)
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
@assemblies_pu.get('/obtenerMejorAlmacenamiento', status_code=status.HTTP_200_OK)
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
            if assembly.product_id == producto.id and producto.category_id == 9:
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
@assemblies_pu.get('/obtenerMejorCooler', status_code=status.HTTP_200_OK)
async def obtener_mejor_cooler(placa_id: int, procesador_id: int, case_id: int, gpu_id: int = None, db: Session = Depends(get_db)):
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
    #!BUSCAR QUE TODOS LOS PRODUCTOS SEAN DE LA CATEGORIA COOLER
    #Si no hay gpu
    if gpu_id == None:
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
        #!OBTENER TODOS LOS ASSEMBLIES RECOMENDADOS PARA LA GPU
        assemblies4 = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == gpu_id).all()

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

#Mejor fuente segun placa, procesador y case, si hubiera gpu tambien
@assemblies_pu.get('/obtenerMejorFuente', status_code=status.HTTP_200_OK)
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
                            if assembly.product_id == producto.id and producto.category_id == 11:
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
                                if assembly.product_id == producto.id and producto.category_id == 11:
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
@assemblies_pu.get('/obtenerMejorGpu', status_code=status.HTTP_200_OK)
async def obtener_mejor_gpu(placa_id: int, procesador_id: int, case_id: int, db: Session = Depends(get_db)):
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

    #!BUSCAR QUE TODOS LOS PRODUCTOS SEAN DE LA CATEGORIA GPU
    for assembly in assemblies:
        for assembly2 in assemblies2:
            for assembly3 in assemblies3:
                if assembly.product_id == assembly2.product_id and assembly2.product_id == assembly3.product_id:
                    for producto in productos:
                        if assembly.product_id == producto.id and producto.category_id == 5:
                            data["Id"].append(producto.id)
                            data["Name"].append(producto.name)
                            data["Price"].append(producto.price)
                            data["Discount"].append(producto.discount)
                            data["Ranking"].append(producto.ranking)
                            data["Warranty"].append(producto.warranty)
                            data["Description"].append(assembly.description)
    #!DEVOLVER DATA
    return data