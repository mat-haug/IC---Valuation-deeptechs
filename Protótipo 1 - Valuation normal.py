# import streamlit as st

# # --- CONFIGURAÇÃO GERAL ---
# st.set_page_config(page_title="Valuation Deep Techs", page_icon="🔬", layout="wide")

# # --- NAVEGAÇÃO (BARRA LATERAL) ---
# st.sidebar.markdown("### 🧭 Menu Principal")
# pagina = st.sidebar.radio(
#     "Selecione o Cenário:",
#     ["🔬 Licenciamento", "⚡ Energia", "🌱 Agronegócio"],
#     label_visibility="collapsed" # Esconde o título do radio para ficar com cara de menu nativo
# )

# st.sidebar.divider()

# # --- LÓGICA POR PÁGINA ---

# if pagina == "🔬 Licenciamento":
#     st.title("🔬 Valuation - Licenciamento Tecnológico")
#     st.markdown("Modelo de Fluxo de Caixa Descontado (DCF) ajustado para Iniciação Tecnológica.")
    
#     # --- PREMISSAS GLOBAIS (BARRA LATERAL) ---
#     st.sidebar.markdown("### ⚙️ Premissas Globais")
    
#     tipo_valuation = st.sidebar.selectbox("Metodologia:", ["NPV Tradicional", "rNPV (Ajustado ao Risco)"])
#     coc_constante = st.sidebar.radio("COC constante no tempo?", ["Sim", "Não"], horizontal=True)

#     if coc_constante == "Sim":
#         taxa_desconto_perc = st.sidebar.number_input("Custo de Capital Global (%)", min_value=0.0, max_value=200.0, value=40.0, step=1.0)
#         taxa_desconto_global = taxa_desconto_perc / 100
#     else:
#         taxa_desconto_global = 0.0 # Será definido ano a ano

#     num_anos = st.sidebar.number_input("Horizonte Projetado (Anos)", min_value=1, max_value=15, value=5, step=1)

#     # --- ENTRADA DE DADOS (ÁREA PRINCIPAL) ---
#     st.subheader("📊 Projeção de Fluxos de Caixa")
    
#     # Cartão com borda para organizar a entrada de dados
#     with st.container(border=True):
#         fluxos_de_caixa = []
#         taxas_desconto = []
#         probabilidades = []
        
#         # Cria um layout de Grid (3 colunas por linha) para ficar organizado
#         colunas_grid = st.columns(3)
        
#         for i in range(int(num_anos)):
#             # O "i % 3" garante que os anos vão preenchendo as colunas de 3 em 3
#             with colunas_grid[i % 3]:
#                 st.markdown(f"**Ano {i+1}**")
#                 cf = st.number_input(f"Fluxo de Caixa (R$)", value=-100000.0, step=50000.0, key=f"cf_{i+1}")
#                 fluxos_de_caixa.append(cf)
                
#                 if coc_constante == "Não":
#                     taxa = st.number_input(f"COC (%)", value=40.0, step=1.0, key=f"taxa_{i+1}") / 100
#                     taxas_desconto.append(taxa)
#                 else:
#                     taxas_desconto.append(taxa_desconto_global)
                    
#                 if tipo_valuation == "rNPV (Ajustado ao Risco)":
#                     prob = st.number_input(f"Sucesso (%)", min_value=0.0, max_value=100.0, value=100.0, step=5.0, key=f"prob_{i+1}") / 100
#                     probabilidades.append(prob)
#                 else:
#                     probabilidades.append(1.0)
                
#                 st.write("") # Espaço extra entre as linhas do grid

#     # Cartão exclusivo para o Terminal Value
#     with st.container(border=True):
#         st.markdown("**📈 Valor Terminal (Perpetuidade)**")
#         col_tv1, col_tv2, col_tv3 = st.columns(3)
        
