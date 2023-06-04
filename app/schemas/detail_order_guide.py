from pydantic import BaseModel, validator

class DetailOrderGuide(BaseModel):
    sn_id: str
    order_guide_id: int

    @validator('sn_id')
    def sn_id_must_be_valid(cls, sn_id):
        if len(sn_id) > 255:
            raise ValueError("El número de serie debe tener máximo 255 caracteres")
        if not all(char.isalnum() or char.isspace() or char in (",", ".", "?", "!") for char in sn_id):
            raise ValueError("El número de serie solo puede contener caracteres alfanuméricos, espacios, comas, puntos, signos de interrogación y exclamación")
        return sn_id
    
    @validator('order_guide_id')
    def order_guide_id_must_be_valid(cls, order_guide_id):
        if order_guide_id < 0:
            raise ValueError("La guía de remisión debe ser válida")
        return order_guide_id
    
class DetailOrderGuidePost(DetailOrderGuide):
    pass

class DetailOrderGuidePut(DetailOrderGuide):
    pass