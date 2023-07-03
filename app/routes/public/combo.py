from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.combo import Combo as ComboModel
from app.models.detail_combo import DetailCombo as DetailComboModel
from app.models.product import Product as ProductModel
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.models.model import Model as ModelModel
from app.models.brand import Brand as BrandModel
from app.models.worker import Worker as WorkerModel
from app.models.user import User as UserModel

combo_pu = APIRouter()

#!COMBO
#GET ALL
@combo_pu.get('/combos', status_code=status.HTTP_200_OK, name='Listado de combos')
async def get_combos(db: Session = Depends(get_db)):
    # Obtener todos los combos
    combos_db = db.query(ComboModel).all()
    # Obtener todas las categorias
    categories_db = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
    categories_db = [{'id': category.id_table, 'description': category.description} for category in categories_db]
    # Obtener todas las marcas
    brands_db = db.query(BrandModel).all()
    # Obtener todos los modelos
    models_db = db.query(ModelModel).all()
    # Obtener todos los estados de los productos
    status_db = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
    status_db = [{'id': statusdb.id_table, 'description': statusdb.description} for statusdb in status_db]

    # Crear el Json de respuesta
    reponse = []

    # Recorrer todos los combos
    for combo in combos_db:
        # Obtener el producto asociado al combo
        product = db.query(ProductModel).filter(ProductModel.id == combo.product_id).first()
        # Obtener todos los detalles asociados al combo
        details = db.query(DetailComboModel).filter(DetailComboModel.combo_id == combo.id).all()
        # Obtener la categoria del producto
        category = [category for category in categories_db if category['id'] == product.category_id]
        # Obtener la marca del producto
        brand = [brand for brand in brands_db if brand.id == product.brand_id]
        # Obtener el modelo del producto
        model = [model for model in models_db if model.id == product.model_id]
        # Obtener el estado del producto
        statusdb = [statusdb for statusdb in status_db if statusdb['id'] == product.status_id]
        # Obtener el usuario que creo el combo
        worker = db.query(WorkerModel).filter(WorkerModel.id == combo.worker_id).first()
        # Obtener el usuario que creo el combo
        user = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()

        # Crear el Json del combo
        combo_json = {
            'id': combo.id,
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
                'status': statusdb,
                'ranking': product.ranking
            },
            'created_at': combo.created_at,
            'worker': {
                'id': worker.id,
                'user': {
                    'num_doc': user.num_doc,
                    'username': user.username,
                    'full_name': user.full_name,
                    'email': user.email,
                    'is_active': user.is_active
                }
            },
            'details': []
        }

        # Recorrer todos los detalles del combo
        for detail in details:
            # Obtener el producto asociado al detalle
            product = db.query(ProductModel).filter(ProductModel.id == detail.product_id).first()
            # Obtener la categoria del producto
            category = [category for category in categories_db if category['id'] == product.category_id]
            # Obtener la marca del producto
            brand = [brand for brand in brands_db if brand.id == product.brand_id]
            # Obtener el modelo del producto
            model = [model for model in models_db if model.id == product.model_id]
            # Obtener el estado del producto
            statusdb = [statusdb for statusdb in status_db if statusdb['id'] == product.status_id]

            # Crear el Json del detalle
            detail_json = {
                'id': detail.id,
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
                    'status': statusdb,
                    'ranking': product.ranking
                },
                'quantity': detail.quantity
            }

            # Agregar el detalle al combo
            combo_json['details'].append(detail_json)

        # Agregar el combo a la respuesta
        reponse.append(combo_json)

    # Retornar la respuesta
    return reponse

#get id
@combo_pu.get('/combo/{combo_id}', status_code=status.HTTP_200_OK, name='Obtener un combo')
async def get_combo(combo_id: str, db: Session = Depends(get_db)):
    # Obtener el combo
    combo_db = db.query(ComboModel).filter(ComboModel.id == combo_id).first()
    if not combo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El combo no existe')
    # Obtener el producto asociado al combo
    product = db.query(ProductModel).filter(ProductModel.id == combo_db.product_id).first()
    # Obtener todos los detalles asociados al combo
    details = db.query(DetailComboModel).filter(DetailComboModel.combo_id == combo_db.id).all()
    # Obtener todas las categorias
    categories_db = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
    categories_db = [{'id': category.id_table, 'description': category.description} for category in categories_db]
    # Obtener todas las marcas
    brands_db = db.query(BrandModel).all()
    # Obtener todos los modelos
    models_db = db.query(ModelModel).all()
    # Obtener todos los estados de los productos
    status_db = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
    status_db = [{'id': statusdb.id_table, 'description': statusdb.description} for statusdb in status_db]
    # Obtener el usuario que creo el combo
    worker = db.query(WorkerModel).filter(WorkerModel.id == combo_db.worker_id).first()
    # Obtener el usuario que creo el combo
    user = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()

    # Crear el Json del combo
    combo_json = {
        'id': combo_db.id,
        'product': {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'path_image': product.path_image,
            'quantity': product.quantity,
            'price': product.price,
            'discount': product.discount,
            'warranty': product.warranty,
            'category': [category for category in categories_db if category['id'] == product.category_id],
            'brand': [brand for brand in brands_db if brand.id == product.brand_id],
            'model': [model for model in models_db if model.id == product.model_id],
            'status': [statusdb for statusdb in status_db if statusdb['id'] == product.status_id],
            'ranking': product.ranking
        },
        'created_at': combo_db.created_at,
        'worker': {
            'id': worker.id,
            'user': {
                'num_doc': user.num_doc,
                'username': user.username,
                'full_name': user.full_name,
                'email': user.email,
                'is_active': user.is_active
            }
        },
        'details': []
    }

    # Recorrer todos los detalles del combo
    for detail in details:
        # Obtener el producto asociado al detalle
        product = db.query(ProductModel).filter(ProductModel.id == detail.product_id).first()
        # Obtener la categoria del producto
        category = [category for category in categories_db if category['id'] == product.category_id]
        # Obtener la marca del producto
        brand = [brand for brand in brands_db if brand.id == product.brand_id]
        # Obtener el modelo del producto
        model = [model for model in models_db if model.id == product.model_id]
        # Obtener el estado del producto
        statusdb = [statusdb for statusdb in status_db if statusdb['id'] == product.status_id]

        # Crear el Json del detalle
        detail_json = {
            'id': detail.id,
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
                'status': statusdb,
                'ranking': product.ranking
            },
            'quantity': detail.quantity
        }

        # Agregar el detalle al combo
        combo_json['details'].append(detail_json)

    # Retornar la respuesta
    return combo_json