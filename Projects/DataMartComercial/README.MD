#  PROJETO DATA MART COMERCIAL - NORTHWIND

##  Visão Geral do Projeto

Este repositório contém toda a documentação do projeto de Business Intelligence da Northwind: **Modelagem Dimensional para Data Mart Comercial**.

### Objetivo
Criar um Data Mart dimensional otimizado para análises comerciais, respondendo a 27 perguntas de negócio identificadas pela área comercial da Northwind.

### Estrutura do Projeto
O projeto está dividido em etapas:
- **Etapa 1:** Modelagem Dimensional
- **Etapa 2:** ETL (Pentaho)
- **Etapa 3:** Visualização (Power BI)

---

##  Estrutura de Arquivos

###  Documentação Principal

| Arquivo | Descrição | Quando Usar |
|---------|-----------|-------------|
| **Readme.MD** | Este arquivo - índice do projeto | Começar por aqui! |
| **resumo_executivo.MD** | Documento completo consolidado | Visão geral completa do projeto |
| **mermaid-diagrama.md** | Diagrama ER em Mermaid | Visualizar relacionamentos |

### Análise e Requisitos

| Arquivo | Descrição | Quando Usar |
|---------|-----------|-------------|
| **analise_requisitos.MD** | Matriz completa: Perguntas → Medidas → Dimensões | Entender os requisitos de negócio |

### Recursos Adicionais

| Arquivo | Descrição |
|---------|-----------|
| **diagrama_dimensional.png** | Imagem visual do modelo dimensional |
| **dump-northwind** | Dump do banco de dados Northwind original |

---

##  Guia de Início Rápido

### Para Gestores e Patrocinadores

1. **Comece por aqui:** [resumo_executivo.MD](resumo_executivo.MD)
   - Visão completa do projeto
   - Justificativas das decisões
   - Próximos passos

2. **Visualização:** [diagrama_dimensional.png](diagrama_dimensional.png)
   - Diagrama visual do modelo
   - Hierarquias dimensionais
   - Características principais

### Para Arquitetos e Consultores

1. **Análise de Requisitos:** [analise_requisitos.MD](analise_requisitos.MD)
   - 27 perguntas de negócio mapeadas
   - Medidas identificadas
   - Dimensões e hierarquias

2. **Especificação Técnica:** [resumo_executivo.MD](resumo_executivo.MD)
   - Detalhamento completo de cada dimensão e fato
   - Justificativas técnicas
   - SCD implementados
   - Estimativas de volume

3. **Diagrama ER:** [diagrama_dimensional.svg](mermaid-diagrama)
   - Diagrama em formato Mermaid
   - Relacionamentos entre tabelas

---

##  Modelo Dimensional - Visão Resumida

### Arquitetura
**Esquema Estrela** com 7 dimensões e 1 fato

### Dimensões

| Dimensão | Tipo SCD | Hierarquias |
|----------|----------|-------------|
| **DIM_CLIENTE** | Tipo 2   | País → Região → Cidade → Cliente |
| **DIM_PRODUTO** | Tipo 2   | Categoria → Produto |
| **DIM_VENDEDOR** | Tipo 2   | País → Cidade → Vendedor<br>Supervisor → Vendedor |
| **DIM_FORNECEDOR** | Tipo 1 | País → Cidade → Fornecedor |
| **DIM_TRANSPORTADORA** | Tipo 1   |  - |
| **DIM_TEMPO** | -        | Ano → Trimestre → Mês → Data |
| **DIM_JUNK** | -        | - |

### Fatos

| Fato | Grain | Medidas                       |
|------|-------|-------------------------------|
| **FATO_VENDAS** | Item de Pedido | 10 medidas (valores e tempos) |

### SCD (Slowly Changing Dimensions)

**Tipo 2 - Historização Completa:**
-  Cliente (endereço, cidade, país)
-  Produto (preço, fornecedor)
-  Vendedor (supervisor, território)

**Tipo 1 - Sobrescrever:**
-  Fornecedor (telefone, contato)
-  Transportadora (telefone)

---

##  Conceitos Implementados

###  Estrela (Star Schema)
- Fato central cercado por dimensões
- Performance superior
- Simplicidade para usuários

### Snowflake Parcial (Categoria e Fornecedor)
- **Categoria** e **Fornecedor** normalizados a partir de **DIM_PRODUTO** por serem propriedades intrínsecas e estáveis do produto (1 produto = 1 categoria = 1 fornecedor). Isso reduz redundância, centraliza manutenção e atende 100% dos requisitos (#9, #15) sem impactar performance significativamente, mantendo o modelo predominantemente Star Schema.

###  Role-Playing Dimension
- DIM_TEMPO usada 4 vezes
- Evita duplicação
- Análises temporais ricas

### Degenerate Dimensions
- Numero_Pedido no fato
- Alta cardinalidade
- Rastreabilidade
---

##  Cobertura de Requisitos

### 27 Perguntas de Negócio - 100% Atendidas

| Categoria | Perguntas | Status |
|-----------|-----------|--------|
| **Vendas** | 1-4, 17, 26 | ✅ 6/6 |
| **Vendedores** | 5, 6, 12, 14, 23 | ✅ 5/5 |
| **Clientes** | 7, 13, 18, 20, 27 | ✅ 5/5 |
| **Produtos** | 2, 3, 8, 16, 24, 25 | ✅ 6/6 |
| **Fornecedores** | 9, 15 | ✅ 2/2 |
| **Transportadoras** | 11, 19, 21 | ✅ 3/3 |
| **Performance** | 10, 22 | ✅ 2/2 |

**TOTAL: 27/27 (100%)**

---

##  Medidas e KPIs Principais

### Medidas Base (Armazenadas no Fato)
-  Valor_Venda_Liquido (principal)
-  Quantidade
-  Valor_Desconto
-  Tempo_Entrega_Dias
-  Tempo_Processamento_Dias

---

##  Ferramentas e Tecnologias

### Bancos de Dados Suportados
-  **SQL Server 2016+** (recomendado)
-  PostgreSQL 12+
-  MySQL 8+ (ajustes menores)
-  Oracle 12c+ (ajustes menores)

### Ferramentas ETL
-  **Pentaho Data Integration** (definido no projeto)
-  SQL Server Integration Services (SSIS)
-  Apache Airflow
-  Talend

### Ferramentas BI
-  **Power BI** (definido no projeto)
-  Tableau
-  Qlik Sense
-  Looker

---

##  Referências e Boas Práticas

### Modelagem Dimensional
- Kimball, Ralph. "The Data Warehouse Toolkit"
- Kimball Group: www.kimballgroup.com
- Best Practices for Star Schema Design

### Padrões Utilizados
-  Star Schema (Esquema Estrela)
-  Slowly Changing Dimensions (Tipos 1 e 2)
-  Role-Playing Dimensions
-  Degenerate Dimensions
-  Surrogate Keys

---

## 📝 Histórico de Versões

| Versão | Data | Responsável | Alterações |
|--------|------|-------------|------------|
| 1.0 | Dez/2025 | Consultoria BI | Versão inicial - Modelagem completa |
| 1.1 | - | - | ETL Pentaho (planejado) |
| 1.2 | - | - | Power BI (planejado) |

---