#         with col_tv1:
#             terminal_value = st.number_input("Terminal Value Estimado (R$)", value=5000000.0, step=100000.0)
#         with col_tv2:
#             if coc_constante == "Não":
#                 taxa_tv = st.number_input("COC do TV (%)", value=40.0, step=1.0) / 100
#             else:
#                 taxa_tv = taxa_desconto_global
#                 # St.metric fica com cara de Dashboard informando um valor que ele herdou
#                 st.metric("COC do TV", f"{taxa_tv*100:.0f}%", help="Herdado da premissa global") 
#         with col_tv3:
#             if tipo_valuation == "rNPV (Ajustado ao Risco)":
#                 prob_tv = st.number_input("Prob. Sucesso TV (%)", min_value=0.0, max_value=100.0, value=100.0, step=5.0) / 100
#             else:
#                 prob_tv = 1.0
#                 st.metric("Prob. Sucesso TV", "100%", help="NPV tradicional não ajusta probabilidade")

#     # --- CÁLCULOS DA MEMÓRIA ---
#     st.subheader("⚙️ Memória de Cálculo")
    
#     valor_presente_fluxos = 0
#     fator_desconto_acumulado = 1.0
    
#     with st.container(border=True):
#         for i in range(int(num_anos)):
#             ano = i + 1
#             cf = fluxos_de_caixa[i]
#             taxa = taxas_desconto[i]
#             prob = probabilidades[i]

#             cf_esperado = cf * prob

#             if coc_constante == "Não":
#                 fator_desconto_acumulado *= (1 + taxa)
#                 fator_atual = fator_desconto_acumulado
#             else:
#                 fator_atual = (1 + taxa) ** ano

#             vp_cf = cf_esperado / fator_atual
#             valor_presente_fluxos += vp_cf
            
#             texto_prob = f" (Prob: {prob*100:.0f}%)" if tipo_valuation == "rNPV (Ajustado ao Risco)" else ""
#             st.write(f"**Ano {ano}:** R\$ {cf_esperado:,.2f}{texto_prob} descontado a {taxa*100:.1f}% = **R\$ {vp_cf:,.2f}**")
        
#         # TV
#         tv_esperado = terminal_value * prob_tv
#         fator_tv = (1 + taxa_tv) ** num_anos
#         vp_tv = tv_esperado / fator_tv
        
#         texto_prob_tv = f" (Prob: {prob_tv*100:.0f}%)" if tipo_valuation == "rNPV (Ajustado ao Risco)" else ""
#         st.divider()
#         st.write(f"**Perpetuidade:** R\$ {tv_esperado:,.2f}{texto_prob_tv} descontado a {taxa_tv*100:.1f}% = **R\$ {vp_tv:,.2f}**")

#     # --- RESULTADOS FINAIS (Dashboard Style) ---
#     enterprise_value = valor_presente_fluxos + vp_tv
    
#     st.subheader("🎯 Resumo do Valuation")
    
#     col_res1, col_res2, col_res3 = st.columns(3)
#     with col_res1:
#         with st.container(border=True):
#             st.metric("VP dos Fluxos Projetados", f"R$ {valor_presente_fluxos:,.2f}")
#     with col_res2:
#         with st.container(border=True):
#             st.metric(f"VP do Terminal Value", f"R$ {vp_tv:,.2f}")
#     with col_res3:
#         with st.container(border=True): # Dá um destaque no resultado final
#             st.metric("Enterprise Value (Valuation)", f"R$ {enterprise_value:,.2f}")


# elif pagina == "⚡ Energia":
#     st.title("Valuation - Setor de Energia")
#     st.info("Aba em desenvolvimento para infraestrutura e ativos de energia.")

# elif pagina == "🌱 Agronegócio":
#     st.title("Valuation - Setor de Agronegócio")
#     st.info("Aba em desenvolvimento para Biotechs e Agtechs.")

import streamlit as st

# --- CONFIGURAÇÃO GERAL ---
st.set_page_config(page_title="Valuation Deep Techs", page_icon="🔬", layout="wide")

