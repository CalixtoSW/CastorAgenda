# CastorAgenda\models\agendamento.py
from sqlalchemy import Column, Integer, Date, Time, TIMESTAMP, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Agendamento(Base):
    __tablename__ = 'agendamentos'
    __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    sala_id = Column(Integer, ForeignKey('public.salas.id'), nullable=False)
    medico_id = Column(Integer, ForeignKey('public.medicos.id'), nullable=False)
    dt_criacao = Column(TIMESTAMP, server_default=func.now())
    dt_exclusao = Column(TIMESTAMP, nullable=True)
    paciente_id = Column(Integer, ForeignKey('public.pacientes.id'), nullable=False)
