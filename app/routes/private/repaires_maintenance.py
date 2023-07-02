from datetime import datetime
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.repairs_maintenance import RepairsMaintenancePost, RepairsMaintenancePut, RepairsMaintenanceStatusPut
from app.security.token import get_current_active_user
from app.models.repairs_maintenance import RepairsMaintenance as RepairsMaintenanceModel
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.models.worker import Worker as WorkerModel
from app.models.sn import SerialNumber as SerialNumberModel
from app.models.product import Product as ProductModel
from app.models.history_rm import HistoryRM as HistoryRMModel
from app.models.user import User as UserModel
from app.models.supplier import Supplier as SupplierModel
from app.models.brand import Brand as BrandModel
from app.models.model import Model as ModelModel
from app.models.combo import Combo as ComboModel
from app.models.detail_combo import DetailCombo as DetailComboModel

repairs_maintenance = APIRouter()

@repairs_maintenance.get('/admin/listadoServicios', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Listar servicios')
async def listar_tipos_servicios(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para este servicio')
    services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 7).all()
    services = sorted(services, key=lambda x: x.id_table)
    return [{'id': service.id_table, 'description': service.description} for service in services]

@repairs_maintenance.get('/admin/listadoTipos', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Listar tipos de servicios')
async def listar_tipos_servicios(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para este servicio')
    types_services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 9).all()
    types_services = sorted(types_services, key=lambda x: x.id_table)
    return [{'id': type_service.id_table, 'description': type_service.description} for type_service in types_services]

@repairs_maintenance.get('/admin/obtenerServicio/{id_table}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener tipo de servicio')
async def obtener_tipo_servicio(id_table: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para este servicio')
    service = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 7).filter(TableOfTablesModel.id_table == id_table).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El tipo de servicio con id {id_table} no existe")
    return {'id': service.id_table, 'description': service.description}

@repairs_maintenance.get('/admin/obtenerTipo/{id_table}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener tipo de servicio')
async def obtener_tipo_servicio(id_table: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para este servicio')
    type_service = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 9).filter(TableOfTablesModel.id_table == id_table).first()
    if not type_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El tipo de servicio con id {id_table} no existe")
    return {'id': type_service.id_table, 'description': type_service.description}

@repairs_maintenance.get('/admin/listadoEstados', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Listar estados de servicios')
async def listar_estados_servicios(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para este servicio')
    states_services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 8).all()
    states_services = sorted(states_services, key=lambda x: x.id_table)
    return [{'id': state_service.id_table, 'description': state_service.description} for state_service in states_services]

@repairs_maintenance.get('/admin/obtenerEstado/{id_table}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener estado de servicio')
async def obtener_estado_servicio(id_table: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para este servicio')
    state_service = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 8).filter(TableOfTablesModel.id_table == id_table).first()
    if not state_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El estado de servicio con id {id_table} no existe")
    return {'id': state_service.id_table, 'description': state_service.description}

@repairs_maintenance.get('/admin/listarReparaciones', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Listar servicios de reparaciones')
async def get_repairs(user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Reparaciones
        reparations_db = db.query(RepairsMaintenanceModel).filter(RepairsMaintenanceModel.service_id == 2).all()
        # Servicios
        services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 7).all()
        services = [{'id': service.id_table, 'description': service.description} for service in services]
        # Tipos de servicios
        types_services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 9).all()
        types_services = [{'id': type_service.id_table, 'description': type_service.description} for type_service in types_services]
        # Estados de servicios
        states_services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 8).all()
        states_services = [{'id': state_service.id_table, 'description': state_service.description} for state_service in states_services]
        # Estados de series
        states_series = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 6).all()
        states_series = [{'id': state_serie.id_table, 'description': state_serie.description} for state_serie in states_series]

        # Crear Json de respuesta
        response = []

        for reparation in reparations_db:
            # Obtener estados de productos
            states_products = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
            states_products = [{'id': state_product.id_table, 'description': state_product.description} for state_product in states_products]
            # Obtener categorias
            categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
            categories = [{'id': category.id_table, 'description': category.description} for category in categories]
            # Obtener servicio
            service = [service for service in services if service['id'] == reparation.service_id]
            # Obtener tipo de servicio
            type_service = [type_service for type_service in types_services if type_service['id'] == reparation.type_id]
            # Obtener historial de estados de servicio
            history_states_service = db.query(HistoryRMModel).filter(HistoryRMModel.repairs_maintenance_id == reparation.id).all()
            history_states_service_json = []
            for history_state_service in history_states_service:
                # Obtener estado de servicio
                state_service = [state_service for state_service in states_services if state_service['id'] == history_state_service.status_id]

                history_state_service_json = {
                    'id': history_state_service.id,
                    'state': state_service,
                    'date': history_state_service.date,
                    'description': history_state_service.description,
                    'note_diagnostic': history_state_service.note_diagnostic,
                    'note_repair': history_state_service.note_repair,
                }
                history_states_service_json.append(history_state_service_json)
            # Obtener trabajador
            worker = db.query(WorkerModel).filter(WorkerModel.id == reparation.worker_id).first()
            user_worker = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()
            # Obtener cliente
            user_client = db.query(UserModel).filter(UserModel.num_doc == reparation.client_doc).first()
            if user_client:
                user_client = {
                    'num_doc': user_client.num_doc,
                    'username': user_client.username,
                    'full_name': user_client.full_name,
                    'email': user_client.email,
                }
            else:
                user_client = {
                    'num_doc': reparation.clint_doc,
                    'username': '',
                    'full_name': reparation.client_name,
                    'email': reparation.client_email,
                }
            # Obtener serie
            serial = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == reparation.serial_number).first()
            if serial:
                # Obtener producto
                product = db.query(ProductModel).filter(ProductModel.id == serial.product_id).first()
                # Obtener marca
                brand = db.query(BrandModel).filter(BrandModel.id == product.brand_id).first()
                # Obtener modelo
                model = db.query(ModelModel).filter(ModelModel.id == product.model_id).first()
                # Obtener categoria
                category = [category for category in categories if category['id'] == product.category_id]
                # Obtener estado de producto
                state_product = [state_product for state_product in states_products if state_product['id'] == serial.state_product_id]
                # Obtener proveedor
                supplier = db.query(SupplierModel).filter(SupplierModel.num_doc == serial.supplier_id).first()
                # Obtener usuario
                user = db.query(UserModel).filter(UserModel.num_doc == serial.user_id).first()
                # Obtener estado de serie
                state_serie = [state_serie for state_serie in states_series if state_serie['id'] == serial.state_serie_id]
                # Buscar en combos el product_id
                combo = db.query(ComboModel).filter(ComboModel.id == serial.product_id).first()

                if combo:
                    # Obtener detalles de combo
                    combo_details = db.query(DetailComboModel).filter(DetailComboModel.combo_id == combo.id).all()

                    serial_data = {
                        'sn_id': serial.sn_id,
                        'product': {
                            'id': product.id,
                            'name': product.name,
                            'description': product.description,
                            'brand': brand,
                            'model': model,
                            'category': category,
                            'state_product': state_product,
                            'combo_details': [
                                {
                                    'id': detail_combo.id,
                                    'product': {
                                        'id': detail_combo.product_id,
                                        'name': db.query(ProductModel).filter(ProductModel.id == detail_combo.product_id).first().name,
                                    },
                                    'quantity': detail_combo.quantity,
                                } for detail_combo in combo_details
                            ],
                        },
                        'supplier': supplier,
                        'user': {
                            'num_doc': user.num_doc,
                            'full_name': user.full_name,
                            'email': user.email,
                            'is_active': user.is_active,
                        },
                        'state_serie': state_serie,
                        'entrance_at': serial.entrance_at,
                        'departure_at': serial.departure_at,
                    }
                else:
                    serial_data = {
                        'sn_id': serial.sn_id,
                        'product': {
                            'id': product.id,
                            'name': product.name,
                            'description': product.description,
                            'brand': brand,
                            'model': model,
                            'category': category,
                            'state_product': state_product,
                        },
                        'supplier': supplier,
                        'user': {
                            'num_doc': user.num_doc,
                            'full_name': user.full_name,
                            'email': user.email,
                            'is_active': user.is_active,
                        },
                        'state_serie': state_serie,
                        'entrance_at': serial.entrance_at,
                        'departure_at': serial.departure_at,
                    }
            else:
                serial_data = reparation.serial_number

            # Crear Json de reparación
            reparation_json = {
                'id': reparation.id,
                'service': service,
                'type_service': type_service,
                'entry_date': reparation.entry_date,
                'departure_date': reparation.departure_date,
                'client': user_client,
                'serial_number': serial_data,
                'description': reparation.description,
                'note_diagnostic': reparation.note_diagnostic,
                'note_repair': reparation.note_repair,
                'status': history_state_service_json,
                'discount': reparation.discount,
                'price': reparation.price,
                'total': reparation.total,
                'worker': {
                    'num_doc': user_worker.num_doc,
                    'username': user_worker.username,
                    'full_name': user_worker.full_name,
                    'email': user_worker.email,
                    'is_active': user_worker.is_active
                }
            }
            response.append(reparation_json)
        return response
    
