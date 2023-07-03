from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.combo import Combo as ComboModel
from app.models.product import Product as ProductModel
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.models.model import Model as ModelModel
from app.models.brand import Brand as BrandModel
from app.models.worker import Worker as WorkerModel
from app.models.user import User as UserModel

combo_pu = APIRouter()

#!COMBO
#GET ALL
@combo_pu.get('/listarCombos', status_code=status.HTTP_200_OK, name='Listado de combos')
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
        # Obtener el case
        case_db = db.query(ProductModel).filter(ProductModel.id == combo.case_id).first()
        case_db_json = {
            'id': case_db.id,
            'name': case_db.name,
            'description': case_db.description,
            'path_image': case_db.path_image,
            'price': case_db.price,
            'quantity': combo.quantity_case,
            'category': [category for category in categories_db if category['id'] == case_db.category_id],
            'brand': [brand for brand in brands_db if brand.id == case_db.brand_id],
            'model': [model for model in models_db if model.id == case_db.model_id],
            'status': [statusdb for statusdb in status_db if statusdb['id'] == case_db.status_id]
        }
        # Obtener la motherboard
        motherboard_db = db.query(ProductModel).filter(ProductModel.id == combo.motherboard_id).first()
        motherboard_db_json = {
            'id': motherboard_db.id,
            'name': motherboard_db.name,
            'description': motherboard_db.description,
            'path_image': motherboard_db.path_image,
            'price': motherboard_db.price,
            'quantity': combo.quantity_motherboard,
            'category': [category for category in categories_db if category['id'] == motherboard_db.category_id],
            'brand': [brand for brand in brands_db if brand.id == motherboard_db.brand_id],
            'model': [model for model in models_db if model.id == motherboard_db.model_id],
            'status': [statusdb for statusdb in status_db if statusdb['id'] == motherboard_db.status_id]
        }
        # Obtener el procesador
        procesador_db = db.query(ProductModel).filter(ProductModel.id == combo.processor_id).first()
        procesador_db_json = {
            'id': procesador_db.id,
            'name': procesador_db.name,
            'description': procesador_db.description,
            'path_image': procesador_db.path_image,
            'price': procesador_db.price,
            'quantity': combo.quantity_processor,
            'category': [category for category in categories_db if category['id'] == procesador_db.category_id],
            'brand': [brand for brand in brands_db if brand.id == procesador_db.brand_id],
            'model': [model for model in models_db if model.id == procesador_db.model_id],
            'status': [statusdb for statusdb in status_db if statusdb['id'] == procesador_db.status_id]
        }
        # Obtener la ram
        ram_db = db.query(ProductModel).filter(ProductModel.id == combo.ram_id).first()
        ram_db_json = {
            'id': ram_db.id,
            'name': ram_db.name,
            'description': ram_db.description,
            'path_image': ram_db.path_image,
            'price': ram_db.price,
            'quantity': combo.quantity_ram,
            'category': [category for category in categories_db if category['id'] == ram_db.category_id],
            'brand': [brand for brand in brands_db if brand.id == ram_db.brand_id],
            'model': [model for model in models_db if model.id == ram_db.model_id],
            'status': [statusdb for statusdb in status_db if statusdb['id'] == ram_db.status_id]
        }
        # Obtener el almacenamiento
        almacenamiento_db = db.query(ProductModel).filter(ProductModel.id == combo.almacenamiento_id).first()
        almacenamiento_db_json = {
            'id': almacenamiento_db.id,
            'name': almacenamiento_db.name,
            'description': almacenamiento_db.description,
            'path_image': almacenamiento_db.path_image,
            'price': almacenamiento_db.price,
            'quantity': combo.quantity_almacenamiento,
            'category': [category for category in categories_db if category['id'] == almacenamiento_db.category_id],
            'brand': [brand for brand in brands_db if brand.id == almacenamiento_db.brand_id],
            'model': [model for model in models_db if model.id == almacenamiento_db.model_id],
            'status': [statusdb for statusdb in status_db if statusdb['id'] == almacenamiento_db.status_id]
        }
        # Obtener el cooler
        cooler_db = db.query(ProductModel).filter(ProductModel.id == combo.cooler_id).first()
        if cooler_db is not None:
            cooler_db_json = {
                'id': cooler_db.id,
                'name': cooler_db.name,
                'description': cooler_db.description,
                'path_image': cooler_db.path_image,
                'price': cooler_db.price,
                'quantity': combo.quantity_cooler,
                'category': [category for category in categories_db if category['id'] == cooler_db.category_id],
                'brand': [brand for brand in brands_db if brand.id == cooler_db.brand_id],
                'model': [model for model in models_db if model.id == cooler_db.model_id],
                'status': [statusdb for statusdb in status_db if statusdb['id'] == cooler_db.status_id]
            }
        else:
            cooler_db_json = None
        # Obtener la gpu
        gpu_db = db.query(ProductModel).filter(ProductModel.id == combo.gpu_id).first()
        if gpu_db is not None:
            gpu_db_json = {
                'id': gpu_db.id,
                'name': gpu_db.name,
                'description': gpu_db.description,
                'path_image': gpu_db.path_image,
                'price': gpu_db.price,
                'quantity': combo.quantity_gpu,
                'category': [category for category in categories_db if category['id'] == gpu_db.category_id],
                'brand': [brand for brand in brands_db if brand.id == gpu_db.brand_id],
                'model': [model for model in models_db if model.id == gpu_db.model_id],
                'status': [statusdb for statusdb in status_db if statusdb['id'] == gpu_db.status_id]
            }
        else:
            gpu_db_json = None
        # Obtener el fan
        fan_db = db.query(ProductModel).filter(ProductModel.id == combo.fan_id).first()
        if fan_db is not None:
            fan_db_json = {
                'id': fan_db.id,
                'name': fan_db.name,
                'description': fan_db.description,
                'path_image': fan_db.path_image,
                'price': fan_db.price,
                'quantity': combo.quantity_fan,
                'category': [category for category in categories_db if category['id'] == fan_db.category_id],
                'brand': [brand for brand in brands_db if brand.id == fan_db.brand_id],
                'model': [model for model in models_db if model.id == fan_db.model_id],
                'status': [statusdb for statusdb in status_db if statusdb['id'] == fan_db.status_id]
            }
        else:
            fan_db_json = None
        # Obtener la fuente
        fuente_db = db.query(ProductModel).filter(ProductModel.id == combo.fuente_id).first()
        if fuente_db is not None:
            fuente_db_json = {
                'id': fuente_db.id,
                'name': fuente_db.name,
                'description': fuente_db.description,
                'path_image': fuente_db.path_image,
                'price': fuente_db.price,
                'quantity': combo.quantity_fuente,
                'category': [category for category in categories_db if category['id'] == fuente_db.category_id],
                'brand': [brand for brand in brands_db if brand.id == fuente_db.brand_id],
                'model': [model for model in models_db if model.id == fuente_db.model_id],
                'status': [statusdb for statusdb in status_db if statusdb['id'] == fuente_db.status_id]
            }
        else:
            fuente_db_json = None
        # Obtener el trabajador
        worker_db = db.query(WorkerModel).filter(WorkerModel.user_id == combo.worker_id).first()
        # Obtener el usuario
        user_db = db.query(UserModel).filter(UserModel.id == worker_db.user_id).first()
        worker_db_json = {
            'id': worker_db.id,
            'user': {
                'num_doc': user_db.num_doc,
                'username': user_db.username,
                'full_name': user_db.full_name,
                'email': user_db.email,
                'is_active': user_db.is_active,
            }
        }
        # Crear el Json de respuesta
        combo_json = {
            'id': combo.id,
            'name': combo.name,
            'description': combo.description,
            'path_image': combo.path_image,
            'case': case_db_json,
            'motherboard': motherboard_db_json,
            'procesador': procesador_db_json,
            'ram': ram_db_json,
            'almacenamiento': almacenamiento_db_json,
            'cooler': cooler_db_json,
            'gpu': gpu_db_json,
            'fan': fan_db_json,
            'fuente': fuente_db_json,
            'created_at': combo.created_at,
            'worker': worker_db_json,
        }
        # Agregar el combo al Json de respuesta
        reponse.append(combo_json)
    # Retornar combos
    return reponse

