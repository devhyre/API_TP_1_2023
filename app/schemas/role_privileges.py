from pydantic import BaseModel, validator

class RolePrivilege(BaseModel):
    role_id: int
    module_1: bool
    module_2: bool
    module_3: bool
    module_4: bool
    module_5: bool
    module_6: bool
    module_7: bool
    module_8: bool
    module_9: bool
    module_10: bool
    module_11: bool
    module_12: bool
    module_13: bool
    module_14: bool
    module_15: bool
    module_16: bool
    module_17: bool
    module_18: bool
    module_19: bool
    module_20: bool

    @validator('role_id')
    def role_id_must_be_valid(cls, role_id):
        if role_id < 0:
            raise ValueError("El rol debe ser válido")
        return role_id
    
class RolePrivilegePost(RolePrivilege):
    pass

class RolePrivilegePut(RolePrivilege):
    module_1: bool
    module_2: bool
    module_3: bool
    module_4: bool
    module_5: bool
    module_6: bool
    module_7: bool
    module_8: bool
    module_9: bool
    module_10: bool
    module_11: bool
    module_12: bool
    module_13: bool
    module_14: bool
    module_15: bool
    module_16: bool
    module_17: bool
    module_18: bool
    module_19: bool
    module_20: bool