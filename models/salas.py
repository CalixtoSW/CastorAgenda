# Castor_Agenda/models/salas.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Sala(Base):
    __tablename__ = 'salas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    numero = Column(String(10), nullable=False)
    capacidade = Column(Integer, nullable=False)
    dt_criacao = Column(TIMESTAMP, server_default=func.now())
    dt_exclusao = Column(TIMESTAMP, nullable=True)
