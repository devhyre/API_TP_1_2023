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
    filters = [
        (categoria_id, ProductModel.category_id),
        (marca_id, ProductModel.brand_id),
        (precio_min, ProductModel.price >= precio_min),
        (precio_max, ProductModel.price <= precio_max),
        (descuento_min, ProductModel.discount >= descuento_min),
        (descuento_max, ProductModel.discount <= descuento_max),
        (ranking_min, ProductModel.ranking >= ranking_min),
        (ranking_max, ProductModel.ranking <= ranking_max)
    ]

    query = db.query(ProductModel).filter(ProductModel.status_id == 4)

    for r in range(1, 9):  # Generate combinations of 1 to 8 filters
        for combination in itertools.combinations(filters, r):
            filters_to_apply = []
            for value, condition in combination:
                if value is not None:
                    filters_to_apply.append(condition)
            if filters_to_apply:
                query = query.filter(*filters_to_apply)

            products = query.all()
            # Process the resulting products here or return them

    # Handle the case where no filters are applied

    return []