# --- CUSTOM CSS (Estética Dark Tech / Profissional) ---
st.markdown("""
    <style>
        /* Fundo principal escuro (Preto/Cinza profundo) */
        .stApp { background-color: #0E1117; }
        
        /* Títulos principais em Azul Tech elegante */
        h1 { color: #00D2FF !important; font-weight: 800 !important; }
        
        /* Subtítulos em cinza claro/branco para leitura fácil */
        h2, h3 { color: #E2E8F0 !important; font-weight: 700 !important; }
        
        /* Cartões flutuantes com fundo escuro e uma borda tech muito sutil */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 12px !important;
            background-color: #161B22 !important;
            box-shadow: 0px 4px 20px rgba(0, 210, 255, 0.05) !important; /* Um leve glow azul */
            border: 1px solid #30363D !important;
            padding: 1rem !important;
        }
        
        /* Números de resultado em Verde Matrix/Finanças */
        [data-testid="stMetricValue"] {
            color: #39D353 !important;
            font-size: 2.2rem !important;
            font-weight: 800 !important;
        }
        
        /* Textos descritivos dos resultados */
        [data-testid="stMetricLabel"] {
            font-size: 1.1rem !important;
            color: #8B949E !important;
            font-weight: 600 !important;
        }
        
        /* Barra lateral num tom de preto ainda mais fechado para contraste */
        [data-testid="stSidebar"] {
            background-color: #010409 !important;
            border-right: 1px solid #21262D !important;
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
    st.markdown("Plataforma de avaliação financeira ajustada para Deep Techs e startups de base tecnológica.")
    
    # --- PREMISSAS GLOBAIS (BARRA LATERAL) ---
    st.sidebar.markdown("### ⚙️ Premissas Globais")
    
    tipo_valuation = st.sidebar.selectbox(
        "Metodologia:", 
        ["NPV Tradicional", "rNPV (Ajustado ao Risco)", "VC Method (Capital de Risco)"]
    )
    
    # Seletor de Ordem de Grandeza
    ordem_grandeza = st.sidebar.selectbox("Ordem de Grandeza Financeira:", ["Milhares (Mil)", "Milhões (Mi)", "Bilhões (Bi)"], index=1)
    
    if ordem_grandeza == "Milhares (Mil)":
        mult = 1_000
        sufixo = "Mil"
    elif ordem_grandeza == "Milhões (Mi)":
        mult = 1_000_000
        sufixo = "Mi"
    else:
        mult = 1_000_000_000
        sufixo = "Bi"

    # Se a metodologia for VC, o Custo de Capital vira o "ROI Alvo", mas a variável global se mantém
    coc_constante = st.sidebar.radio("Custo de Capital constante no tempo?", ["Sim", "Não"], horizontal=True)

    if coc_constante == "Sim":
        taxa_desconto_perc = st.sidebar.number_input("Custo de Capital Global (%)", min_value=0.0, max_value=200.0, value=40.0, step=1.0)
        taxa_desconto_global = taxa_desconto_perc / 100
    else:
        taxa_desconto_global = 0.0 

    num_anos = st.sidebar.number_input("Horizonte Projetado (Anos)", min_value=1, max_value=15, value=5, step=1)

    # =========================================================================
    # LÓGICA 1: NPV e rNPV (Métodos Baseados em Fluxo de Caixa Contínuo)
    # =========================================================================
    if tipo_valuation in ["NPV Tradicional", "rNPV (Ajustado ao Risco)"]:
        
        st.subheader("📊 Projeção de Fluxos de Caixa")
        
        with st.container(border=True):
            fluxos_de_caixa = []
            taxas_desconto = []
            probabilidades = []
            
            colunas_grid = st.columns(3)
            
            for i in range(int(num_anos)):
                with colunas_grid[i % 3]:
                    st.markdown(f"**Ano {i+1}**")
                    cf_input = st.number_input(f"Fluxo de Caixa (Em {sufixo})", value=-100.0, step=50.0, key=f"cf_{i+1}")
                    fluxos_de_caixa.append(cf_input * mult) # Multiplicador aplicado
                    
                    if coc_constante == "Não":
                        taxa = st.number_input(f"Custo de Capital (%)", value=40.0, step=1.0, key=f"taxa_{i+1}") / 100
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
                tv_input = st.number_input(f"Terminal Value Estimado (Em {sufixo})", value=5.0, step=1.0)
                terminal_value = tv_input * mult
            with col_tv2:
                if coc_constante == "Não":
                    taxa_tv = st.number_input("Custo de Capital do TV (%)", value=40.0, step=1.0) / 100
                else:
                    taxa_tv = taxa_desconto_global
                    st.metric("Custo de Capital do TV", f"{taxa_tv*100:.0f}%") 
            with col_tv3:
                if tipo_valuation == "rNPV (Ajustado ao Risco)":
                    prob_tv = st.number_input("Prob. Sucesso TV (%)", min_value=0.0, max_value=100.0, value=100.0, step=5.0) / 100
                else:
                    prob_tv = 1.0
                    st.metric("Prob. Sucesso TV", "100%")

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
                st.metric("💰 Enterprise Value (Valuation)", f"R$ {enterprise_value:,.2f}")

    # =========================================================================
    # LÓGICA 2: VC METHOD (Focado na saída e diluição, dispensa fluxo contínuo)
    # =========================================================================
    elif tipo_valuation == "VC Method (Capital de Risco)":
        
        st.subheader("📊 Premissas da Rodada e Retenção")
        
        with st.container(border=True):
            col_vc1, col_vc2 = st.columns(2)
            with col_vc1:
                investimento_input = st.number_input(f"Aporte Solicitado na Rodada Atual (Em {sufixo})", value=2.0, step=0.5)
                investimento = investimento_input * mult
                target_ownership = st.number_input("Participação Alvo do Investidor na Saída (%)", min_value=1.0, max_value=100.0, value=20.0, step=1.0) / 100
                
            with col_vc2:
                diluicao_futura = st.number_input("Expectativa de Diluição em Rodadas Futuras (%)", min_value=0.0, max_value=100.0, value=15.0, step=1.0) / 100
                taxa_retencao = 1 - diluicao_futura
                participacao_exigida = target_ownership / taxa_retencao if taxa_retencao > 0 else 0
                st.metric("Taxa de Retenção (Retention Rate)", f"{taxa_retencao*100:.1f}%")
        
        with st.container(border=True):
            st.markdown("**📈 Valor Terminal no Evento de Liquidez (Saída)**")
            col_tv1, col_tv2 = st.columns(2)
            with col_tv1:
                tv_input = st.number_input(f"Terminal Value Estimado no Ano {int(num_anos)} (Em {sufixo})", value=50.0, step=5.0)
                terminal_value = tv_input * mult
            with col_tv2:
                if coc_constante == "Não":
                    roi_alvo = st.number_input("ROI Alvo / Hurdle Rate (%)", value=50.0, step=5.0) / 100
                else:
                    roi_alvo = taxa_desconto_global
                    st.metric("ROI Alvo / Hurdle Rate", f"{roi_alvo*100:.0f}%", help="O Custo de Capital atua como a taxa de retorno exigida pelo fundo.") 

        st.subheader("⚙️ Memória de Cálculo (VC Method)")
        
        post_money = terminal_value / ((1 + roi_alvo) ** num_anos)
        pre_money = post_money - investimento
        
        with st.container(border=True):
            st.markdown(f"""
            1. **Post-Money Valuation:** Trazendo o Terminal Value de **R$ {terminal_value:,.2f}** a valor presente usando o ROI Alvo de **{roi_alvo*100:.1f}%** ao longo de **{int(num_anos)} anos**.
               * $Post\\text{{-}}Money = \\frac{{TV}}{{(1 + ROI)^n}}$ = **R$ {post_money:,.2f}**
               
            2. **Pre-Money Valuation:** Subtraindo o investimento da rodada atual de **R$ {investimento:,.2f}**.
               * $Pre\\text{{-}}Money = Post\\text{{-}}Money - Investimento$ = **R$ {pre_money:,.2f}**
               
            3. **Participação Exigida Hoje (Required Current Ownership):** Ajustando a meta de **{target_ownership*100:.1f}%** pela diluição futura.
               * $Ownership = \\frac{{Target\\ Ownership}}{{Retention\\ Rate}}$ = **{participacao_exigida*100:.2f}%**
            """)

        st.subheader("🎯 Resumo do Valuation (Capital de Risco)")
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            with st.container(border=True):
                st.metric("Pre-Money Valuation", f"R$ {pre_money:,.2f}")
        with col_res2:
            with st.container(border=True):
                st.metric(f"Post-Money Valuation", f"R$ {post_money:,.2f}")
        with col_res3:
            with st.container(border=True): 
                st.metric("🤝 Participação a Ceder", f"{participacao_exigida*100:.2f}%")


elif pagina == "⚡ Energia":
    st.title("⚡ Valuation - Setor de Energia")
    st.info("Aba em desenvolvimento para infraestrutura e ativos de energia.")

elif pagina == "🌱 Agronegócio":
    st.title("🌱 Valuation - Setor de Agronegócio")
    st.info("Aba em desenvolvimento para Biotechs e Agtechs.")