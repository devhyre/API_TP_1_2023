from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.product import Product as ProductModel
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.models.brand import Brand as BrandModel
from app.models.model import Model as ModelModel

catalogue = APIRouter()

@catalogue.get('/obtenerProductos', status_code=status.HTTP_200_OK, name='Obtener catalogo de productos')
async def obtener_productos(db: Session = Depends(get_db)):
    # Obtener todos los productos con stock
    products_db = db.query(ProductModel).filter(ProductModel.quantity > 0).all()
    # Filtrar los productos con estado 4
    products_db = list(filter(lambda product: product.status_id == 4, products_db))
    # Obtener las marcas
    brands_db = db.query(BrandModel).all()
    # Obtener los modelos
    models_db = db.query(ModelModel).all()
    # Obtener las categorias
    categories_db = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
    categories_db = [{'id': category.id_table, 'description': category.description} for category in categories_db]
    # Obtener los estados de los productos
    status_db = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
    status_db = [{'id': status.id_table, 'description': status.description} for status in status_db]
    # Crear el Json de respuesta
    response = []
    for product in products_db:
        # Obtener la marca
        brand = next(filter(lambda brand: brand.id == product.brand_id, brands_db))
        # Obtener el modelo
        model = next(filter(lambda model: model.id == product.model_id, models_db))
        # Obtener la categoria
        category = next(filter(lambda category: category['id'] == product.category_id, categories_db))
        # Obtener el estado
        status = next(filter(lambda status: status['id'] == product.status_id, status_db))

        # Crear el Json
        product_json = {
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
            'ranking': product.ranking,
        }
        response.append(product_json)
    return response

@catalogue.get('/obtenerProducto/{id}', status_code=status.HTTP_200_OK, name='Obtener producto por id')
async def obtener_producto(id:int, db: Session = Depends(get_db)):
    # Buscar el producto
    product_db = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No existe el producto')
    # Verificar que el producto tenga stock y estado 4
    if product_db.quantity <= 0 or product_db.status_id != 4:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El producto no esta disponible')
    # Obtener la marca
    brand_db = db.query(BrandModel).filter(BrandModel.id == product_db.brand_id).first()
    # Obtener el modelo
    model_db = db.query(ModelModel).filter(ModelModel.id == product_db.model_id).first()
    # Obtener las categorias
    categories_db = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
    categories_db = [{'id': category.id_table, 'description': category.description} for category in categories_db]
    categoria_db = next(filter(lambda category: category['id'] == product_db.category_id, categories_db))
    # Obtener los estados de los productos
    status_db = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
    status_db = [{'id': status.id_table, 'description': status.description} for status in status_db]
    status_db = next(filter(lambda status: status['id'] == product_db.status_id, status_db))
    # Crear el Json de respuesta
    response = {
        'id': product_db.id,
        'name': product_db.name,
        'description': product_db.description,
        'path_image': product_db.path_image,
        'quantity': product_db.quantity,
        'price': product_db.price,
        'discount': product_db.discount,
        'warranty': product_db.warranty,
        'category': categoria_db,
        'brand': brand_db,
        'model': model_db,
        'status': status_db,
        'ranking': product_db.ranking,
    }
    return response
    
#!OBTENER TODOS LOS PRODUCTOS CON EL ESTADO 4(STOCK) POR CATEGORIAS, MARCAS, RANGO DE PRECIOS, RANGO DE DESCUENTOS Y RANGO DE RANKING. NO ES NECESARIO QUE SE INGRESEN TODOS LOS PARAMETROS, SOLO LOS QUE SE DESEEN FILTRAR.
@catalogue.get('/obtenerProductosFiltros', status_code=status.HTTP_200_OK, name='Filtro de productos')
async def obtener_productos_filtro(categoria_id: int = None, marca_id: int = None, precio_min: float = None, precio_max: float = None, descuento_min: int = None, descuento_max: int = None, ranking_min: int = None, ranking_max: int = None, db: Session = Depends(get_db)):
    #!OBTENER TODOS LOS PRODUCTOS
    products = db.query(ProductModel).all()
    #!VERIFICAR QUE PARAMETROS SE INGRESARON
    if categoria_id:
        FILTRO_CATEGORIA = filter(lambda product: product.category_id == categoria_id, products)
        products = list(FILTRO_CATEGORIA)
    if marca_id:
        FILTRO_MARCA = filter(lambda product: product.brand_id == marca_id, products)
        products = list(FILTRO_MARCA)
    if precio_min:
        FILTRO_PRECIO_MIN = filter(lambda product: product.price >= precio_min, products)
        products = list(FILTRO_PRECIO_MIN)
    if precio_max:
        FILTRO_PRECIO_MAX = filter(lambda product: product.price <= precio_max, products)
        products = list(FILTRO_PRECIO_MAX)
    if descuento_min:
        FILTRO_DESCUENTO_MIN = filter(lambda product: product.discount >= descuento_min, products)
        products = list(FILTRO_DESCUENTO_MIN)
    if descuento_max:
        FILTRO_DESCUENTO_MAX = filter(lambda product: product.discount <= descuento_max, products)
        products = list(FILTRO_DESCUENTO_MAX)
    if ranking_min:
        FILTRO_RANKING_MIN = filter(lambda product: product.ranking >= ranking_min, products)
        products = list(FILTRO_RANKING_MIN)
    if ranking_max:
        FILTRO_RANKING_MAX = filter(lambda product: product.ranking <= ranking_max, products)
        products = list(FILTRO_RANKING_MAX)
    return products