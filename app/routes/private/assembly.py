from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user
from app.models.assembly import Assembly as AssemblyModel
from app.schemas.assembly import AssemblyPost, AssemblyPut

assemblies_pr = APIRouter()

#!OBTENER ASSEMBLIES
@assemblies_pr.get('/obtenerAssemblies', status_code=status.HTTP_200_OK)
async def obtener_assemblies(db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    User_type = list(user.keys())[0]
    if User_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        assemblies = db.query(AssemblyModel).all()
        return assemblies

#!CREAR ASSEMBLY
@assemblies_pr.post('/crearAssembly', status_code=status.HTTP_201_CREATED)
async def crear_assembly(assembly: AssemblyPost, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
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
        return assembly_db

#!ACTUALIZAR ASSEMBLY
@assemblies_pr.put('/actualizarAssembly/{id}', status_code=status.HTTP_202_ACCEPTED)
async def actualizar_assembly(id:int, assembly: AssemblyPut, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        assembly_db = db.query(AssemblyModel).filter(AssemblyModel.id == id).first()
        if assembly_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El assembly no existe')
        else:
            assembly_db.description = assembly.description
            db.commit()
            db.refresh(assembly_db)
            return assembly_db
        
#!ELIMINAR ASSEMBLY
@assemblies_pr.delete('/eliminarAssembly/{id}', status_code=status.HTTP_200_OK)
async def eliminar_assembly(id:int, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        assembly_db = db.query(AssemblyModel).filter(AssemblyModel.id == id).first()
        if assembly_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El assembly no existe')
        else:
            db.delete(assembly_db)
            db.commit()
            return {'message': 'Assembly eliminado'}