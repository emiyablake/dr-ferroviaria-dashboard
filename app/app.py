import streamlit as st
from views import showdataframe, showpatios

st.title("DR Ferroviaria")

menu = st.sidebar.title("Menu")
botao1 = st.sidebar.button("Visualizar dados")
botao2 = st.sidebar.button("Pátios")
botao3 = st.sidebar.button("Página 3")

if botao1:
    showdataframe.run()

elif botao2:
    showpatios.run()

elif botao3:
    st.subheader("Você selecionou a Página 3")
    st.write("Conteúdo da Página 3 aqui...")

else:
    st.write("Selecione uma opção no menu lateral.")
