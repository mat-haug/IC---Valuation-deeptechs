import streamlit as st

# --- CONFIGURAÇÃO GERAL ---
st.set_page_config(page_title="Valuation Deep Techs", page_icon="🔬", layout="wide")

# --- CUSTOMIZAÇÃO DE CORES E LOGO (CSS INJECT) ---
st.markdown(
    """
    <style>
    /* Fundo da barra lateral mais suave */
    [data-testid="stSidebar"] {
        background-color: #f8f9fc;
    }
    
    /* Cor dos títulos (Azul Escuro Institucional) */
    h1, h2, h3, h4 {
        color: #002244 !important;
    }

    /* Destacando os números principais das métricas com a cor do tema */
    [data-testid="stMetricValue"] {
        color: #002244;
        font-weight: 800;
    }

    /* Estilizando as bordas dos cartões para um visual mais moderno (SaaS) */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        border-radius: 12px !important;
        border-color: #e0e4e8 !important;
        box-shadow: 2px 4px 12px rgba(0,0,0,0.04);
    }

    /* Fixando o logo da USP no canto inferior direito */
    .logo-fixo {
        position: fixed;
        bottom: 25px;
        right: 25px;
        width: 110px;  /* Tamanho do logo */
        z-index: 9999; /* Garante que fique por cima de tudo na tela */
        opacity: 0.8;  /* Leve transparência para não atrapalhar a leitura */
        transition: 0.3s ease-in-out;
    }
    
    /* Efeito ao passar o mouse no logo */
    .logo-fixo:hover {
        opacity: 1.0;
        transform: scale(1.05);
    }
    </style>

    <a href="https://www.usp.br" target="_blank">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Universidade_de_S%C3%A3o_Paulo_bras%C3%A3o.png/320px-Universidade_de_S%C3%A3o_Paulo_bras%C3%A3o.png" class="logo-fixo" alt="Logo USP">
    </a>
    """,
    unsafe_allow_html=True
)

# --- NAVEGAÇÃO (BARRA LATERAL) ---
st.sidebar.markdown("### 🧭 Menu Principal")
pagina = st.sidebar.radio(
    "Selecione o Cenário:",
    ["🔬 Licenciamento", "⚡ Energia", "🌱 Agronegócio"],
    label_visibility="collapsed" 
)

st.sidebar.divider()

# --- LÓGICA POR PÁGINA ---