@repairs_maintenance.get('/admin/listarMantenimientos', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Listar servicios de mantenimiento')
async def get_maintenance(user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Mantenimientos
        maintenances_db = db.query(RepairsMaintenanceModel).filter(RepairsMaintenanceModel.service_id == 1).all()
        # Servicios
        services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 7).all()
        services = [{'id': service.id_table, 'description': service.description} for service in services]
        # Tipos de servicios
        types_services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 9).all()
        types_services = [{'id': type_service.id_table, 'description': type_service.description} for type_service in types_services]
        # Estados de servicios
        states_services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 8).all()
        states_services = [{'id': state_service.id_table, 'description': state_service.description} for state_service in states_services]
        # Estados de series
        states_series = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 6).all()
        states_series = [{'id': state_serie.id_table, 'description': state_serie.description} for state_serie in states_series]

        # Crear Json de respuesta
        response = []

        for maintenance in maintenances_db:
            # Obtener estados de productos
            states_products = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
            states_products = [{'id': state_product.id_table, 'description': state_product.description} for state_product in states_products]
            # Obtener categorias
            categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
            categories = [{'id': category.id_table, 'description': category.description} for category in categories]
            # Obtener servicio
            service = [service for service in services if service['id'] == maintenance.service_id]
            # Obtener tipo de servicio
            type_service = [type_service for type_service in types_services if type_service['id'] == maintenance.type_id]
            # Obtener historial de estados de servicio
            history_states_service = db.query(HistoryRMModel).filter(HistoryRMModel.repairs_maintenance_id == maintenance.id).all()
            history_states_service_json = []
            for history_state_service in history_states_service:
                # Obtener estado de servicio
                state_service = [state_service for state_service in states_services if state_service['id'] == history_state_service.status_id]

                history_state_service_json = {
                    'id': history_state_service.id,
                    'state': state_service,
                    'date': history_state_service.date,
                    'description': history_state_service.description,
                    'note_diagnostic': history_state_service.note_diagnostic,
                    'note_repair': history_state_service.note_repair,
                }
                history_states_service_json.append(history_state_service_json)

            # Obtener trabajador
            worker = db.query(WorkerModel).filter(WorkerModel.id == maintenance.worker_id).first()
            user_worker = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()
            # Obtener cliente
            user_client = db.query(UserModel).filter(UserModel.num_doc == maintenance.client_doc).first()
            if user_client:
                user_client = {
                    'num_doc': user_client.num_doc,
                    'username': user_client.username,
                    'full_name': user_client.full_name,
                    'email': user_client.email,
                }
            else:
                user_client = {
                    'num_doc': maintenance.client_doc,
                    'username': '',
                    'full_name': maintenance.client_name,
                    'email': maintenance.client_email,
                }
            # Obtener serie
            serial = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == maintenance.serial_number).first()
            if serial:
                # Obtener producto
                product = db.query(ProductModel).filter(ProductModel.id == serial.product_id).first()
                # Obtener marca
                brand = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == product.brand_id).first()
                # Obtener modelo
                model = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == product.model_id).first()
                # Obtener categoria
                category = [category for category in categories if category['id'] == product.category_id]
                # Obtener estado de producto
                state_product = [state_product for state_product in states_products if state_product['id'] == product.status_id]
                # Obtener proveedor
                supplier = db.query(SupplierModel).filter(SupplierModel.num_doc == serial.supplier_id).first()
                # Obtener usuario
                user = db.query(UserModel).filter(UserModel.num_doc == serial.user_id).first()
                # Obtener estado de serie
                state_serie = [state_serie for state_serie in states_series if state_serie['id'] == serial.state_serie_id]
                # Buscar en combos el product_id
                combo = db.query(ComboModel).filter(ComboModel.id == serial.product_id).first()

                if combo:
                    # Obtener detalles de combo
                    combo_details = db.query(DetailComboModel).filter(DetailComboModel.combo_id == combo.id).all()

                    serial_data = {
                        'sn_id': serial.sn_id,
                        'product': {
                            'id': product.id,
                            'name': product.name,
                            'description': product.description,
                            'brand': brand,
                            'model': model,
                            'category': category,
                            'state_product': state_product,
                            'combo_details': [
                                {
                                    'id': detail_combo.id,
                                    'product': {
                                        'id': detail_combo.product_id,
                                        'name': db.query(ProductModel).filter(ProductModel.id == detail_combo.product_id).first().name,
                                    },
                                    'quantity': detail_combo.quantity,
                                } for detail_combo in combo_details
                            ],
                        },
                        'supplier': supplier,
                        'user': {
                            'num_doc': user.num_doc,
                            'full_name': user.full_name,
                            'email': user.email,
                            'is_active': user.is_active,
                        },
                        'state_serie': state_serie,
                        'entrance_at': serial.entrance_at,
                        'departure_at': serial.departure_at,
                    }
                else:
                    serial_data = {
                        'sn_id': serial.sn_id,
                        'product': {
                            'id': product.id,
                            'name': product.name,
                            'description': product.description,
                            'brand': brand,
                            'model': model,
                            'category': category,
                            'state_product': state_product,
                        },
                        'supplier': supplier,
                        'user': {
                            'num_doc': user.num_doc,
                            'full_name': user.full_name,
                            'email': user.email,
                            'is_active': user.is_active,
                        },
                        'state_serie': state_serie,
                        'entrance_at': serial.entrance_at,
                        'departure_at': serial.departure_at,
                    }
            else:
                serial_data = maintenance.serial_number

            # Crear Json de mantenimiento
            maintenance_json = {
                'id': maintenance.id,
                'service': service,
                'type_service': type_service,
                'entry_date': maintenance.entry_date,
                'departure_date': maintenance.departure_date,
                'client': user_client,
                'serial_number': serial_data,
                'description': maintenance.description,
                'note_diagnostic': maintenance.note_diagnostic,
                'note_repair': maintenance.note_repair,
                'status': history_states_service_json,
                'discount': maintenance.discount,
                'price': maintenance.price,
                'total': maintenance.total,
                'worker': {
                    'num_doc': user_worker.num_doc,
                    'username': user_worker.username,
                    'full_name': user_worker.full_name,
                    'email': user_worker.email,
                    'is_active': user_worker.is_active
                }
            }
            response.append(maintenance_json)
        return response
    
