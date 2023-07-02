from app.core.db import SessionLocal as Session

def startup():
    Session()
    print("Conectado a la base de datos")

def shutdown():
    Session.close_all()
    print("Desconectado de la base de datos")