@combo_pu.get('/combo/{combo_id}', status_code=status.HTTP_200_OK, name='Obtener un combo')
async def get_combo(combo_id: str, db: Session = Depends(get_db)):
    # Obtener el combo
    combo_db = db.query(ComboModel).filter(ComboModel.id == combo_id).first()
    # Existe el combo?
    if combo_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El combo no existe')
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

    case_db = db.query(ProductModel).filter(ProductModel.id == combo_db.case_id).first()
    case_db_json = {
        'id': case_db.id,
        'name': case_db.name,
        'description': case_db.description,
        'path_image': case_db.path_image,
        'price': case_db.price,
        'quantity': combo_db.quantity_case,
        'category': [category for category in categories_db if category.id == case_db.category_id],
        'brand': [brand for brand in brands_db if brand.id == case_db.brand_id],
        'model': [model for model in models_db if model.id == case_db.model_id],
        'status': [statusdb for statusdb in status_db if statusdb.id == case_db.status_id]
    }
    motherboard_db = db.query(ProductModel).filter(ProductModel.id == combo_db.motherboard_id).first()
    motherboard_db_json = {
        'id': motherboard_db.id,
        'name': motherboard_db.name,
        'description': motherboard_db.description,
        'path_image': motherboard_db.path_image,
        'price': motherboard_db.price,
        'quantity': combo_db.quantity_motherboard,
        'category': [category for category in categories_db if category.id == motherboard_db.category_id],
        'brand': [brand for brand in brands_db if brand.id == motherboard_db.brand_id],
        'model': [model for model in models_db if model.id == motherboard_db.model_id],
        'status': [statusdb for statusdb in status_db if statusdb.id == motherboard_db.status_id]
    }
    procesador_db = db.query(ProductModel).filter(ProductModel.id == combo_db.procesador_id).first()
    procesador_db_json = {
        'id': procesador_db.id,
        'name': procesador_db.name,
        'description': procesador_db.description,
        'path_image': procesador_db.path_image,
        'price': procesador_db.price,
        'quantity': combo_db.quantity_procesador,
        'category': [category for category in categories_db if category.id == procesador_db.category_id],
        'brand': [brand for brand in brands_db if brand.id == procesador_db.brand_id],
        'model': [model for model in models_db if model.id == procesador_db.model_id],
        'status': [statusdb for statusdb in status_db if statusdb.id == procesador_db.status_id]
    }
    ram_db = db.query(ProductModel).filter(ProductModel.id == combo_db.ram_id).first()
    ram_db_json = {
        'id': ram_db.id,
        'name': ram_db.name,
        'description': ram_db.description,
        'path_image': ram_db.path_image,
        'price': ram_db.price,
        'quantity': combo_db.quantity_ram,
        'category': [category for category in categories_db if category.id == ram_db.category_id],
        'brand': [brand for brand in brands_db if brand.id == ram_db.brand_id],
        'model': [model for model in models_db if model.id == ram_db.model_id],
        'status': [statusdb for statusdb in status_db if statusdb.id == ram_db.status_id]
    }
    almacenamiento_db = db.query(ProductModel).filter(ProductModel.id == combo_db.almacenamiento_id).first()
    almacenamiento_db_json = {
        'id': almacenamiento_db.id,
        'name': almacenamiento_db.name,
        'description': almacenamiento_db.description,
        'path_image': almacenamiento_db.path_image,
        'price': almacenamiento_db.price,
        'quantity': combo_db.quantity_almacenamiento,
        'category': [category for category in categories_db if category.id == almacenamiento_db.category_id],
        'brand': [brand for brand in brands_db if brand.id == almacenamiento_db.brand_id],
        'model': [model for model in models_db if model.id == almacenamiento_db.model_id],
        'status': [statusdb for statusdb in status_db if statusdb.id == almacenamiento_db.status_id]
    }
    cooler_db = db.query(ProductModel).filter(ProductModel.id == combo_db.cooler_id).first()
    cooler_db_json = {
        'id': cooler_db.id,
        'name': cooler_db.name,
        'description': cooler_db.description,
        'path_image': cooler_db.path_image,
        'price': cooler_db.price,
        'quantity': combo_db.quantity_tarjeta_video,
        'category': [category for category in categories_db if category.id == cooler_db.category_id],
        'brand': [brand for brand in brands_db if brand.id == cooler_db.brand_id],
        'model': [model for model in models_db if model.id == cooler_db.model_id],
        'status': [statusdb for statusdb in status_db if statusdb.id == cooler_db.status_id]
    }
    gpu_db = db.query(ProductModel).filter(ProductModel.id == combo_db.gpu_id).first()
    gpu_db_json = {
        'id': gpu_db.id,
        'name': gpu_db.name,
        'description': gpu_db.description,
        'path_image': gpu_db.path_image,
        'price': gpu_db.price,
        'quantity': combo_db.quantity_cooler,
        'category': [category for category in categories_db if category.id == gpu_db.category_id],
        'brand': [brand for brand in brands_db if brand.id == gpu_db.brand_id],
        'model': [model for model in models_db if model.id == gpu_db.model_id],
        'status': [statusdb for statusdb in status_db if statusdb.id == gpu_db.status_id]
    }
    fan_db = db.query(ProductModel).filter(ProductModel.id == combo_db.fan_id).first()
    fan_db_json = {
        'id': fan_db.id,
        'name': fan_db.name,
        'description': fan_db.description,
        'path_image': fan_db.path_image,
        'price': fan_db.price,
        'quantity': combo_db.quantity_fan,
        'category': [category for category in categories_db if category.id == fan_db.category_id],
        'brand': [brand for brand in brands_db if brand.id == fan_db.brand_id],
        'model': [model for model in models_db if model.id == fan_db.model_id],
        'status': [statusdb for statusdb in status_db if statusdb.id == fan_db.status_id]
    }
    fuente_db = db.query(ProductModel).filter(ProductModel.id == combo_db.fuente_id).first()
    fuente_db_json = {
        'id': fuente_db.id,
        'name': fuente_db.name,
        'description': fuente_db.description,
        'path_image': fuente_db.path_image,
        'price': fuente_db.price,
        'quantity': combo_db.quantity_fuente,
        'category': [category for category in categories_db if category.id == fuente_db.category_id],
        'brand': [brand for brand in brands_db if brand.id == fuente_db.brand_id],
        'model': [model for model in models_db if model.id == fuente_db.model_id],
        'status': [statusdb for statusdb in status_db if statusdb.id == fuente_db.status_id]
    }
    worker_db = db.query(WorkerModel).filter(WorkerModel.id == combo_db.worker_id).first()
    user_db = db.query(UserModel).filter(UserModel.id == worker_db.user_id).first()
    worker_json = {
        'id': worker_db.id,
        'user': {
            'num_doc': user_db.num_doc,
            'username': user_db.username,
            'full_name': user_db.full_name,
            'email': user_db.email,
            'is_active': user_db.is_active
        }
    }
    combo_json = {
        'id': combo_db.id,
        'name': combo_db.name,
        'description': combo_db.description,
        'path_image': combo_db.path_image,
        'case': case_db_json,
        'motherboard': motherboard_db_json,
        'procesador': procesador_db_json,
        'ram': ram_db_json,
        'almacenamiento': almacenamiento_db_json,
        'cooler': cooler_db_json,
        'gpu': gpu_db_json,
        'fan': fan_db_json,
        'fuente': fuente_db_json,
        'created_at': combo_db.created_at,
        'worker': worker_json
    }
    return combo_json




