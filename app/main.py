from fastapi import APIRouter, FastAPI, status, HTTPException, responses
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.db import Session, engine, Base
#!PUBLIC ROUTES
from app.auth.login import auth
from app.routes.public.documents import documents
from app.routes.public.register_client import register_client
from app.routes.public.category import categories_pu
from app.routes.public.brand import brand_pu
from app.routes.public.model import model_pu
from app.routes.public.catalogue import catalogue
from app.routes.public.assembly import assemblies_pu
from app.routes.public.combo import combo_pu
#!PRIVATE ROUTES
from app.routes.private.profile import profile
from app.routes.private.roles import roles
from app.routes.private.role_privileges import role_privileges
from app.routes.private.register import register
from app.routes.private.supplier import supplier
from app.routes.private.category import categories_pr
from app.routes.private.brand import brand_pr
from app.routes.private.model import model_pr
from app.routes.private.supplier_categories import supplier_categories
from app.routes.private.client_review import client_review
from app.routes.private.products import products
from app.routes.private.assembly import assemblies_pr
from app.routes.private.combo import combo_pr
from app.routes.private.order import order
from app.routes.private.workers import workers
from app.routes.private.sale import sale
from app.routes.private.repaires_maintenance import repairs_maintenance

app = FastAPI(title=settings.PROJECT_NAME, description=settings.PROJECT_DESCRIPTION, docs_url=settings.DOCS_URL, redoc_url=settings.REDOC_URL, version=1.0)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.on_event("startup")
def startup():
    Session()
    print("Conectado a la base de datos")

@app.on_event("shutdown")
def shutdown():
    Session.close_all()
    print("Desconectado de la base de datos")

    

@app.get("/", include_in_schema=False)
async def root():
    return responses.RedirectResponse(url="/docs")

@app.get("/about", include_in_schema=False)
async def about():
    return HTTPException(status_code=status.HTTP_200_OK, detail="Rayotec API v1.0.0")

@app.get("/health", include_in_schema=False)
def health():
    if Session():
        return HTTPException(status_code=status.HTTP_200_OK, detail="API saludable")
    else:
        return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="API no saludable")

#! CREAR TABLAS
Base.metadata.create_all(bind=engine)

router_api = APIRouter(prefix="/api/v1")

routes = [
    (auth, "/public", "Autenticación"),
    (documents, "/public/documents", "Documentos"),
    (register_client, "/public/client", "Registro de clientes"),
    (categories_pu, "/public/categories", "Categorias"),
    (brand_pu, "/public/brand", "Marcas"),
    (model_pu, "/public/model", "Modelos"),
    (catalogue, "/public/catalogue", "Catalogo de Productos"),
    (assemblies_pu, "/public/assemblies", "Recomendaciones para Armar una Computadora"),
    (combo_pu, "/public/combo", "Combos de Productos"),
    (profile, "/private", "Perfil de usuario"),
    (roles, "/private/roles", "Roles Administrativos"),
    (role_privileges, "/private/role_privileges", "Privilegios de Roles"),
    (register, "/private/register", "Registro de Trabajadores y Administradores"),
    (workers, "/private/workers", "Trabajadores"),
    (supplier, "/private/supplier", "Proveedores"),
    (supplier_categories, "/private/supplier/categories", "Categorias de Proveedores"),
    (categories_pr, "/private/categories", "Categorias"),
    (brand_pr, "/private/brand", "Marcas"),
    (model_pr, "/private/model", "Modelos"),
    (client_review, "/private/client_review", "Reseñas de Clientes"),
    (products, "/private/products", "Inventario de Productos"),
    (assemblies_pr, "/private/assemblies", "Recomendaciones para Armar una Computadora"),
    (combo_pr, "/private/combo", "Combos de Productos"),
    (order, "/private/order", "Pedidos"),
    (sale, "/private/sale", "Ventas"),
    (repairs_maintenance, "/private/repairs_maintenance", "Reparaciones y Mantenimiento")
]

for route, prefix, tag in routes:
    router = APIRouter(prefix=prefix, tags=[tag])
    router.include_router(route)
    router_api.include_router(router)

app.include_router(router_api)