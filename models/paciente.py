# CastorAgenda\models\paciente.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Paciente(Base):
    __tablename__ = 'pacientes'
    __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    sexo = Column(String(1), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(20), nullable=False)
    dt_nascimento = Column(TIMESTAMP, nullable=False)
    endereco = Column(String(2000), nullable=False)
    dt_criacao = Column(TIMESTAMP, server_default=func.now())
    dt_exclusao = Column(TIMESTAMP, nullable=True)