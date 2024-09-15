from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Especialidade(Base):
    __tablename__ = 'especialidades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    dt_criacao = Column(TIMESTAMP, server_default=func.now())
    dt_exclusao = Column(TIMESTAMP, nullable=True)

    # Relacionamento com médicos através da tabela associativa
    medicos = relationship(
        'Medico',
        secondary='especialidade_medico',
        back_populates='especialidades'
    )
