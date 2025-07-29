import streamlit as st
import pandas as pd
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from models import Patio, Terminal, Mercadoria, TerminalMercadoria, EntrePatio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'db', 'ferroviaria.db')

engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)
session = Session()


def run():
    st.title("Visualização dos Dados")

    st.subheader("Tabela: Pátio")
    patios = session.query(Patio).all()
    df_patio = pd.DataFrame([p.__dict__ for p in patios]).drop(columns=["_sa_instance_state"])
    st.dataframe(df_patio)

    st.subheader("Tabela: Entre_patios")
    entre_patio = session.query(EntrePatio).all()
    df_entrePatio = pd.DataFrame([p.__dict__ for p in entre_patio]).drop(columns=["_sa_instance_state"])
    st.dataframe(df_entrePatio)

    st.subheader("Tabela: Terminal")
    terminais = session.query(Terminal).all()
    df_terminal = pd.DataFrame([p.__dict__ for p in terminais]).drop(columns=["_sa_instance_state"])
    st.dataframe(df_terminal)

    st.subheader("Tabela: Mercadoria")
    mercadorias = session.query(Mercadoria).all()
    df_mercadoria = pd.DataFrame([p.__dict__ for p in mercadorias]).drop(columns=["_sa_instance_state"])
    st.dataframe(df_mercadoria)

    st.subheader("Tabela: Terminal_Mercadoria")
    terminal_mercadoria = session.query(TerminalMercadoria).all()
    df_terminalMercadoria = pd.DataFrame([p.__dict__ for p in terminal_mercadoria]).drop(columns=["_sa_instance_state"],  errors="ignore")
    st.dataframe(df_terminalMercadoria)

if __name__ == "__main__":
    run()