@repairs_maintenance.get('/admin/listarServiciosAsignados', status_code=status.HTTP_200_OK, name='TRABAJADOR - Listar servicios asignados')
async def get_servicios_asignados(user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    # Obtener servicios asignados
    servicios_asignados = db.query(RepairsMaintenanceModel).filter(RepairsMaintenanceModel.worker_id == user[user_type]['id']).all()
    if not servicios_asignados:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No tiene servicios asignados')
    # Mantenimientos
    maintenances_db = [mantenimiento for mantenimiento in servicios_asignados if mantenimiento.type_id == 1]
    # Reparaciones
    reparations_db = [reparacion for reparacion in servicios_asignados if reparacion.type_id == 2]
    # Servicios
    services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 7).all()
    services = [{'id': service.id_table, 'description': service.description} for service in services]
    # Tipos de servicios
    types_services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 9).all()
    types_services = [{'id': type_service.id_table, 'description': type_service.description} for type_service in types_services]
    # Estados de servicios
    states_services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 8).all()
    states_services = [{'id': state_service.id_table, 'description': state_service.description} for state_service in states_services]
    # Estados de series
    states_series = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 6).all()
    states_series = [{'id': state_serie.id_table, 'description': state_serie.description} for state_serie in states_series]

    # Crear Json de respuesta
    response = []
    # Crear Json de mantenimientos
    response_mantenimientos = []
    # Crear Json de reparaciones
    response_reparaciones = []

    for maintenance in maintenances_db:
        # Obtener estados de productos
        states_products = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
        states_products = [{'id': state_product.id_table, 'description': state_product.description} for state_product in states_products]
        # Obtener categorias
        categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
        categories = [{'id': category.id_table, 'description': category.description} for category in categories]
        # Obtener servicio
        service = [service for service in services if service['id'] == maintenance.service_id]
        # Obtener tipo de servicio
        type_service = [type_service for type_service in types_services if type_service['id'] == maintenance.type_id]
        # Obtener historial de estados de servicio
        history_states_service = db.query(HistoryRMModel).filter(HistoryRMModel.repairs_maintenance_id == maintenance.id).all()
        history_states_service_json = []
        for history_state_service in history_states_service:
            # Obtener estado de servicio
            state_service = [state_service for state_service in states_services if state_service['id'] == history_state_service.status_id]

            history_state_service_json = {
                'id': history_state_service.id,
                'state': state_service,
                'date': history_state_service.date,
                'description': history_state_service.description,
                'note_diagnostic': history_state_service.note_diagnostic,
                'note_repair': history_state_service.note_repair,
            }
            history_states_service_json.append(history_state_service_json)

        # Obtener trabajador
        worker = db.query(WorkerModel).filter(WorkerModel.id == maintenance.worker_id).first()
        user_worker = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()
        # Obtener cliente
        user_client = db.query(UserModel).filter(UserModel.num_doc == maintenance.client_doc).first()
        if user_client:
            user_client = {
                'num_doc': user_client.num_doc,
                'username': user_client.username,
                'full_name': user_client.full_name,
                'email': user_client.email,
            }
        else:
            user_client = {
                'num_doc': maintenance.client_doc,
                'username': '',
                'full_name': maintenance.client_name,
                'email': maintenance.client_email,
            }
        # Obtener serie
        serial = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == maintenance.serial_number).first()
        if serial:
            # Obtener producto
            product = db.query(ProductModel).filter(ProductModel.id == serial.product_id).first()
            # Obtener marca
            brand = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == product.brand_id).first()
            # Obtener modelo
            model = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == product.model_id).first()
            # Obtener categoria
            category = [category for category in categories if category['id'] == product.category_id]
            # Obtener estado de producto
            state_product = [state_product for state_product in states_products if state_product['id'] == product.status_id]
            # Obtener proveedor
            supplier = db.query(SupplierModel).filter(SupplierModel.num_doc == serial.supplier_id).first()
            # Obtener usuario
            user = db.query(UserModel).filter(UserModel.num_doc == serial.user_id).first()
            # Obtener estado de serie
            state_serie = [state_serie for state_serie in states_series if state_serie['id'] == serial.state_serie_id]
            # Buscar en combos el product_id
            combo = db.query(ComboModel).filter(ComboModel.id == serial.product_id).first()

            if combo:
                # Obtener detalles de combo
                combo_details = db.query(DetailComboModel).filter(DetailComboModel.combo_id == combo.id).all()

                serial_data = {
                    'sn_id': serial.sn_id,
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'brand': brand,
                        'model': model,
                        'category': category,
                        'state_product': state_product,
                        'combo_details': [
                            {
                                'id': detail_combo.id,
                                'product': {
                                    'id': detail_combo.product_id,
                                    'name': db.query(ProductModel).filter(ProductModel.id == detail_combo.product_id).first().name,
                                },
                                'quantity': detail_combo.quantity,
                            } for detail_combo in combo_details
                        ],
                    },
                    'supplier': supplier,
                    'user': {
                        'num_doc': user.num_doc,
                        'full_name': user.full_name,
                        'email': user.email,
                        'is_active': user.is_active,
                    },
                    'state_serie': state_serie,
                    'entrance_at': serial.entrance_at,
                    'departure_at': serial.departure_at,
                }
            else:
                serial_data = {
                    'sn_id': serial.sn_id,
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'brand': brand,
                        'model': model,
                        'category': category,
                        'state_product': state_product,
                    },
                    'supplier': supplier,
                    'user': {
                        'num_doc': user.num_doc,
                        'full_name': user.full_name,
                        'email': user.email,
                        'is_active': user.is_active,
                    },
                    'state_serie': state_serie,
                    'entrance_at': serial.entrance_at,
                    'departure_at': serial.departure_at,
                }
        else:
            serial_data = maintenance.serial_number

        # Crear Json de mantenimiento
        maintenance_json = {
            'id': maintenance.id,
            'service': service,
            'type_service': type_service,
            'entry_date': maintenance.entry_date,
            'departure_date': maintenance.departure_date,
            'client': user_client,
            'serial_number': serial_data,
            'description': maintenance.description,
            'note_diagnostic': maintenance.note_diagnostic,
            'note_repair': maintenance.note_repair,
            'status': history_state_service_json,
            'discount': maintenance.discount,
            'price': maintenance.price,
            'total': maintenance.total,
            'worker': {
                'num_doc': user_worker.num_doc,
                'username': user_worker.username,
                'full_name': user_worker.full_name,
                'email': user_worker.email,
                'is_active': user_worker.is_active
            }
        }
        # Agregar mantenimiento a la lista
        response_mantenimientos.append(maintenance_json)
    
    for reparation in reparations_db:
        # Obtener estados de productos
        states_products = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
        states_products = [{'id': state_product.id_table, 'description': state_product.description} for state_product in states_products]
        # Obtener categorias
        categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
        categories = [{'id': category.id_table, 'description': category.description} for category in categories]
        # Obtener servicio
        service = [service for service in services if service['id'] == reparation.service_id]
        # Obtener tipo de servicio
        type_service = [type_service for type_service in types_services if type_service['id'] == reparation.type_id]
        # Obtener historial de estados de servicio
        history_states_service = db.query(HistoryRMModel).filter(HistoryRMModel.repairs_maintenance_id == reparation.id).all()
        history_states_service_json = []
        for history_state_service in history_states_service:
            # Obtener estado de servicio
            state_service = [state_service for state_service in states_services if state_service['id'] == history_state_service.status_id]

            history_state_service_json = {
                'id': history_state_service.id,
                'state': state_service,
                'date': history_state_service.date,
                'description': history_state_service.description,
                'note_diagnostic': history_state_service.note_diagnostic,
                'note_repair': history_state_service.note_repair,
            }
            history_states_service_json.append(history_state_service_json)

        # Obtener trabajador
        worker = db.query(WorkerModel).filter(WorkerModel.id == reparation.worker_id).first()
        user_worker = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()
        # Obtener cliente
        user_client = db.query(UserModel).filter(UserModel.num_doc == reparation.client_doc).first()
        if user_client:
            user_client = {
                'num_doc': user_client.num_doc,
                'username': user_client.username,
                'full_name': user_client.full_name,
                'email': user_client.email,
            }
        else:
            user_client = {
                'num_doc': reparation.clint_doc,
                'username': '',
                'full_name': reparation.client_name,
                'email': reparation.client_email,
            }
        # Obtener serie
        serial = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == reparation.serial_number).first()
        if serial:
            # Obtener producto
            product = db.query(ProductModel).filter(ProductModel.id == serial.product_id).first()
            # Obtener marca
            brand = db.query(BrandModel).filter(BrandModel.id == product.brand_id).first()
            # Obtener modelo
            model = db.query(ModelModel).filter(ModelModel.id == product.model_id).first()
            # Obtener categoria
            category = [category for category in categories if category['id'] == product.category_id]
            # Obtener estado de producto
            state_product = [state_product for state_product in states_products if state_product['id'] == product.status_id]
            # Obtener proveedor
            supplier = db.query(SupplierModel).filter(SupplierModel.num_doc == serial.supplier_id).first()
            # Obtener usuario
            user = db.query(UserModel).filter(UserModel.num_doc == serial.user_id).first()
            # Obtener estado de serie
            state_serie = [state_serie for state_serie in states_series if state_serie['id'] == serial.state_serie_id]
               # Buscar en combos el product_id
            combo = db.query(ComboModel).filter(ComboModel.id == serial.product_id).first()

            if combo:
                # Obtener detalles de combo
                combo_details = db.query(DetailComboModel).filter(DetailComboModel.combo_id == combo.id).all()

                serial_data = {
                    'sn_id': serial.sn_id,
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'brand': brand,
                        'model': model,
                        'category': category,
                        'state_product': state_product,
                        'combo_details': [
                            {
                                'id': detail_combo.id,
                                'product': {
                                    'id': detail_combo.product_id,
                                    'name': db.query(ProductModel).filter(ProductModel.id == detail_combo.product_id).first().name,
                                },
                                'quantity': detail_combo.quantity,
                            } for detail_combo in combo_details
                        ],
                    },
                    'supplier': supplier,
                    'user': {
                        'num_doc': user.num_doc,
                        'full_name': user.full_name,
                        'email': user.email,
                        'is_active': user.is_active,
                    },
                    'state_serie': state_serie,
                    'entrance_at': serial.entrance_at,
                    'departure_at': serial.departure_at,
                }
            else:
                serial_data = {
                    'sn_id': serial.sn_id,
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'brand': brand,
                        'model': model,
                        'category': category,
                        'state_product': state_product,
                    },
                    'supplier': supplier,
                    'user': {
                        'num_doc': user.num_doc,
                        'full_name': user.full_name,
                        'email': user.email,
                        'is_active': user.is_active,
                    },
                    'state_serie': state_serie,
                    'entrance_at': serial.entrance_at,
                    'departure_at': serial.departure_at,
                }
        else:
            serial_data = reparation.serial_number

        # Crear Json de reparación
        reparation_json = {
            'id': reparation.id,
            'service': service,
            'type_service': type_service,
            'entry_date': reparation.entry_date,
            'departure_date': reparation.departure_date,
            'client': user_client,
            'serial_number': serial_data,
            'description': reparation.description,
            'note_diagnostic': reparation.note_diagnostic,
            'note_repair': reparation.note_repair,
            'status': history_states_service_json,
            'discount': reparation.discount,
            'price': reparation.price,
            'total': reparation.total,
            'worker': {
                'num_doc': user_worker.num_doc,
                'username': user_worker.username,
                'full_name': user_worker.full_name,
                'email': user_worker.email,
                'is_active': user_worker.is_active
            }
        }
        response_reparaciones.append(reparation_json)
    # Obtener todos los servicios
    response = {
        'reparaciones': response_reparaciones,
        'total_reparacion': len(response_reparaciones),
        'mantenimientos': response_mantenimientos,
        'total_mantenimiento': len(response_mantenimientos),
    }
    return response

