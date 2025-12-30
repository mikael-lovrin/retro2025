import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Retrospectiva '25", page_icon="🌿", layout="centered")

# --- PALETA "ARCHITECT" ---
color_success = '#2E8B57'  # SeaGreen
color_warning = '#D4AC0D'  # Classic Gold
color_alert   = '#C0392B'  # Red
color_sage    = '#52796F'  # Sage Green Base
funnel_palette = ['#354F52', '#52796F', '#84A98C', '#B2BDA0']

# --- CSS PERSONALIZADO ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    .stApp {{ background-color: #F9F7F2; }}

    h1, h2, h3 {{
        font-family: 'Playfair Display', serif !important;
        color: #2F3E46;
        font-weight: 700;
    }}
    
    p, div, label, span {{
        font-family: 'Inter', sans-serif;
        color: #485659;
    }}

    /* Cards KPI */
    .kpi-card {{
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 10px;
        border: 1px solid #EBEBE8;
    }}
    
    .kpi-label {{
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #6c757d;
        font-weight: 600;
        margin-bottom: 4px;
    }}
    
    .kpi-val {{
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #2F3E46;
    }}
    
    .kpi-sub {{
        font-size: 0.75rem;
        margin-top: 4px;
        font-style: italic;
        color: #79888A;
    }}

    .border-success {{ border-left: 5px solid {color_success}; }}
    .border-warning {{ border-left: 5px solid {color_warning}; }}
    .border-alert   {{ border-left: 5px solid {color_alert}; }}
    .border-neutral {{ border-left: 5px solid #CAD2C5; }}

</style>
""", unsafe_allow_html=True)

# --- DADOS ---
def load_data():
    data = [
        {'Mes': 'Janeiro', 'Pais': 'Turquia', 'Profissao': 'Engenheira', 'Idade': 25, 'Cabelo': 'Castanho', 'Tipo': 'Reciclado', 'Lugar': 'N/A', 'Beijo': 'Sim', 'Output': 'Conhecidos'},
        {'Mes': 'Janeiro', 'Pais': 'Alemanha', 'Profissao': 'Arquiteta', 'Idade': 22, 'Cabelo': 'Loiro', 'Tipo': 'Reciclado', 'Lugar': 'N/A', 'Beijo': 'Sim', 'Output': 'Amigos'},
        {'Mes': 'Fevereiro', 'Pais': 'Brasil', 'Profissao': 'Engenheira', 'Idade': 27, 'Cabelo': 'Castanho', 'Tipo': 'Novo', 'Lugar': 'Café', 'Beijo': 'Não', 'Output': 'Conhecidos'},
        {'Mes': 'Fevereiro', 'Pais': 'Brasil', 'Profissao': 'Nutrição', 'Idade': 22, 'Cabelo': 'Loiro', 'Tipo': 'Novo', 'Lugar': 'Café', 'Beijo': 'Não', 'Output': 'Conhecidos'},
        {'Mes': 'Março', 'Pais': 'Brasil', 'Profissao': 'Fisioterapia', 'Idade': 24, 'Cabelo': 'Castanho', 'Tipo': 'Reciclado', 'Lugar': 'N/A', 'Beijo': 'Sim', 'Output': 'Amigos'},
        {'Mes': 'Julho', 'Pais': 'Brasil', 'Profissao': 'Advogada', 'Idade': 25, 'Cabelo': 'Castanho', 'Tipo': 'Novo', 'Lugar': 'Parque', 'Beijo': 'Sim', 'Output': 'Ghosting'},
        {'Mes': 'Agosto', 'Pais': 'Brasil', 'Profissao': 'Jornalista', 'Idade': 24, 'Cabelo': 'Castanho', 'Tipo': 'Novo', 'Lugar': 'Concerto', 'Beijo': 'Não', 'Output': 'Amigos'},
        {'Mes': 'Dezembro', 'Pais': 'Brasil', 'Profissao': 'Engenheira', 'Idade': 20, 'Cabelo': 'Castanho', 'Tipo': 'Novo', 'Lugar': 'Parque', 'Beijo': 'Sim', 'Output': 'Conhecidos'},
    ]
    df = pd.DataFrame(data)
    
    def categorizar_area(prof):
        if prof in ['Engenheira', 'Arquiteta']: return 'Exatas/Tech'
        if prof in ['Nutrição', 'Fisioterapia']: return 'Saúde'
        return 'Humanas/Sociais'
    df['Area'] = df['Profissao'].apply(categorizar_area)
    
    meses_ordem = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    df['Mes'] = pd.Categorical(df['Mes'], categories=meses_ordem, ordered=True)
    df = df.sort_values('Mes')
    
    return df

df = load_data()

# Helper Layout Gráficos Clean
def clean_layout(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_family="Inter", font_color="#2F3E46",
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    fig.update_xaxes(showgrid=False, visible=False)
    fig.update_yaxes(showgrid=False, visible=False)
    return fig

def kpi(label, value, sub, status="neutral"):
    st.markdown(f"""
    <div class="kpi-card border-{status}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-val">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

# --- HEADER ---
st.title("Retrospectiva '25")
st.caption("Relatório de Performance Afetiva")

st.markdown("---")

# --- 1. KPIs (GRID HTML RESPONSIVO) ---
# Aqui usamos HTML puro para garantir o Grid 2x3 no celular
st.markdown(f"""
<div class="kpi-grid">
    {kpi_html("Decepções Recebidas", "0", "▼ -100% vs 2024", "success")}
    {kpi_html("Auto-Humilhações", "0", "✔ Recuperação Total", "success")}
    {kpi_html("CAPEX (Por Date)", "R$ 75,00", "Min: R$0 | Max: R$300", "warning")}
    {kpi_html("Decepções Entregues", "1", "⚠️ Incidente Isolado", "warning")}
    {kpi_html("Recaídas", "Error 500", "⛔ Stack Overflow", "alert")}
    {kpi_html("ROI (Retorno)", "Duvidoso", "Ativo de Alto Risco", "alert")}
</div>
""", unsafe_allow_html=True)

st.caption("Nota: Dados financeiros baseados em estimativas proprietárias (Fonte: vozes da minha cabeça).")
st.markdown("---")

# --- 2. DEMOGRAFIA ---
col_demo1, col_demo2 = st.columns(2)

with col_demo1:
    st.subheader("Nacionalidade")
    fig_nac = px.pie(df, names='Pais', hole=0.7, color_discrete_sequence=[color_sage, '#84A98C', '#CAD2C5'])
    st.plotly_chart(clean_layout(fig_nac), width="stretch")

with col_demo2:
    st.subheader("Distribuição Etária")
    fig_age = px.box(df, y='Idade', points="all", color_discrete_sequence=[color_sage])
    fig_age = clean_layout(fig_age)
    # Ajuste: Forçando a visibilidade do eixo Y e dos marcadores (ticks)
    fig_age.update_yaxes(visible=True, showticklabels=True, showgrid=True, gridcolor='#EBEBE8', title=None)
    st.plotly_chart(fig_age, width="stretch")

col_demo3, col_demo4 = st.columns(2)

with col_demo3:
    st.subheader("Perfil Capilar")
    fig_hair = px.pie(df, names='Cabelo', hole=0.7, color_discrete_sequence=['#52796F', '#EBEBE8'])
    st.plotly_chart(clean_layout(fig_hair), width="stretch")

with col_demo4:
    st.subheader("Área de Formação")
    fig_area = px.pie(df, names='Area', hole=0.7, color_discrete_sequence=['#354F52', '#52796F', '#84A98C'])
    st.plotly_chart(clean_layout(fig_area), width="stretch")

st.markdown("---")

# --- 3. SAZONALIDADE ---
st.subheader("Sazonalidade")
dates_mes = df['Mes'].value_counts().reindex(df['Mes'].cat.categories, fill_value=0).reset_index()
dates_mes.columns = ['Mes', 'Qtd']

# Ajuste: text_auto=True para mostrar números nas colunas
fig_saz = px.bar(dates_mes, x='Mes', y='Qtd', text_auto=True, color_discrete_sequence=[color_sage])
fig_saz = clean_layout(fig_saz)
# Ajuste: Eixo Y visível para mostrar a régua
fig_saz.update_yaxes(visible=True, showgrid=True, gridcolor='#EBEBE8', title=None)
fig_saz.update_xaxes(visible=True, title=None)
st.plotly_chart(fig_saz, width="stretch")

st.info("""
**Gargalos Operacionais:** A análise da série temporal demonstra uma correlação direta entre a disponibilidade para encontros e os períodos de recesso acadêmico. Observa-se um gargalo severo durante os meses letivos.
""")
st.markdown("---")

# --- 4. FUNIL DE CONVERSÃO ---
st.subheader("Funil de Conversão")

cf1, cf2 = st.columns(2)
with cf1:
    st.markdown("**1. Origem (Sourcing)**")
    fig_origem = px.pie(df, names='Tipo', hole=0.6, color_discrete_sequence=['#354F52', '#CAD2C5'])
    st.plotly_chart(clean_layout(fig_origem), width="stretch")

with cf2:
    st.markdown("**2. Local (Onboarding)**")
    # Filtra apenas os novos
    df_local_novo = df[df['Tipo']=='Novo']
    fig_local = px.pie(df_local_novo, names='Lugar', hole=0.7, color_discrete_sequence=funnel_palette)
    
    # Aplica o layout limpo primeiro
    fig_local = clean_layout(fig_local)
    
    # Adiciona o texto central (Anotação)
    fig_local.update_layout(
        annotations=[dict(
            text='Apenas<br>1º Date<br>(2025)', # <br> quebra a linha
            x=0.5, y=0.5, # Posição central
            font_size=11, # Tamanho discreto
            showarrow=False,
            font_family="Inter", # Mesma fonte da legenda
            font_color="#79888A" # Mesma cor dos subtítulos para ficar sutil
        )]
    )
    st.plotly_chart(fig_local, width="stretch")

cf3, cf4 = st.columns(2)
with cf3:
    st.markdown("**3. Taxa de Conversão Labial**")
    fig_beijo = px.pie(df, names='Beijo', hole=0.6, color_discrete_sequence=[color_success, '#E0E0E0'])
    st.plotly_chart(clean_layout(fig_beijo), width="stretch")

with cf4:
    st.markdown("**4. Output Final**")
    color_map_out = {'Ghosting': color_alert, 'Amigos': '#52796F', 'Conhecidos': '#CAD2C5'}
    # Aumentei o buraco para caber a nota de alerta
    fig_out = px.pie(df, names='Output', hole=0.7, color='Output', color_discrete_map=color_map_out)
    fig_out = clean_layout(fig_out)
    
    # NOVA ANOTAÇÃO CENTRAL COM ALERTA
    fig_out.update_layout(
        annotations=[dict(
            text='⚠️<br>Failed Situationships<br>01',
            x=0.5, y=0.5,
            font_size=10,
            showarrow=False,
            font_family="Inter",
            font_color="#79888A"
        )]
    )
    st.plotly_chart(fig_out, width="stretch")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.success("Conclusão Técnica: O sistema opera com alta variância, mas sem falhas catastróficas. Uma otimização de hardware para 2026 seria interessante, mas o software demanda refatoração urgente (terapia).")
st.markdown("""
<div style='text-align: center; color: #aaa; font-size: 0.8rem; font-family: Inter;'>
    Design by Mikael Lovrin • Aceitando doações em PIX ou terapia
</div>

""", unsafe_allow_html=True)

