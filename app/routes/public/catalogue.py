from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.product import Product as ProductModel
import itertools

catalogue = APIRouter()

@catalogue.get('/obtenerProductos')
async def obtener_productos(db: Session = Depends(get_db)):
    products_4 = db.query(ProductModel).filter(ProductModel.status_id == 4).all()
    products_1 = db.query(ProductModel).filter(ProductModel.status_id == 1).all()
    products = products_4 + products_1
    return products

@catalogue.get('/obtenerProducto/{id}')
async def obtener_producto(id:int, db: Session = Depends(get_db)):
    product_4 = db.query(ProductModel).filter(ProductModel.id == id).filter(ProductModel.status_id == 4).first()
    product_1 = db.query(ProductModel).filter(ProductModel.id == id).filter(ProductModel.status_id == 1).first()
    if product_1:
        return product_1
    elif product_4:
        return product_4
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El producto no existe")
    
#!OBTENER TODOS LOS PRODUCTOS CON EL ESTADO 4(STOCK) POR CATEGORIAS, MARCAS, RANGO DE PRECIOS, RANGO DE DESCUENTOS Y RANGO DE RANKING. NO ES NECESARIO QUE SE INGRESEN TODOS LOS PARAMETROS, SOLO LOS QUE SE DESEEN FILTRAR.
@catalogue.get('/obtenerProductosFiltros')
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