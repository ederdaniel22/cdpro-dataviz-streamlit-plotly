"""Dashboard Streamlit com os principais KPIs do dataset de clientes/empréstimos."""
import pandas as pd
import plotly.express as px
import streamlit as st

CAMINHO_CSV = r"D:\CDPRO\CD2026\Base de dados\clientes.csv"

st.set_page_config(page_title="Dashboard - Análise de Clientes", layout="wide")


@st.cache_data
def carregar_dados(caminho: str) -> pd.DataFrame:
    df = pd.read_csv(caminho)
    df["renda"] = pd.to_numeric(df["renda"], errors="coerce")
    df["renda_conjuge"] = pd.to_numeric(df["renda_conjuge"], errors="coerce")
    df["emprestimo"] = pd.to_numeric(df["emprestimo"], errors="coerce")
    df["renda_total"] = df["renda"].fillna(0) + df["renda_conjuge"].fillna(0)
    return df


st.title("📊 Dashboard - Análise de Clientes e Empréstimos")

try:
    df = carregar_dados(CAMINHO_CSV)
except FileNotFoundError:
    st.error(f"Arquivo não encontrado: {CAMINHO_CSV}")
    arquivo = st.file_uploader("Envie o arquivo clientes.csv", type="csv")
    if arquivo is None:
        st.stop()
    df = carregar_dados(arquivo)

# --- Filtros (sidebar) ---
st.sidebar.header("Filtros")
sexo = st.sidebar.multiselect("Sexo", df["sexo"].dropna().unique(), default=list(df["sexo"].dropna().unique()))
educacao = st.sidebar.multiselect("Educação", df["educacao"].dropna().unique(), default=list(df["educacao"].dropna().unique()))
imovel = st.sidebar.multiselect("Área do Imóvel", df["imovel"].dropna().unique(), default=list(df["imovel"].dropna().unique()))

df_filtrado = df[
    df["sexo"].isin(sexo)
    & df["educacao"].isin(educacao)
    & df["imovel"].isin(imovel)
]

if df_filtrado.empty:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

# --- KPIs ---
total_clientes = len(df_filtrado)
renda_media = df_filtrado["renda"].mean()
emprestimo_medio = df_filtrado["emprestimo"].mean()
taxa_aprovacao = (df_filtrado["aprovacao_emprestimo"] == "Y").mean() * 100
taxa_historico_credito = (df_filtrado["historico_credito"] == 1).mean() * 100

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total de Clientes", f"{total_clientes:,}")
col2.metric("Renda Média", f"R$ {renda_media:,.2f}")
col3.metric("Empréstimo Médio", f"R$ {emprestimo_medio:,.2f}")
col4.metric("Taxa de Aprovação", f"{taxa_aprovacao:.1f}%")
col5.metric("Com Histórico de Crédito", f"{taxa_historico_credito:.1f}%")

st.divider()

# --- Gráficos ---
linha1_col1, linha1_col2 = st.columns(2)

with linha1_col1:
    aprov_sexo = df_filtrado.groupby("sexo")["aprovacao_emprestimo"].apply(
        lambda s: (s == "Y").mean() * 100
    ).reset_index(name="taxa_aprovacao")
    fig_sexo = px.bar(
        aprov_sexo, x="sexo", y="taxa_aprovacao",
        title="Taxa de Aprovação por Sexo (%)",
        labels={"sexo": "Sexo", "taxa_aprovacao": "Taxa de Aprovação (%)"},
    )
    st.plotly_chart(fig_sexo, width='stretch')

with linha1_col2:
    aprov_educacao = df_filtrado.groupby("educacao")["aprovacao_emprestimo"].apply(
        lambda s: (s == "Y").mean() * 100
    ).reset_index(name="taxa_aprovacao")
    fig_educacao = px.bar(
        aprov_educacao, x="educacao", y="taxa_aprovacao",
        title="Taxa de Aprovação por Educação (%)",
        labels={"educacao": "Educação", "taxa_aprovacao": "Taxa de Aprovação (%)"},
    )
    st.plotly_chart(fig_educacao, width='stretch')

linha2_col1, linha2_col2 = st.columns(2)

with linha2_col1:
    fig_renda = px.histogram(
        df_filtrado, x="renda", nbins=30, title="Distribuição de Renda",
        labels={"renda": "Renda"},
    )
    st.plotly_chart(fig_renda, width='stretch')

with linha2_col2:
    fig_scatter = px.scatter(
        df_filtrado, x="renda", y="emprestimo", color="aprovacao_emprestimo",
        title="Renda vs Valor do Empréstimo",
        labels={"renda": "Renda", "emprestimo": "Empréstimo", "aprovacao_emprestimo": "Aprovação"},
    )
    st.plotly_chart(fig_scatter, width='stretch')

fig_imovel = px.bar(
    df_filtrado.groupby("imovel")["aprovacao_emprestimo"].apply(lambda s: (s == "Y").mean() * 100).reset_index(name="taxa_aprovacao"),
    x="imovel", y="taxa_aprovacao",
    title="Taxa de Aprovação por Área do Imóvel (%)",
    labels={"imovel": "Área do Imóvel", "taxa_aprovacao": "Taxa de Aprovação (%)"},
)
st.plotly_chart(fig_imovel, width='stretch')

st.divider()
st.subheader("Dados Filtrados")
st.dataframe(df_filtrado, width='stretch')
