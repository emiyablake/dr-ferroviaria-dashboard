import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from models import TerminalMercadoria, Terminal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'db', 'ferroviaria.db')

engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)
session = Session()

def run():
    st.title("Tempo Médio de Carga e Descarga por Terminal")

    dados = (
            session.query(
                Terminal.name,
                TerminalMercadoria.tempo_medio_carga_vg_h,
                TerminalMercadoria.tempo_medio_carga_tu_h,
                TerminalMercadoria.tempo_medio_descarga_vg_h,
                TerminalMercadoria.tempo_medio_descarga_tu_h
            )
            .join(Terminal, Terminal.id == TerminalMercadoria.idterminal)
            .all()
        )

    if not dados:
        st.warning("Nenhum dado de tempo médio encontrado.")
        return
    # Cria DataFrame
    df = pd.DataFrame(dados, columns=[
        "Terminal",
        "Carga VG (h)",
        "Carga TU (h)",
        "Descarga VG (h)",
        "Descarga TU (h)"
    ])

    df_grouped = df.groupby("Terminal").mean(numeric_only=True).reset_index()

    terminais_disponiveis = df_grouped["Terminal"].unique().tolist()
    terminais_selecionados = st.multiselect(
        "Selecione os terminais que deseja visualizar:",
        options=terminais_disponiveis,
        default=terminais_disponiveis[:10]  # mostra os 10 primeiros por padrão
    )

    if not terminais_selecionados:
        st.info("Selecione pelo menos um terminal para visualizar o gráfico.")
        return

    df_filtrado = df_grouped[df_grouped["Terminal"].isin(terminais_selecionados)]

    st.subheader("Tempo Médio de Carga e Descarga por Tipo e Terminal")
    fig, ax = plt.subplots(figsize=(12, 6))
    df_filtrado.set_index("Terminal").plot(kind="bar", ax=ax)
    ax.set_ylabel("Tempo Médio (horas)")
    ax.set_title("Tempo Médio de Carga/Descarga (VG/TU) por Terminal")
    ax.legend(title="Operação")
    st.pyplot(fig)

if __name__ == "__main__":
    run()