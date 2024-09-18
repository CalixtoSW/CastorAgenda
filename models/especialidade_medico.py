from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class EspecialidadeMedico(Base):
    __tablename__ = 'especialidade_medico'

    id = Column(Integer, primary_key=True, autoincrement=True)
    medico_id = Column(Integer, ForeignKey('medicos.id'), nullable=False)
    especialidade_id = Column(Integer, ForeignKey('especialidades.id'), nullable=False, default=1)
    dt_criacao = Column(TIMESTAMP, server_default=func.now())
    dt_exclusao = Column(TIMESTAMP, nullable=True)

    # Relacionamentos
    medico = relationship('Medico', back_populates='especialidades')
    especialidade = relationship('Especialidade', back_populates='medicos')

