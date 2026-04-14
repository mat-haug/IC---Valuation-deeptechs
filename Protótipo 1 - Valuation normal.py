import streamlit as st

# --- CONFIGURAÇÃO GERAL ---
st.set_page_config(page_title="Valuation Deep Techs", page_icon="🔬", layout="wide")

# --- CUSTOM CSS (O TRUQUE DE DESIGN) ---
st.markdown("""
    <style>
        /* Fundo principal do site mais suave (Cinza claro corporativo) */
        .stApp {
            background-color: #F4F6F9;
        }
        /* Cor e peso dos títulos principais */
        h1 {
            color: #1E3A8A !important; /* Azul escuro tech */
            font-weight: 800 !important;
        }
        h2, h3 {
            color: #334155 !important; /* Cinza chumbo */
            font-weight: 700 !important;
        }
        /* Estilizando os Cartões (Containers com borda) */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 12px !important;
            background-color: #FFFFFF !important;
            box-shadow: 0px 4px 16px rgba(0, 0, 0, 0.04) !important;
            border: 1px solid #E2E8F0 !important;
            padding: 1rem !important;
        }
        /* Estilizando os números de Resultado (Metrics) */
        [data-testid="stMetricValue"] {
            color: #047857 !important; /* Verde financeiro clássico */
            font-size: 2.2rem !important;
            font-weight: 800 !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 1.1rem !important;
            color: #64748B !important;
            font-weight: 600 !important;
        }
        /* Barra lateral mais limpa */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
        }
    </style>
""", unsafe_allow_html=True)

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
            # Um st.success para dar um destaque visual maior ao resultado final
            st.success("💰 Enterprise Value Final")
            st.metric("", f"R$ {enterprise_value:,.2f}", label_visibility="collapsed")


elif pagina == "⚡ Energia":
    st.title("⚡ Valuation - Setor de Energia")
    st.info("Aba em desenvolvimento para infraestrutura e ativos de energia.")

elif pagina == "🌱 Agronegócio":
    st.title("🌱 Valuation - Setor de Agronegócio")
    st.info("Aba em desenvolvimento para Biotechs e Agtechs.")