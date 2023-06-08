from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.repairs_maintenance import RepairsMaintenancePost, RepairsMaintenancePut
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user
from app.models.repairs_maintenance import RepairsMaintenance as RepairsMaintenanceModel
from app.models.table_of_tables import TableOfTables as TableOfTablesModel

repairs_maintenance = APIRouter()

@repairs_maintenance.get('/listadoTiposServicios', status_code=status.HTTP_200_OK)
async def listar_tipos_servicios(db: Session = Depends(get_db)):
    types_services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 7).all()
    types_services = sorted(types_services, key=lambda x: x.id_table)
    return [{'id': type_service.id_table, 'description': type_service.description} for type_service in types_services]

@repairs_maintenance.get('/obtenerTipoServicio/{id_table}')
async def obtener_tipo_servicio(id_table: int, db: Session = Depends(get_db)):
    type_service = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 7).filter(TableOfTablesModel.id_table == id_table).first()
    if not type_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El tipo de servicio con id {id_table} no existe")
    return {'id': type_service.id_table, 'description': type_service.description}

@repairs_maintenance.get('/listadoEstadosServicios', status_code=status.HTTP_200_OK)
async def listar_estados_servicios(db: Session = Depends(get_db)):
    states_services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 8).all()
    states_services = sorted(states_services, key=lambda x: x.id_table)
    return [{'id': state_service.id_table, 'description': state_service.description} for state_service in states_services]

@repairs_maintenance.get('/obtenerEstadoServicio/{id_table}')
async def obtener_estado_servicio(id_table: int, db: Session = Depends(get_db)):
    state_service = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 8).filter(TableOfTablesModel.id_table == id_table).first()
    if not state_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El estado de servicio con id {id_table} no existe")
    return {'id': state_service.id_table, 'description': state_service.description}

@repairs_maintenance.get('/listarReparaciones', status_code=status.HTTP_200_OK)
async def get_repairs_maintenance(user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        list_repairs_maintenance = db.query(RepairsMaintenanceModel).filter(RepairsMaintenanceModel.type_service_id == 3 or RepairsMaintenanceModel.type_service_id == 4).all()
        return list_repairs_maintenance
    
@repairs_maintenance.get('/listarMantenimientos', status_code=status.HTTP_200_OK)
async def get_maintenance(user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        list_repairs_maintenance = db.query(RepairsMaintenanceModel).filter(RepairsMaintenanceModel.type_service_id == 1 or RepairsMaintenanceModel.type_service_id == 2).all()
        return list_repairs_maintenance
    
@repairs_maintenance.get('/listarReparacionesMantenimientos', status_code=status.HTTP_200_OK)
async def get_repairs_maintenance(user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        list_repairs_maintenance = db.query(RepairsMaintenanceModel).all()
        return list_repairs_maintenance
    
@repairs_maintenance.get('/listarReparacionesMantenimientosTrabajadorAsignado/{worker_id}', status_code=status.HTTP_200_OK)
async def get_repairs_maintenance(worker_id: int, user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        list_repairs_maintenance = db.query(RepairsMaintenanceModel).filter(RepairsMaintenanceModel.worker_id == worker_id).all()
        return list_repairs_maintenance
    
@repairs_maintenance.post('/registrarReparacionMantenimiento', status_code=status.HTTP_201_CREATED)
async def post_repairs_maintenance(repairs_maintenance: RepairsMaintenancePost, user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        db_repairs_maintenance = RepairsMaintenanceModel(
            type_service_id = repairs_maintenance.type_service_id,
            serial_number_id = repairs_maintenance.serial_number_id,
            created_at = datetime.now(),
            worker_id = repairs_maintenance.worker_id,
            description = repairs_maintenance.description,
            note = repairs_maintenance.note,
            status_id = repairs_maintenance.status_id,
            discount = repairs_maintenance.discount,
            total = repairs_maintenance.total * (1 - repairs_maintenance.discount / 100)
        )

@repairs_maintenance.put('/actualizarReparacionMantenimiento/{id}', status_code=status.HTTP_200_OK)
async def put_repairs_maintenance(id: int, repairs_maintenance: RepairsMaintenancePut, user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        #!ACTUALIZAR DESCRIPTION, NOTE, STATUS_ID, DISCOUNT, TOTAL
        db_repairs_maintenance = db.query(RepairsMaintenanceModel).filter(RepairsMaintenanceModel.id == id).first()
        if db_repairs_maintenance is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Reparación o mantenimiento no encontrado')
        else:
            db_repairs_maintenance.description = repairs_maintenance.description
            db_repairs_maintenance.note = repairs_maintenance.note
            db_repairs_maintenance.status_id = repairs_maintenance.status_id
            db_repairs_maintenance.discount = repairs_maintenance.discount
            db_repairs_maintenance.total = repairs_maintenance.total * (1 - repairs_maintenance.discount / 100)
            db.commit()
            return db_repairs_maintenance
        
        