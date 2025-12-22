import pandas as pd


caminho_arquivo = "enem/PARTICIPANTES_2024.csv"

# -----------------------------------------------------------
# 1. Leitura do CSV
# -----------------------------------------------------------
# Observações:
# - O separador oficial é ';'
# - A codificação 'latin-1' evita erros com acentos (ex: "São Luiz")
# - low_memory=False impede warnings ao lidar com colunas mistas
df = pd.read_csv(
    caminho_arquivo,
    sep=';',
    encoding='latin-1',
    low_memory=False
)

# # -----------------------------------------------------------
# # 2. Informações gerais do DataFrame
# # -----------------------------------------------------------
# print("📏 Dimensões do dataset (linhas, colunas):", df.shape)
# print("\n🧩 Colunas disponíveis:")
# print(df.columns.tolist())

# # -----------------------------------------------------------
# # 3. Visualização inicial
# # -----------------------------------------------------------
# print("\n👀 Primeiras 5 linhas:")
# print(df.head())

# # -----------------------------------------------------------
# # 4. Tipos de dados
# # -----------------------------------------------------------
# print("\n🔢 Tipos de dados por coluna:")
# print(df.dtypes)

# # -----------------------------------------------------------
# # 5. Valores ausentes (percentual)
# # -----------------------------------------------------------
# print("\n🚫 Percentual de valores ausentes por coluna:")
# print(df.isnull().mean().round(3) * 100)

# # -----------------------------------------------------------
# # 6. Estatísticas descritivas básicas (numéricas)
# # -----------------------------------------------------------
# print("\n📈 Estatísticas descritivas (numéricas):")
# print(df.describe())

# # -----------------------------------------------------------
# # 7. Estatísticas para variáveis categóricas (exemplo)
# # -----------------------------------------------------------
# colunas_categoricas = ['TP_SEXO', 'TP_FAIXA_ETARIA', 'TP_COR_RACA', 'Q006', 'Q007', 'Q023']

# for col in colunas_categoricas:
#     if col in df.columns:
#         print(f"\n📊 Distribuição de valores - {col}:")
#         print(df[col].value_counts(dropna=False))

# # -----------------------------------------------------------
# # 8. Correção opcional de encoding (caso apareçam caracteres quebrados)
# # -----------------------------------------------------------
# # Exemplo: transformar "S�o Luiz Gonzaga" → "São Luiz Gonzaga"
# df['NO_MUNICIPIO_PROVA'] = df['NO_MUNICIPIO_PROVA'].str.encode('latin1', 'ignore').str.decode('utf-8', 'ignore')

# print("\n✅ Verificação de nomes de municípios (amostra):")
# print(df['NO_MUNICIPIO_PROVA'].head())


# Filtrar apenas participantes da Paraíba



novo_nome_colunas = {
    'NU_INSCRICAO': 'inscricao',
    'CO_MUNICIPIO_PROVA': 'cod_municipio_prova',
    'NO_MUNICIPIO_PROVA': 'municipio_prova',

    'TP_FAIXA_ETARIA': 'faixa_etaria',
    'TP_SEXO': 'sexo',
    'TP_ESTADO_CIVIL': 'estado_civil',
    'TP_COR_RACA': 'cor_raca',

    'TP_ST_CONCLUSAO': 'status_conclusao',
    'TP_ANO_CONCLUIU': 'ano_conclusao',
    'TP_ENSINO': 'tipo_ensino',
    'IN_TREINEIRO': 'treineiro',

    # Socioeconômicas
    'Q001': 'esc_mae',
    'Q002': 'esc_pai',
    'Q003': 'trab_mae',
    'Q004': 'trab_pai',
    'Q005': 'pessoas_residencia',
    'Q006': 'possui_renda',
    'Q007': 'renda_mensal_familiar',
    'Q008': 'contrata_servico_domestico',
    'Q009': 'tem_banheiro',
    'Q010': 'tem_quarto',
    'Q011': 'tem_carro',
    'Q012': 'tem_motocicleta',
    'Q013': 'tem_geladeira',
    'Q014': 'tem_freezer',
    'Q015': 'tem_maquina_de_lavar',
    'Q016': 'tem_micro_ondas',
    'Q017': 'tem_aspirador_de_po',
    'Q018': 'tem_tv',
    'Q019': 'tem_tv_por_assinatura',
    'Q020': 'tem_internet_wifi',
    'Q021': 'tem_computador_notebook',
    'Q022': 'tem_celular',
    'Q023': 'tipo_escola'
}


colunas_renomeadas = [
    'inscricao','cod_municipio_prova','municipio_prova','faixa_etaria','sexo','estado_civil','cor_raca',
    'status_conclusao','ano_conclusao','tipo_ensino','treineiro','esc_mae','esc_pai','trab_mae','trab_pai',
    'pessoas_residencia','possui_renda','renda_mensal_familiar','contrata_servico_domestico','tem_banheiro',
    'tem_quarto','tem_carro','tem_motocicleta','tem_geladeira','tem_freezer','tem_maquina_de_lavar',
    'tem_micro_ondas','tem_aspirador_de_po','tem_tv','tem_tv_por_assinatura','tem_internet_wifi',
    'tem_computador_notebook','tem_celular','tipo_escola'
]

df = df.rename(columns=novo_nome_colunas)

# Filtrar apenas participantes da Paraíba
df_pb_enem_2024 = df[df["SG_UF_PROVA"] == "PB"] 

# Selecionar apenas as colunas de interesse
df_pb_enem_2024 = df_pb_enem_2024[colunas_renomeadas]


# Tratamento de valores ausentes
for col in df_pb_enem_2024.select_dtypes(include='object').columns:
     df_pb_enem_2024[col] = df_pb_enem_2024[col].fillna('Não informado')

for col in df_pb_enem_2024.select_dtypes(exclude='object').columns:
    df_pb_enem_2024[col] = df_pb_enem_2024[col].fillna(df_pb_enem_2024 [col].median())



# print(df_pb_enem_2024.columns)



# Salvar o DataFrame tratado em um novo arquivo CSV
df_pb_enem_2024.to_csv("enem/enem_pb_2024_tratado.csv", index=False)