@repairs_maintenance.get('/admin/obtenerServicioMR/{id}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener el servicio de mantenimiento o reparación por id')
async def get_service(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    # Obtener mantenimiento o reparación
    serivicio = db.query(RepairsMaintenanceModel).filter(RepairsMaintenanceModel.id == id).first()
    if not serivicio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El servicio: {id} no existe")
    # Obtener servicio
    services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 7).all()
    services = [{'id': service.id_table, 'description': service.description} for service in services]
    service = [service for service in services if service['id'] == serivicio.service_id]
    # Obtener tipo de servicio
    type_services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 9).all()
    type_services = [{'id': type_service.id_table, 'description': type_service.description} for type_service in type_services]
    type_service = [type_service for type_service in type_services if type_service['id'] == serivicio.type_id]
    # Estados de servicios
    states_services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 8).all()
    states_services = [{'id': state_service.id_table, 'description': state_service.description} for state_service in states_services]
    # Estados de series
    states_series = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 6).all()
    states_series = [{'id': state_serie.id_table, 'description': state_serie.description} for state_serie in states_series]
    # Obtener cliente
    user_client = db.query(UserModel).filter(UserModel.num_doc == serivicio.client_doc).first()
    if not user_client:
        user_client = {
            'client_doc': serivicio.client_doc,
            'full_name': serivicio.client_name,
            'email': serivicio.client_email
        }
    else:
        user_client = {
            'client_doc': user_client.num_doc,
            'full_name': user_client.full_name,
            'email': user_client.email
        }
    # Obtener estados de productos
    states_products = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
    states_products = [{'id': state_product.id_table, 'description': state_product.description} for state_product in states_products]
    # Obtener categorias
    categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
    categories = [{'id': category.id_table, 'description': category.description} for category in categories]
    # Obtener serial
    serial = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == serivicio.serial_number).first()
    if serial:
        # Obtener producto
        product = db.query(ProductModel).filter(ProductModel.id == serial.product_id).first()
        # Obtener marca
        brand = db.query(BrandModel).filter(BrandModel.id == product.brand_id).first()
        # Obtener modelo
        model = db.query(ModelModel).filter(ModelModel.id == product.model_id).first()
        # Obtener categoria
        category = [category for category in categories if category['id'] == product.category_id]
        # Obtener estado de producto
        state_product = [state_product for state_product in states_products if state_product['id'] == product.status_id]
        # Obtener proveedor
        supplier = db.query(SupplierModel).filter(SupplierModel.id == serial.supplier_id).first()
        # Obtener usuario
        user = db.query(UserModel).filter(UserModel.num_doc == serial.user_id).first()
        # Obtener estado de serie
        state_serie = [state_serie for state_serie in states_series if state_serie['id'] == serial.state_serie_id]
        # Buscar en combos el product_id
        combo = db.query(ComboModel).filter(ComboModel.id == serial.product_id).first()
        if combo:
            # Obtener detalles de combo
            combo_details = db.query(DetailComboModel).filter(DetailComboModel.combo_id == combo.id).all()

            serial_data = {
                'sn_id': serial.sn_id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'brand': brand,
                    'model': model,
                    'category': category,
                    'state_product': state_product,
                    'combo_details': [
                        {
                            'id': detail_combo.id,
                            'product': {
                                'id': detail_combo.product_id,
                                'name': db.query(ProductModel).filter(ProductModel.id == detail_combo.product_id).first().name,
                            },
                            'quantity': detail_combo.quantity,
                        } for detail_combo in combo_details
                    ],
                },
                'supplier': supplier,
                'user': {
                    'num_doc': user.num_doc,
                    'full_name': user.full_name,
                    'email': user.email,
                    'is_active': user.is_active,
                },
                'state_serie': state_serie,
                'entrance_at': serial.entrance_at,
                'departure_at': serial.departure_at,
            }
        else:
            serial_data = {
                'sn_id': serial.sn_id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'brand': brand,
                    'model': model,
                    'category': category,
                    'state_product': state_product,
                },
                'supplier': supplier,
                'user': {
                    'num_doc': user.num_doc,
                    'full_name': user.full_name,
                    'email': user.email,
                    'is_active': user.is_active,
                },
                'state_serie': state_serie,
                'entrance_at': serial.entrance_at,
                'departure_at': serial.departure_at,
            }
    # Obtener historial de estados de servicio
    history_states_service = db.query(HistoryRMModel).filter(HistoryRMModel.repairs_maintenance_id == service.id).all()
    history_states_service_json = []
    for history_state_service in history_states_service:
        # Obtener estado de servicio
        state_service = [state_service for state_service in states_services if state_service['id'] == history_state_service.status_id]

        history_state_service_json = {
            'id': history_state_service.id,
            'state': state_service,
            'date': history_state_service.date,
            'description': history_state_service.description,
            'note_diagnostic': history_state_service.note_diagnostic,
            'note_repair': history_state_service.note_repair,
        }
        history_states_service_json.append(history_state_service_json)
    # Obtener trabajador
    worker = db.query(WorkerModel).filter(WorkerModel.id == service.worker_id).first()
    user_worker = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()

    # Crear Json de Servicio
    service_json = {
        'id': serivicio.id,
        'service': service,
        'type_service': type_service,
        'entry_date': serivicio.entry_date,
        'departure_date': serivicio.departure_date,
        'client': user_client,
        'serial_number': serial_data,
        'description': serivicio.description,
        'note_diagnostic': serivicio.note_diagnostic,
        'note_repair': serivicio.note_repair,
        'status': history_state_service_json,
        'discount': serivicio.discount,
        'price': serivicio.price,
        'total': serivicio.total,
        'worker': {
            'num_doc': user_worker.num_doc,
            'username': user_worker.username,
            'full_name': user_worker.full_name,
            'email': user_worker.email,
            'is_active': user_worker.is_active,
        }
    }
    return service_json

