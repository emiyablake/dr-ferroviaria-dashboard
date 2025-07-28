import streamlit as st
import pandas as pd
from . import session

from models import Patio, Terminal, Mercadoria, TerminalMercadoria, Base 


def run():
    st.title("Visualização dos Dados")

    st.subheader("Tabela: Pátio")
    patios = session.query(Patio).all()
    df_patio = pd.DataFrame([p.__dict__ for p in patios]).drop(columns=["_sa_instance_state"])
    st.dataframe(df_patio)

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