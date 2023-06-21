from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.token import get_current_active_user
from app.models.combo import Combo as ComboBase
from app.models.detail_combo import DetailCombo as DetailComboBase

combo_pu = APIRouter()

#!COMBO
#GET ALL
#get id

#!COMBO DETAIL
#get id
