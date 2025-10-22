# Requisitos de instalação (opcional para Google Colab)
# !pip install streamlit plotly pyngrok

import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração inicial da página
st.set_page_config(layout="wide")
st.title("📊 Dashboard de Análise de Vendas Globais")

# Organização de colunas para os gráficos
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7, col8, col9 = st.columns(3)

# ==============================
# 1. Carregamento de dados
# ==============================
try:
    df_vendas = pd.read_csv("VendasGlobais.csv")
    df_fornecedores = pd.read_csv("Fornecedores.csv")
    df_transportadoras = pd.read_csv("Transportadoras.csv")
    df_vendedores = pd.read_csv("Vendedores.csv")
except FileNotFoundError:
    st.error("❌ Erro: Um ou mais arquivos CSV não foram encontrados. "
             "Certifique-se de que todos os arquivos estão no mesmo diretório do script.")
    st.stop()

# Conversão de datas
df_vendas["Data"] = pd.to_datetime(df_vendas["Data"], format="%d/%m/%Y")

# ==============================
# 2. Top 10 Clientes
# ==============================
top_clientes = df_vendas.groupby("ClienteNome")["Vendas"].sum().nlargest(10).reset_index()
fig1 = px.bar(
    top_clientes,
    x="ClienteNome",
    y="Vendas",
    labels={"ClienteNome": "Cliente", "Vendas": "Total de Vendas ($)"},
    title="🏆 Top 10 Clientes por Vendas",
    color_discrete_sequence=px.colors.qualitative.Plotly 
)
col1.plotly_chart(fig1, use_container_width=True)

# ==============================
# 3. Top 3 Países
# ==============================
top_paises = df_vendas.groupby("ClientePaís")["Vendas"].sum().nlargest(3).reset_index()
fig2 = px.bar(
    top_paises,
    x="ClientePaís",
    y="Vendas",
    labels={"x": "País", "y": "Total de Vendas ($)"},
    title="🌍 Top 3 Países por Vendas",
    color_discrete_sequence=px.colors.qualitative.G10 
)
col2.plotly_chart(fig2, use_container_width=True)

# ==============================
# 4. Faturamento por Categoria (Brasil)
# ==============================
vendas_brasil = df_vendas[df_vendas["ClientePaís"] == "Brazil"]
if not vendas_brasil.empty:
    faturamento_categoria = vendas_brasil.groupby("CategoriaNome")["Vendas"].sum().reset_index()
    fig3 = px.pie(
        faturamento_categoria,
        names="CategoriaNome",
        values="Vendas",
        title="Faturamento por Categoria no Brasil",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Safe 
    )
    col3.plotly_chart(fig3, use_container_width=True)
else:
    col3.warning("⚠️ Não há dados de vendas para o Brasil.")

# ==============================
# 5. Frete por Transportadora
# ==============================
df_vendas_transportadoras = pd.merge(
    df_vendas, df_transportadoras, on="TransportadoraID", how="inner"
)
frete_por_transportadora = df_vendas_transportadoras.groupby("TransportadoraNome")["Frete"].sum().reset_index()
fig4 = px.bar(
    frete_por_transportadora,
    x="TransportadoraNome",
    y="Frete",
    labels={"TransportadoraNome": "Transportadora", "Frete": "Total de Frete ($)"},
    title="🚚 Despesa de Frete por Transportadora",
    color_discrete_sequence=px.colors.qualitative.Pastel 
)
col4.plotly_chart(fig4, use_container_width=True)

# ==============================
# 6. Principais Clientes - Men's Shoes (Alemanha)
# ==============================
df_men_shoes_ger = df_vendas[
    (df_vendas["CategoriaDescrição"] == "Men Shoes") &
    (df_vendas["ClientePaís"] == "Germany")
]

if not df_men_shoes_ger.empty:
    vendas_por_cliente = (
        df_men_shoes_ger.groupby("ClienteNome")["Vendas"].sum()
        .nlargest(5).reset_index()
    )
    fig5 = px.bar(
        vendas_por_cliente,
        x="ClienteNome",
        y="Vendas",
        title="Vendas de Calçados Masculinos na Alemanha por Cliente",
        labels={"ClienteNome": "Cliente", "Vendas": "Total de Vendas ($)"},
        color_discrete_sequence=px.colors.qualitative.Dark24 
    )
    fig5.update_layout(xaxis_tickangle=-45)

    with col5:
        st.plotly_chart(fig5, use_container_width=True)
