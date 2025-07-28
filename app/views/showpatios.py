import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from models import Patio, Terminal, Mercadoria, TerminalMercadoria, Base 

engine = create_engine("sqlite:///db/ferroviaria.db")
Session = sessionmaker(bind=engine)
session = Session()

def run():
    # Consulta os pátios do banco e transforma em DataFrame
    from models import Patio

    patios = session.query(Patio).all()
    df = pd.DataFrame([{
        'name': p.name,
        'em_operacao': p.em_operacao,
        'auto_assistido': p.auto_assistido
    } for p in patios])

    st.title("Análise dos Pátios")

    if df.empty:
        st.warning("Nenhum dado de pátios disponível.")
        return

    # Pizza: Em operação vs Não em operação
    operacao_counts = df['em_operacao'].value_counts()
    operacao_labels = ['Em Operação' if x else 'Não em Operação' for x in operacao_counts.index]

    st.subheader("Situação Operacional dos Pátios")
    st.pyplot(
        operacao_counts.plot.pie(
            labels=operacao_labels,
            autopct='%1.1f%%',
            startangle=90,
            legend=False
        ).figure
    )

    # Pizza: Auto assistido vs Não auto assistido
    auto_counts = df['auto_assistido'].value_counts()
    auto_labels = ['Auto Assistido' if x else 'Não Auto Assistido' for x in auto_counts.index]

    st.subheader("Pátios Auto Assistidos")
    st.pyplot(
        auto_counts.plot.pie(
            labels=auto_labels,
            autopct='%1.1f%%',
            startangle=90,
            legend=False
        ).figure
    )