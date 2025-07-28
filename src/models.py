from sqlalchemy import (
    Column, Integer, String, Boolean, Float, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Ferrovia(Base):
    __tablename__ = "ferrovia"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    
    patios = relationship("Patio", back_populates="ferrovia")

class Bitola(Base):
    __tablename__ = "bitola"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    linhas = relationship("Linha", back_populates="bitola")
    entre_patios = relationship("EntrePatio", back_populates="bitola")

class Linha(Base):
    __tablename__ = "linha"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    idbitola = Column(Integer, ForeignKey("bitola.id"), nullable=False)

    bitola = relationship("Bitola", back_populates="linhas")
    entre_patios = relationship("EntrePatio", back_populates="linha")

class Patio(Base):
    __tablename__ = "patio"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    codigo = Column(String)
    em_operacao = Column(Boolean)
    auto_assistido = Column(Boolean)
    comprimento_util_desvio = Column(Integer)
    tempo_licenciamento = Column(Integer)
    idferrovia = Column(Integer, ForeignKey("ferrovia.id"), nullable=False)
    

    ferrovia = relationship("Ferrovia", back_populates="patios")
    terminal_mercadorias = relationship("TerminalMercadoria", back_populates="patio")
    entre_patios_a = relationship("EntrePatio", back_populates="patio_a", foreign_keys='EntrePatio.idpatio_a')
    entre_patios_b = relationship("EntrePatio", back_populates="patio_b", foreign_keys='EntrePatio.idpatio_b')

class EntrePatio(Base):
    __tablename__ = "entre_patio"
    id = Column(Integer, primary_key=True, autoincrement=True)
    idpatio_a = Column(Integer, ForeignKey("patio.id"), nullable=False)
    idpatio_b = Column(Integer, ForeignKey("patio.id"), nullable=False)
    idlinha = Column(Integer, ForeignKey("linha.id"), nullable=False)
    idbitola = Column(Integer, ForeignKey("bitola.id"), nullable=False)

    patio_a = relationship("Patio", foreign_keys=[idpatio_a], back_populates="entre_patios_a")
    patio_b = relationship("Patio", foreign_keys=[idpatio_b], back_populates="entre_patios_b")
    linha = relationship("Linha", back_populates="entre_patios")
    bitola = relationship("Bitola", back_populates="entre_patios")

class Mercadoria(Base):
    __tablename__ = "mercadoria"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    terminal_mercadorias = relationship("TerminalMercadoria", back_populates="mercadoria")

class Terminal(Base):
    __tablename__ = "terminal"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    terminal_mercadorias = relationship("TerminalMercadoria", back_populates="terminal")

class TerminalMercadoria(Base):
    __tablename__ = "terminal_mercadoria"
    id = Column(Integer, primary_key=True, autoincrement=True)
    idterminal = Column(Integer, ForeignKey("terminal.id"), nullable=False)
    idpatio = Column(Integer, ForeignKey("patio.id"), nullable=False)
    idmercadoria = Column(Integer, ForeignKey("mercadoria.id"), nullable=False)

    capacidade_vg_dia = Column(Float)
    capacidade_tu_dia = Column(Float)
    horas_funcionamento_dia = Column(Float)
    tempo_medio_carga_vg_h = Column(Float)
    tempo_medio_carga_tu_h = Column(Float)
    tempo_medio_descarga_vg_h = Column(Float)
    tempo_medio_descarga_tu_h = Column(Float)

    terminal = relationship("Terminal", back_populates="terminal_mercadorias")
    patio = relationship("Patio", back_populates="terminal_mercadorias")
    mercadoria = relationship("Mercadoria", back_populates="terminal_mercadorias")