import streamlit as st

st.set_page_config(page_title="Valuation Deep Techs", page_icon="🔬", layout="wide")


st.title("Modelo de Valuation para Deep Techs 🚀")
st.write("Protótipo inicial - Iniciação Científica")

# Um exemplo de como as caixinhas vão ficar depois
st.sidebar.header("Parâmetros de Entrada")
investimento_inicial = st.sidebar.number_input("Investimento Inicial de P&D (R$)", min_value=0, step=100000)

st.write("O investimento inicial projetado é de:", investimento_inicial)