@repairs_maintenance.get('/admin/validarGarantiaSerial/{numero_serie}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Validar serial')
async def get_serial(numero_serie: str, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    # Obtener serial
    serial = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == numero_serie).first()
    if not serial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El serial: {numero_serie} no existe en la base de datos")
    # Obtener producto
    product = db.query(ProductModel).filter(ProductModel.id == serial.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El producto: {serial.product_id} no existe en la base de datos")
    # Tipos de servicios
    types_services = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 9).all()
    types_services = [{'id': type_service.id_table, 'description': type_service.description} for type_service in types_services]
    # Reponse
    response = []
    # Validar garantía
    fecha_actual = datetime.now()
    fecha_compra = serial.departure_at
    if fecha_compra is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El serial: {numero_serie} no tiene fecha de compra")
    # Agregarle los meses de garantia a la fecha de compra
    fecha_garantia = fecha_compra + relativedelta(months=+product.warranty)
    if fecha_actual >= fecha_garantia:
        # Obtener servicio
        service = [service for service in types_services if service['id'] == 1]
        garantia_json = {
            'tipo': service,
            'fecha_compra': fecha_compra,
            'grantia_producto': product.warranty,
            'fecha_max_garantia': fecha_garantia,
            'fecha_actual': fecha_actual,
            'estado': 'Vencida'
        }
        response.append(garantia_json)
    else:
        # Obtener servicio
        service = [service for service in types_services if service['id'] == 2]
        garantia_json = {
            'tipo': service,
            'fecha_compra': fecha_compra,
            'grantia_producto': product.warranty,
            'fecha_max_garantia': fecha_garantia,
            'fecha_actual': fecha_actual,
            'estado': 'Vigente'
        }
        response.append(garantia_json)
    return response

