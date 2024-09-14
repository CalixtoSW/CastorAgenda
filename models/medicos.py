# Castor_Agenda/models/medicos.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Medico(Base):
    __tablename__ = 'medicos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    dt_criacao = Column(TIMESTAMP, server_default=func.now())
    dt_exclusao = Column(TIMESTAMP, nullable=True)
