import streamlit as st

# CONFIGURAÇÃO GERAL
st.set_page_config(page_title="Valuation Deep Techs", page_icon="🔬", layout="wide")

# --- BARRA LATERAL (Navegação) ---
st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Selecione o Cenário:",
    ["🔬 Licenciamento", "⚡ Energia", "🌱 Agronegócio"]
)
st.sidebar.divider()

# --- LÓGICA POR PÁGINA ---

if pagina == "🔬 Licenciamento":
    st.title("Valuation de Deep Techs - Licenciamento")
    st.markdown("Modelo de Fluxo de Caixa Descontado (DCF) ajustado para Iniciação Tecnológica.")
    st.divider()

    st.sidebar.header("Premissas do Modelo")

    # 1. Toggles Iniciais
    tipo_valuation = st.sidebar.radio("Metodologia de Valuation:", ["NPV Tradicional", "rNPV (Ajustado ao Risco)"])
    coc_constante = st.sidebar.radio("O Custo de Capital (COC) será constante ao longo do tempo?", ["Sim", "Não"])

    if coc_constante == "Sim":
        taxa_desconto_perc = st.sidebar.number_input("Custo de Capital (COC) Global em %", min_value=0.0, max_value=200.0, value=40.0, step=1.0)
        taxa_desconto_global = taxa_desconto_perc / 100
    else:
        taxa_desconto_global = 0.0 # Será definido ano a ano dentro do loop

    num_anos = st.sidebar.number_input("Número de anos projetados", min_value=1, max_value=15, value=5, step=1)

    # 2. Usando Expander para não poluir a barra lateral
    with st.sidebar.expander("⚙️ Configurar Fluxos Ano a Ano", expanded=True):
        fluxos_de_caixa = []
        taxas_desconto = []
        probabilidades = []

        for i in range(1, int(num_anos) + 1):
            st.markdown(f"**Ano {i}**")
            
            # Caixa do Fluxo de Caixa
            cf = st.number_input(f"Fluxo de Caixa (R$)", value=-100000.0, step=50000.0, key=f"cf_{i}")
            fluxos_de_caixa.append(cf)

            # Caixa do COC Variável (Se aplicável)
            if coc_constante == "Não":
                taxa = st.number_input(f"COC Ano {i} (%)", value=40.0, step=1.0, key=f"taxa_{i}") / 100
                taxas_desconto.append(taxa)
            else:
                taxas_desconto.append(taxa_desconto_global)

            # Caixa do rNPV (Se aplicável)
            if tipo_valuation == "rNPV (Ajustado ao Risco)":
                prob = st.number_input(f"Probabilidade de Sucesso (%)", min_value=0.0, max_value=100.0, value=100.0, step=5.0, key=f"prob_{i}") / 100
                probabilidades.append(prob)
            else:
                probabilidades.append(1.0)
                
            st.divider() # Linha para separar cada ano dentro do menu sanfona

    # 3. Expander do Terminal Value
    with st.sidebar.expander("📈 Configurar Valor Terminal (TV)", expanded=True):
        terminal_value = st.number_input("Terminal Value (TV) no ano final", value=5000000.0, step=100000.0)
        
        if coc_constante == "Não":
            taxa_tv = st.number_input("COC para o desconto do TV (%)", value=40.0, step=1.0) / 100
        else:
            taxa_tv = taxa_desconto_global
            
        if tipo_valuation == "rNPV (Ajustado ao Risco)":
            prob_tv = st.number_input("Prob. de Sucesso para o TV (%)", min_value=0.0, max_value=100.0, value=100.0, step=5.0) / 100
        else:
            prob_tv = 1.0

    # --- CÁLCULOS E RESULTADOS ---
    st.header("Cálculo do Valor Presente")
    valor_presente_fluxos = 0
    fator_desconto_acumulado = 1.0

    st.write("### Desconto dos Fluxos Ano a Ano")
    
    for i in range(int(num_anos)):
        ano = i + 1
        cf = fluxos_de_caixa[i]
        taxa = taxas_desconto[i]
        prob = probabilidades[i]

        # Risco no Numerador: Fluxo Esperado
        cf_esperado = cf * prob

        # Risco no Denominador: Fator de Desconto
        if coc_constante == "Não":
            # Multiplica as taxas ano a ano (Juros Compostos de taxas variáveis)
            fator_desconto_acumulado *= (1 + taxa)
            fator_atual = fator_desconto_acumulado
        else:
            fator_atual = (1 + taxa) ** ano

        vp_cf = cf_esperado / fator_atual
        valor_presente_fluxos += vp_cf
        
        # Exibição inteligente do texto
        texto_prob = f" (Prob: {prob*100:.0f}%)" if tipo_valuation == "rNPV (Ajustado ao Risco)" else ""
        st.write(f"**Ano {ano}:** R\$ {cf_esperado:,.2f}{texto_prob} descontado a {taxa*100:.1f}% = **R\$ {vp_cf:,.2f}**")
    
    # --- Cálculo do TV ---
    tv_esperado = terminal_value * prob_tv
    fator_tv = (1 + taxa_tv) ** num_anos
    vp_tv = tv_esperado / fator_tv
    
    texto_prob_tv = f" (Prob: {prob_tv*100:.0f}%)" if tipo_valuation == "rNPV (Ajustado ao Risco)" else ""
    st.write(f"**Perpetuidade:** R\$ {tv_esperado:,.2f}{texto_prob_tv} descontado a {taxa_tv*100:.1f}% = **R\$ {vp_tv:,.2f}**")

    # Enterprise Value 
    enterprise_value = valor_presente_fluxos + vp_tv

    st.divider()

    st.write("### Resumo do Valuation")

    col1, col2, col3 = st.columns(3)
    col1.metric("VP dos Fluxos", f"R$ {valor_presente_fluxos:,.2f}")
    col2.metric(f"VP do TV (Ano {num_anos})", f"R$ {vp_tv:,.2f}")
    col3.metric("Valor da Empresa", f"R$ {enterprise_value:,.2f}")

elif pagina == "⚡ Energia":
    st.title("Valuation - Setor de Energia")
    st.info("Esta aba será configurada para modelos de valuation focados em infraestrutura e ativos de energia.")

elif pagina == "🌱 Agronegócio":
    st.title("Valuation - Setor de Agronegócio")
    st.info("Esta aba será configurada para modelos de valuation focados em Biotechs e Agtechs.")