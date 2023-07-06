from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.token import get_current_active_user
from app.models.assembly import Assembly as AssemblyModel
from app.schemas.assembly import AssemblyPost, AssemblyPut
from app.models.product import Product as ProductModel
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.models.model import Model as ModelModel
from app.models.brand import Brand as BrandModel

assemblies_pr = APIRouter()

#!OBTENER ASSEMBLIES
@assemblies_pr.get('/obtenerAssemblies', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener assemblies')
async def obtener_assemblies(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    User_type = list(user.keys())[0]
    if User_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener todas las recomendaciones
        assemblies_db = db.query(AssemblyModel).all()
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

        # Crear el Json de respuesta
        response = []

        for assembly in assemblies_db:
            # Obtener el producto mayor
            major_product = db.query(ProductModel).filter(ProductModel.id == assembly.major_product_id).first()
            # Obtener el producto
            product = db.query(ProductModel).filter(ProductModel.id == assembly.product_id).first()
            # Obtener la categoria del producto mayor
            major_category = [category for category in categories_db if category['id'] == major_product.category_id]
            # Obtener el modelo del producto mayor
            major_model = [model for model in models_db if model.id == major_product.model_id]
            # Obtener la marca del producto mayor
            major_brand = [brand for brand in brands_db if brand.id == major_product.brand_id]
            # Obtener el estado del producto mayor
            major_status = [status for status in status_db if status['id'] == major_product.status_id]
            # Obtener la categoria del producto
            category = [category for category in categories_db if category['id'] == product.category_id]
            # Obtener el modelo del producto
            model = [model for model in models_db if model.id == product.model_id]
            # Obtener la marca del producto
            brand = [brand for brand in brands_db if brand.id == product.brand_id]
            # Obtener el estado del producto
            status = [status for status in status_db if status['id'] == product.status_id]

            # Crear el Json de respuesta
            assembly_json = {
                'id': assembly.id,
                'major_product': {
                    'id': major_product.id,
                    'name': major_product.name,
                    'description': major_product.description,
                    'path_image': major_product.path_image,
                    'quantity': major_product.quantity,
                    'price': major_product.price,
                    'discount': major_product.discount,
                    'warranty': major_product.warranty,
                    'category': major_category,
                    'brand': major_brand,
                    'model': major_model,
                    'status': major_status,
                    'ranking': major_product.ranking
                },
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'path_image': product.path_image,
                    'quantity': product.quantity,
                    'price': product.price,
                    'discount': product.discount,
                    'warranty': product.warranty,
                    'category': category,
                    'brand': brand,
                    'model': model,
                    'status': status,
                    'ranking': product.ranking
                },
                'description': assembly.description
            }
            response.append(assembly_json)
        return response

#!CREAR ASSEMBLY
@assemblies_pr.post('/crearAssembly', status_code=status.HTTP_201_CREATED, name='ADMINISTRADOR|TRABAJADOR - Crear Recomendación')
async def crear_assembly(assembly: AssemblyPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        assembly_db = AssemblyModel(
            major_product_id = assembly.major_product_id,
            product_id = assembly.product_id,
            description = assembly.description
        )
        db.add(assembly_db)
        db.commit()
        db.refresh(assembly_db)
        return {'message': 'Recomendación de ensamble creada exitosamente',
                'data': assembly_db}

#!ACTUALIZAR ASSEMBLY
@assemblies_pr.put('/actualizarAssembly/{id}', status_code=status.HTTP_202_ACCEPTED, name='ADMINISTRADOR|TRABAJADOR - Actualizar Recomendación')
async def actualizar_assembly(id:int, assembly: AssemblyPut, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        assembly_db = db.query(AssemblyModel).filter(AssemblyModel.id == id).first()
        if assembly_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El assembly no existe')
        else:
            db.query(AssemblyModel).filter(AssemblyModel.id == id).update({AssemblyModel.description: assembly.description})
            recomendation_updated = db.query(AssemblyModel).filter(AssemblyModel.id == id).first()
            return {'message': 'Recomendación de ensamble actualizada',
                    'data': recomendation_updated}
        
#!ELIMINAR ASSEMBLY
@assemblies_pr.delete('/eliminarAssembly/{id}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Eliminar Recomendación')
async def eliminar_assembly(id:int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        assembly_db = db.query(AssemblyModel).filter(AssemblyModel.id == id).first()
        if assembly_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El assembly no existe')
        else:
            db.delete(assembly_db)
            return {'message': 'Recomendación de ensamble eliminada'}