import streamlit as st

# --- 1. CONFIGURAÇÃO GERAL ---
st.set_page_config(page_title="Valuation DCF - Deep Tech", page_icon="🔬", layout="wide")
st.title("Valuation de Deep Techs")
st.markdown("Modelo de Fluxo de Caixa Descontado (DCF) focado em startups de base tecnológica.")
st.divider()

# --- 2. BARRA LATERAL (Premissas e Inputs) ---
st.sidebar.header("Premissas do Modelo")

# Custo de Capital (COC)
taxa_desconto_perc = st.sidebar.number_input(
    "Custo de Capital (COC) em %", 
    min_value=0.0, 
    max_value=200.0, 
    value=40.0, 
    step=1.0,
)
taxa_desconto = taxa_desconto_perc / 100

# Horizonte da Projeção
num_anos = st.sidebar.number_input(
    "Número de anos projetados", 
    min_value=1, 
    max_value=15, 
    value=5, 
    step=1
)

# Caixas dinâmicas para os Fluxos de Caixa
st.sidebar.subheader("Fluxos de Caixa Projetados (R$)")

fluxos_de_caixa = []
for i in range(1, int(num_anos) + 1):
    cf = st.sidebar.number_input(
        f"Fluxo de Caixa - Ano {i}", 
        value=-100000.0, 
        step=50000.0, 
        key=f"cf_{i}"
    )
    fluxos_de_caixa.append(cf)

# Terminal Value
st.sidebar.subheader("Valor Terminal")
terminal_value = st.sidebar.number_input(
    "Terminal Value (TV) no ano final", 
    value=5000000.0, 
    step=100000.0,
    help="O valor estimado da empresa do último ano projetado em diante."
)

st.header("Cálculo do Valor Presente")

valor_presente_fluxos = 0

st.write("### Desconto dos Fluxos Ano a Ano")
# Loop para calcular o Valor Presente de cada ano
for i, cf in enumerate(fluxos_de_caixa, start=1):
    fator_desconto = (1 + taxa_desconto) ** i
    vp_cf = cf / fator_desconto
    valor_presente_fluxos += vp_cf
    
    # Mostra a memória de cálculo na tela para o usuário entender
    st.write(f"**Ano {i}:** R\$ {cf:,.2f} descontado a {taxa_desconto_perc}% = **R\$ {vp_cf:,.2f}**")
# Cálculo do Valor Presente do Terminal Value
vp_tv = terminal_value / ((1 + taxa_desconto) ** (num_anos + 1))

# Cálculo do Enterprise Value 
enterprise_value = valor_presente_fluxos + vp_tv

st.divider()

# --- 4. RESULTADOS FINAIS ---
st.write("Resumo do Valuation")

col1, col2, col3 = st.columns(3)

col1.metric("VP dos Fluxos", f"R$ {valor_presente_fluxos:,.2f}")
col2.metric(f"VP do TV (Ano {num_anos})", f"R$ {vp_tv:,.2f}")
col3.metric("Valor da Empresa", f"R$ {enterprise_value:,.2f}")