else:
    col5.info("ℹ️ Não foram encontradas vendas de 'Calçados Masculinos' na Alemanha.")

# ==============================
# 7. Descontos por Vendedor (EUA)
# ==============================
vendas_usa = df_vendas[df_vendas["ClientePaís"] == "USA"]
descontos_vendedores = vendas_usa.groupby("VendedorID")["Desconto"].sum().reset_index()
df_descontos = pd.merge(descontos_vendedores, df_vendedores, on="VendedorID", how="inner")

fig6 = px.bar(
    df_descontos,
    x="VendedorNome",
    y="Desconto",
    title="💲 Descontos por Vendedor (EUA)",
    labels={"VendedorNome": "Vendedor", "Desconto": "Total de Descontos ($)"},
    color_discrete_sequence=px.colors.qualitative.Vivid 
)
col6.plotly_chart(fig6, use_container_width=True)

# ==============================
# 8. Fornecedores com Maior Margem (Vestuário Feminino)
# ==============================
df_vest_fem = df_vendas[df_vendas["CategoriaNome"] == "Womens wear"]
if not df_vest_fem.empty:
    margem_fornecedor = df_vest_fem.groupby("FornecedorID")["Margem Bruta"].sum().reset_index()
    df_margem = pd.merge(margem_fornecedor, df_fornecedores, on="FornecedorID", how="inner")

    fig7 = px.bar(
        df_margem,
        x="FornecedorNome",
        y="Margem Bruta",
        title="📈 Fornecedores Maior Lucro (Vestuário Feminino)",
        labels={"FornecedorNome": "Fornecedor", "Margem Bruta": "Margem de Lucro ($)"},
        color_discrete_sequence=px.colors.qualitative.T10
    )
    col7.plotly_chart(fig7, use_container_width=True)
else:
    col7.warning("⚠️ Não há dados de 'Womens wear' na planilha.")

# ==============================
# 9. Vendas Totais por Ano
# ==============================
#Quanto foi vendido em 2009 = 8766629
venda_ano = df_vendas.groupby(df_vendas["Data"].dt.year)["Vendas"].sum().reset_index()
fig8 = px.line(
    venda_ano,
    x="Data",
    y="Vendas",
    markers=True,
    title="📆 Vendas Totais por Ano",
    labels={"Data": "Ano", "Vendas": "Vendas Totais ($)"},
    color_discrete_sequence=["#1f77b4"]
)
col8.plotly_chart(fig8, use_container_width=True)

# ==============================
# 10. Vendas na Europa
# ==============================
paises_europa = ["France", "Germany", "Italy", "Spain", "Portugal"]
df_europa = df_vendas[df_vendas["ClientePaís"].isin(paises_europa)]
vendas_europa = df_europa.groupby("ClientePaís")["Vendas"].sum().reset_index()

fig9 = px.bar(
    vendas_europa,
    x="ClientePaís",
    y="Vendas",
    title="🇪🇺 Vendas na Europa por País",
    labels={"ClientePaís": "País", "Vendas": "Total de Vendas ($)"},
    color_discrete_sequence=px.colors.qualitative.Bold
)
col9.plotly_chart(fig9, use_container_width=True)

# ==============================
# 11. Análise de Calçados Masculinos em 2013
# ==============================
st.markdown("---")
st.header("👞 Análise de Calçados Masculinos em 2013")

df_2013 = df_vendas[
    (df_vendas["CategoriaNome"] == "Men's Footwear") &
    (df_vendas["Data"].dt.year == 2013)
]

if not df_2013.empty:
    top_clientes_2013 = df_2013.groupby("ClienteNome")["Vendas"].sum().nlargest(10)
    vendas_por_cidade = df_2013.groupby("ClienteCidade")["Vendas"].sum().sort_values(ascending=False)

    col9_1, col9_2 = st.columns(2)
    col9_1.subheader("Top 10 Clientes")
    col9_1.dataframe(top_clientes_2013)

    col9_2.subheader("Vendas por Cidade")
    col9_2.dataframe(vendas_por_cidade)
else:
    st.info("ℹ️ Não foram encontradas vendas de 'Calçados Masculinos' em 2013.")

# Para rodar: streamlit run PraticaIE_Streamlit.py