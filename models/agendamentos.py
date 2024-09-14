# Castor_Agenda/models/agendamentos.py
from sqlalchemy import Column, Integer, Date, Time, TIMESTAMP, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Agendamento(Base):
    __tablename__ = 'agendamentos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    sala_id = Column(Integer, ForeignKey("salas.id"))
    medico_id = Column(Integer, ForeignKey("medicos.id"))
    dt_criacao = Column(TIMESTAMP, server_default=func.now())
    dt_exclusao = Column(TIMESTAMP, nullable=True)