@repairs_maintenance.post('/admin/registrarReparacionMantenimiento', status_code=status.HTTP_201_CREATED, name='TRABAJADOR - Registrar reparación o mantenimiento')
async def post_repairs_maintenance(repairs_maintenance: RepairsMaintenancePost, user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type != 'worker':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    
    # Crear Servicio
    db_service = RepairsMaintenanceModel(
        service_id=repairs_maintenance.service_id,
        type_id=repairs_maintenance.type_id,
        entry_date=repairs_maintenance.entry_date,
        departure_date=None,
        client_doc=repairs_maintenance.client_doc,
        client_name=repairs_maintenance.client_name,
        client_email=repairs_maintenance.client_email,
        serial_number=repairs_maintenance.serial_number,
        description=repairs_maintenance.description,
        note_diagnostic=repairs_maintenance.note_diagnostic,
        note_repair=repairs_maintenance.note_repair,
        discount=repairs_maintenance.discount,
        price=repairs_maintenance.price,
        total= repairs_maintenance.price - (repairs_maintenance.price * (repairs_maintenance.discount / 100)),
        worker_id=user[user_type]['id']
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    # Crear Historial de Servicio
    db_service_history = HistoryRMModel(
        status_id=repairs_maintenance.status_id,
        date = datetime.now(),
        description = repairs_maintenance.description,
        note_diagnostic = repairs_maintenance.note_diagnostic,
        note_repair = repairs_maintenance.note_repair,
        repairs_maintenance_id = db_service.id
    )
    db.add(db_service_history)
    db.commit()
    db.refresh(db_service_history)

    return db_service


@repairs_maintenance.put('/admin/actualizarContenidoServicio/{id}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Actualizar contenido de reparación o mantenimiento')
async def put_repairs_maintenance(id: int, repairs_maintenance: RepairsMaintenancePut, user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    # Obtener servicio
    db_service = db.query(RepairsMaintenanceModel).filter(RepairsMaintenanceModel.id == id).first()
    if not db_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El servicio: {id} no existe")
    # Actualizar servicio
    db_service.description = repairs_maintenance.description
    db_service.note_diagnostic = repairs_maintenance.note_diagnostic
    db_service.note_repair = repairs_maintenance.note_repair

    db.commit()
    db.refresh(db_service)
    return db_service

@repairs_maintenance.put('/admin/actualizarEstadoServicio/{id}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Actualizar estado de reparación o mantenimiento')
async def put_status_repairs_maintenance(id: int, repairs_maintenance: RepairsMaintenanceStatusPut, user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    # Obtener servicio
    db_service = db.query(RepairsMaintenanceModel).filter(RepairsMaintenanceModel.id == id).first()
    if not db_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El servicio: {id} no existe")
    # Crear Historial de Servicio
    db_service_history = HistoryRMModel(
        status_id=repairs_maintenance.status_id,
        date = datetime.now(),
        description = repairs_maintenance.description,
        note_diagnostic = repairs_maintenance.note_diagnostic,
        note_repair = repairs_maintenance.note_repair,
        repairs_maintenance_id = db_service.id
    )
    db.add(db_service_history)
    db.commit()
    db.refresh(db_service_history)
    # Si el estado es 4 actualiza departure_date
    if repairs_maintenance.status_id == 4:
        db_service.departure_date = datetime.now()
        db.commit()
        db.refresh(db_service)
    return db_service_history