if pagina == "🔬 Licenciamento":
    st.title("🔬 Valuation - Licenciamento Tecnológico")
    st.markdown("Modelo de Fluxo de Caixa Descontado (DCF) ajustado para Iniciação Tecnológica.")
    
    # --- PREMISSAS GLOBAIS (BARRA LATERAL) ---
    st.sidebar.markdown("### ⚙️ Premissas Globais")
    
    tipo_valuation = st.sidebar.selectbox("Metodologia:", ["NPV Tradicional", "rNPV (Ajustado ao Risco)"])
    coc_constante = st.sidebar.radio("COC constante no tempo?", ["Sim", "Não"], horizontal=True)

    if coc_constante == "Sim":
        taxa_desconto_perc = st.sidebar.number_input("Custo de Capital Global (%)", min_value=0.0, max_value=200.0, value=40.0, step=1.0)
        taxa_desconto_global = taxa_desconto_perc / 100
    else:
        taxa_desconto_global = 0.0 

    num_anos = st.sidebar.number_input("Horizonte Projetado (Anos)", min_value=1, max_value=15, value=5, step=1)

    # --- ENTRADA DE DADOS (ÁREA PRINCIPAL) ---
    st.subheader("📊 Projeção de Fluxos de Caixa")
    
    with st.container(border=True):
        fluxos_de_caixa = []
        taxas_desconto = []
        probabilidades = []
        
        colunas_grid = st.columns(3)
        
        for i in range(int(num_anos)):
            with colunas_grid[i % 3]:
                st.markdown(f"**Ano {i+1}**")
                cf = st.number_input(f"Fluxo de Caixa (R$)", value=-100000.0, step=50000.0, key=f"cf_{i+1}")
                fluxos_de_caixa.append(cf)
                
                if coc_constante == "Não":
                    taxa = st.number_input(f"COC (%)", value=40.0, step=1.0, key=f"taxa_{i+1}") / 100
                    taxas_desconto.append(taxa)
                else:
                    taxas_desconto.append(taxa_desconto_global)
                    
                if tipo_valuation == "rNPV (Ajustado ao Risco)":
                    prob = st.number_input(f"Sucesso (%)", min_value=0.0, max_value=100.0, value=100.0, step=5.0, key=f"prob_{i+1}") / 100
                    probabilidades.append(prob)
                else:
                    probabilidades.append(1.0)
                
                st.write("") 

    with st.container(border=True):
        st.markdown("**📈 Valor Terminal (Perpetuidade)**")
        col_tv1, col_tv2, col_tv3 = st.columns(3)
        
        with col_tv1:
            terminal_value = st.number_input("Terminal Value Estimado (R$)", value=5000000.0, step=100000.0)
        with col_tv2:
            if coc_constante == "Não":
                taxa_tv = st.number_input("COC do TV (%)", value=40.0, step=1.0) / 100
            else:
                taxa_tv = taxa_desconto_global
                st.metric("COC do TV", f"{taxa_tv*100:.0f}%", help="Herdado da premissa global") 
        with col_tv3:
            if tipo_valuation == "rNPV (Ajustado ao Risco)":
                prob_tv = st.number_input("Prob. Sucesso TV (%)", min_value=0.0, max_value=100.0, value=100.0, step=5.0) / 100
            else:
                prob_tv = 1.0
                st.metric("Prob. Sucesso TV", "100%", help="NPV tradicional não ajusta probabilidade")

    # --- CÁLCULOS DA MEMÓRIA ---
    st.subheader("⚙️ Memória de Cálculo")
    
    valor_presente_fluxos = 0
    fator_desconto_acumulado = 1.0
    
    with st.container(border=True):
        for i in range(int(num_anos)):
            ano = i + 1
            cf = fluxos_de_caixa[i]
            taxa = taxas_desconto[i]
            prob = probabilidades[i]

            cf_esperado = cf * prob

            if coc_constante == "Não":
                fator_desconto_acumulado *= (1 + taxa)
                fator_atual = fator_desconto_acumulado
            else:
                fator_atual = (1 + taxa) ** ano

            vp_cf = cf_esperado / fator_atual
            valor_presente_fluxos += vp_cf
            
            texto_prob = f" (Prob: {prob*100:.0f}%)" if tipo_valuation == "rNPV (Ajustado ao Risco)" else ""
            st.write(f"**Ano {ano}:** R\$ {cf_esperado:,.2f}{texto_prob} descontado a {taxa*100:.1f}% = **R\$ {vp_cf:,.2f}**")
        
        tv_esperado = terminal_value * prob_tv
        fator_tv = (1 + taxa_tv) ** num_anos
        vp_tv = tv_esperado / fator_tv
        
        texto_prob_tv = f" (Prob: {prob_tv*100:.0f}%)" if tipo_valuation == "rNPV (Ajustado ao Risco)" else ""
        st.divider()
        st.write(f"**Perpetuidade:** R\$ {tv_esperado:,.2f}{texto_prob_tv} descontado a {taxa_tv*100:.1f}% = **R\$ {vp_tv:,.2f}**")

    # --- RESULTADOS FINAIS ---
    enterprise_value = valor_presente_fluxos + vp_tv
    
    st.subheader("🎯 Resumo do Valuation")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        with st.container(border=True):
            st.metric("VP dos Fluxos Projetados", f"R$ {valor_presente_fluxos:,.2f}")
    with col_res2:
        with st.container(border=True):
            st.metric(f"VP do Terminal Value", f"R$ {vp_tv:,.2f}")
    with col_res3:
        with st.container(border=True): 
            st.metric("Enterprise Value (Valuation)", f"R$ {enterprise_value:,.2f}")


elif pagina == "⚡ Energia":
    st.title("Valuation - Setor de Energia")
    st.info("Aba em desenvolvimento para infraestrutura e ativos de energia.")

elif pagina == "🌱 Agronegócio":
    st.title("Valuation - Setor de Agronegócio")
    st.info("Aba em desenvolvimento para Biotechs e Agtechs.")