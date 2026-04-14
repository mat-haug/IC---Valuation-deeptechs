import streamlit as st

# CONFIGURAÇÃO GERAL
st.set_page_config(page_title="Valuation Deep Techs", page_icon="🔬", layout="wide")

# --- BARRA LATERAL (Navegação e Ícones) ---
st.sidebar.title("Navegação")
# Adicionando ícones diretamente nas opções para facilitar a visualização
pagina = st.sidebar.radio(
    "Selecione o Cenário:",
    ["🔬 Licenciamento", "⚡ Energia", "🌱 Agronegócio"]
)

# --- LÓGICA POR PÁGINA ---

if pagina == "🔬 Licenciamento":
    st.title("Valuation de Deep Techs - Licenciamento")
    st.markdown("Modelo de Fluxo de Caixa Descontado (DCF) aplicado ao cenário de licenciamento tecnológico.")
    st.divider()

    # BARRA LATERAL (Premissas e Inputs específicos de Licenciamento)
    st.sidebar.header("Premissas de Licenciamento")

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

    # --- CÁLCULOS ---
    st.header("Cálculo do Valor Presente")
    valor_presente_fluxos = 0

    st.write("### Desconto dos Fluxos Ano a Ano")
    
    # Loop para calcular o Valor Presente de cada ano
    for i, cf in enumerate(fluxos_de_caixa, start=1):
        fator_desconto = (1 + taxa_desconto) ** i
        vp_cf = cf / fator_desconto
        valor_presente_fluxos += vp_cf
        
        # Mostra a memória de cálculo na tela
        st.write(f"**Ano {i}:** R\$ {cf:,.2f} descontado a {taxa_desconto_perc}% = **R\$ {vp_cf:,.2f}**")
    
    # Cálculo do Valor Presente do Terminal Value
    vp_tv = terminal_value / ((1 + taxa_desconto) ** num_anos)

    # NOVIDADE: Linha da Perpetuidade logo após o último fluxo
    st.write(f"**Perpetuidade:** R\$ {terminal_value:,.2f} descontado a {taxa_desconto_perc}% = **R\$ {vp_tv:,.2f}**")

    # Cálculo do Enterprise Value 
    enterprise_value = valor_presente_fluxos + vp_tv

    st.divider()

    # RESULTADOS FINAIS
    st.write("### Resumo do Valuation")

    col1, col2, col3 = st.columns(3)
    col1.metric("VP dos Fluxos", f"R$ {valor_presente_fluxos:,.2f}")
    col2.metric(f"VP do TV (Ano {num_anos})", f"R$ {vp_tv:,.2f}")
    col3.metric("Valor da Empresa", f"R$ {enterprise_value:,.2f}")

elif pagina == "⚡ Energia":
    st.title("Valuation - Setor de Energia")
    st.info("Esta aba será configurada para modelos de valuation focados em infraestrutura e ativos de energia.")
    # Aqui você poderá colar uma lógica específica para energia futuramente

elif pagina == "🌱 Agronegócio":
    st.title("Valuation - Setor de Agronegócio")
    st.info("Esta aba será configurada para modelos de valuation focados em Biotechs e Agtechs.")
    # Aqui você poderá colar uma lógica específica para agronegócio futuramente
