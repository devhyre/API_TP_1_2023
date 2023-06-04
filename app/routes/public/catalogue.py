from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.product import Product as ProductModel

catalogue = APIRouter()

#!OBTENER TODOS LOS PRODUCTOS CON EL ESTADO 4(STOCK)
@catalogue.get('/obtenerProductos')
async def obtener_productos(db: Session = Depends(get_db)):
    products = db.query(ProductModel).filter(ProductModel.status_id == 4).all()
    return products

#!OBTENER TODOS LOS PRODUCTOS CON EL ESTADO 4(STOCK) CON PAGINACION
@catalogue.get('/obtenerProductosPaginacion')
async def obtener_productos_paginacion(page:int, db: Session = Depends(get_db)):
    products = db.query(ProductModel).filter(ProductModel.status_id == 4).offset(page).limit(10).all()
    return products

#!OBTENER UN PRODUCTO CON EL ESTADO 4(STOCK)
@catalogue.get('/obtenerProducto/{id}')
async def obtener_producto(id:int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == id).filter(ProductModel.status_id == 4).first()
    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El producto no existe')
    else:
        return product
    
#!OBTENER TODOS LOS PRODUCTOS CON EL ESTADO 4(STOCK) POR CATEGORIAS, MARCAS, RANGO DE PRECIOS, RANGO DE DESCUENTOS Y RANGO DE RANKING
@catalogue.get('/obtenerProductosFiltros')
async def obtener_productos_filtros(category_id:int, brand_id:int, price_min:float, price_max:float, discount_min:float, discount_max:float, ranking_min:float, ranking_max:float, db: Session = Depends(get_db)):
    products = db.query(ProductModel).filter(ProductModel.status_id == 4).filter(ProductModel.category_id == category_id).filter(ProductModel.brand_id == brand_id).filter(ProductModel.price >= price_min).filter(ProductModel.price <= price_max).filter(ProductModel.discount >= discount_min).filter(ProductModel.discount <= discount_max).filter(ProductModel.ranking >= ranking_min).filter(ProductModel.ranking <= ranking_max).all()
    return products