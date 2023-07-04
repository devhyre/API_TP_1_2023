from pydantic import BaseModel, validator
from datetime import datetime

class ClientReview(BaseModel):
    product_id: int
    review: str
    created_at: datetime
    punctuation: int
    
    @validator('product_id')
    def product_id_must_be_valid(cls, product_id):
        if product_id < 0:
            raise ValueError("El producto debe ser válido")
        return product_id
    
    @validator('review')
    def review_must_be_valid(cls, review):
        if len(review) > 255:
            raise ValueError("La reseña debe tener máximo 255 caracteres")
        if not all(char.isalnum() or char.isspace() or char in (",", ".", "?", "!") for char in review):
            raise ValueError("La reseña solo puede contener caracteres alfanuméricos, espacios, comas, puntos, signos de interrogación y exclamación")
        return review
    
    @validator('punctuation')
    def punctuation_must_be_valid(cls, punctuation):
        if punctuation < 0 or punctuation > 5:
            raise ValueError("La puntuación debe ser un número entero entre 0 y 5")
        return punctuation
    
class ClientReviewPost(ClientReview):
    pass

class ClientReviewPut(BaseModel):
    review: str
    punctuation: int

    @validator('review')
    def review_must_be_valid(cls, review):
        if len(review) > 255:
            raise ValueError("La reseña debe tener máximo 255 caracteres")
        if not all(char.isalnum() or char.isspace() or char in (",", ".", "?", "!") for char in review):
            raise ValueError("La reseña solo puede contener caracteres alfanuméricos, espacios, comas, puntos, signos de interrogación y exclamación")
        return review
    
    @validator('punctuation')
    def punctuation_must_be_valid(cls, punctuation):
        if punctuation < 0 or punctuation > 5:
            raise ValueError("La puntuación debe ser un número entero entre 0 y 5")
        return punctuation