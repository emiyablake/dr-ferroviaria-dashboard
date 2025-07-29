import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from models import Patio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'db', 'ferroviaria.db')

engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)
session = Session()

def run():

    patios = session.query(Patio).all()
    df = pd.DataFrame([{
        'name': p.name,
        'em_operacao': p.em_operacao,
        'auto_assistido': p.auto_assistido
    } for p in patios])

    st.title("Situação Operacional dos Pátios")

    if df.empty:
        st.warning("Nenhum dado de pátios disponível.")
        return

    operacao_counts = df['em_operacao'].value_counts()
    operacao_labels = ['Em Operação' if x else 'Não em Operação' for x in operacao_counts.index]

    fig1, ax1 = plt.subplots(figsize=(5,5), facecolor='none')
    operacao_counts.plot.pie(
        labels=operacao_labels,
        autopct='%1.1f%%',
        startangle=90,
        legend=False,
        ax=ax1,
        textprops={'color':'white'}
    )
    ax1.set_facecolor('none')
    st.pyplot(fig1)

    auto_counts = df['auto_assistido'].value_counts()
    auto_labels = ['Auto Assistido' if x else 'Não Auto Assistido' for x in auto_counts.index]

    st.subheader("Pátios Auto Assistidos")
    fig2, ax2 = plt.subplots(figsize=(5,5), facecolor='none')
    auto_counts.plot.pie(
        labels=auto_labels,
        autopct='%1.1f%%',
        startangle=90,
        legend=False,
        ax=ax2,
        textprops={'color':'white'}
    )
    ax2.set_facecolor('none')
    st.pyplot(fig2)

if __name__ == "__main__":
    run()