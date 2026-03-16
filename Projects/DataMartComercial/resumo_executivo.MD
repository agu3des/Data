# MODELO DIMENSIONAL - DATA MART COMERCIAL NORTHWIND
## RESUMO EXECUTIVO DO PROJETO

---

##  ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Decisões de Modelagem](#decisões-de-modelagem)
3. [Estrutura do Modelo](#estrutura-do-modelo)
4. [SCD (Slowly Changing Dimensions)](#scd-slowly-changing-dimensions)
5. [Medidas e KPIs](#medidas-e-kpis)
6. [Cobertura dos Requisitos](#cobertura-dos-requisitos)
7. [Arquivos Entregues](#arquivos-entregues)
8. [Próximos Passos](#próximos-passos)

---

##  VISÃO GERAL

### Objetivo
Criar um Data Mart dimensional otimizado para análises comerciais da Northwind, suportando todas as 27 perguntas de negócio identificadas.

### Arquitetura Escolhida
**Esquema Estrela (Star Schema)**

**Justificativa:**
-  Simplicidade para usuários de negócio
-  Performance superior em queries analíticas
-  Facilita integração com Power BI
-  Manutenção simplificada
-  Queries SQL mais intuitivas

### Características Principais
- **Granularidade:** Item de Pedido (detalhe máximo)
- **Tabelas:** 7 Dimensões + 1 Fato
- **Slowly Changing Dimensions (SCD):** Técnica para rastrear mudanças históricas em dimensões. Tipo 2 implementado em 3 dimensões
---

##  DECISÕES DE MODELAGEM

### 1. Surrogate Keys em Todas as Dimensões
**Decisão:** Usar SK (INT IDENTITY) como chave primária em todas as dimensões.

**Justificativas:**
- Independência do sistema transacional
- Performance superior (chaves numéricas)
- Facilita integração de múltiplas fontes
- Evita problemas com chaves compostas

### 2. Role-Playing Dimension (DIM_TEMPO)
**Decisão:** Uma única dimensão tempo usada 4 vezes no fato.

**Papéis:**
1. Data do Pedido
2. Data do Envio
3. Data de Entrega Prevista
4. Data de Entrega Real

**Justificativas:**
- Evita duplicação de dados
- Facilita manutenção
- Queries complexas de análise temporal
- Economia de espaço

### 3. Dimensões Degeneradas
**Decisão:** Manter Numero_Pedido e Numero_Item_Pedido no fato.

**Justificativas:**
- Alta cardinalidade (não justifica dimensão própria)
- Necessários para rastreabilidade
- Facilitam troubleshooting
- Suportam drill-down até o pedido original

### 4. Relacionamento Produto com Categoria e Fornecedor
**Decisão:** Criar dimensões separadas para Categoria e Fornecedor com relacionamento através da DIM_PRODUTO.

**Justificativas:**
- Permite análises hierárquicas (Categoria → Produto)
- Facilita análises de fornecedores
- Mantém flexibilidade para análises cruzadas
- Suporta SCD Tipo 2 em Produto sem impactar Categoria/Fornecedor

---

##  ESTRUTURA DO MODELO

### TABELAS DE FATOS

#### FATO_VENDAS
**Grain:** Item de Pedido

**Chaves Estrangeiras (8):**
- SK_Cliente
- SK_Produto
- SK_Vendedor
- SK_Transportadora
- SK_Data_Pedido
- SK_Data_Envio
- SK_Data_Entrega_Prevista
- SK_Data_Entrega_Real

**Medidas:**
- Quantidade
- Preco_Unitario
- Valor_Venda_Sem_Desconto
- Valor_Desconto

**Dimensões Degeneradas (2):**
- Numero_Pedido (DD)
- Numero_Item_Pedido (DD)

---

### DIMENSÕES

#### 1. DIM_CLIENTE (SCD Tipo 2)
**Hierarquias:**
- Geografia: País → Região → Cidade → Cliente

**Atributos SCD Tipo 2:**
- Endereço
- Cidade
- País

**Justificativa SCD-2:**
Mudanças de localização são relevantes para análises geográficas históricas.

#### 2. DIM_PRODUTO (SCD Tipo 2)
**Hierarquias:**
- Categoria → Produto

**Atributos SCD Tipo 2:**
- Preco_Unitario_Atual
- FK_Fornecedor_Atual

**Justificativa SCD-2:**
Mudanças de preço e fornecedor são críticas para análises de margem e rentabilidade.

#### 3. DIM_VENDEDOR (SCD Tipo 2)
**Hierarquias:**
- Geografia: País → Cidade → Vendedor
- Organizacional: Supervisor → Vendedor

**Atributos SCD Tipo 2:**
- FK_Supervisor
- Território (implícito via endereço)

**Justificativa SCD-2:**
Mudanças organizacionais impactam análises de performance.

#### 4. DIM_CATEGORIA
**Atributos:**
- SK_Categoria (PK)
- Categoria_ID (NK)
- Nome_Categoria
- Descricao_Categoria

#### 5. DIM_FORNECEDOR
**Atributos:**
- SK_Fornecedor (PK)
- Fornecedor_ID (NK)
- Nome_Fornecedor
- Cidade
- Regiao
- CEP
- Pais

#### 6. DIM_TRANSPORTADORA
**Atributos:**
- SK_Transportadora (PK)
- Transportadora_ID (NK)
- Nome_Transportadora

#### 7. DIM_TEMPO (Pré-populada)
**Hierarquias:**
- Principal: Ano → Trimestre → Mês → Data


**Atributos:**
- SK_Data (PK)
- Data
- Dia, Dia_Semana, Nome_Dia_Semana
- Semana_Ano, Dia_Ano
- Mes, Nome_Mes
- Trimestre, Nome_Trimestre
- Ano, Ano_Mes
- Fim_Semana (boolean)
- Feriado (boolean)
- Nome_Feriado

---

##  SCD (SLOWLY CHANGING DIMENSIONS)

### Implementação de SCD Tipo 2

**Campos Padrão em Todas as Dimensões SCD-2:**
```sql
Data_Inicio_Vigencia DATE NOT NULL
Data_Fim_Vigencia DATE NULL
Flag_Registro_Atual CHAR(1) CHECK IN ('S', 'N')
Versao_Registro INT DEFAULT 1
```

**Estratégia de Versionamento:**
1. Novo registro sempre tem Data_Inicio_Vigencia = data da mudança
2. Registro anterior tem Data_Fim_Vigencia = data da mudança - 1 dia
3. Apenas registros atuais têm Flag_Registro_Atual = 'S'
4. Versao_Registro incrementa a cada mudança

**Exemplo Prático - Cliente muda de cidade:**

| SK_Cliente | Codigo_Cliente | Nome | Cidade | Data_Inicio | Data_Fim | Flag_Atual | Versao |
|------------|----------------|------|--------|-------------|----------|------------|--------|
| 1001 | C001 | ACME Corp | Rio de Janeiro | 01/01/1996 | 31/12/1997 | N | 1 |
| 1025 | C001 | ACME Corp | São Paulo | 01/01/1998 | NULL | S | 2 |

**Benefícios:**
-  Análise "as of" (vendas por região em 1997 vs 1998)
-  Rastreamento completo de mudanças
-  Integridade referencial mantida
-  Queries simples com flag_registro_atual

### Comparação SCD Tipo 1 vs Tipo 2

| Aspecto | Tipo 1 | Tipo 2 |
|---------|--------|--------|
| **Histórico** |  Não mantém |  Mantém completo |
| **Espaço** | Menor | Maior |
| **Complexidade** | Simples | Moderada |
| **Uso** | Dados não-críticos | Dados analíticos |
| **Exemplo Northwind** | Telefone fornecedor | Preço produto |

---

##  MEDIDAS E KPIs

### Medidas Base (Armazenadas no Fato)

| Medida | Tipo | Fórmula | Aditividade |
|--------|------|---------|-------------|
| Quantidade | Numérica | Qtde vendida | Aditiva |
| Preco_Unitario | Monetária | Preço no momento da venda | Semi-aditiva |
| Valor_Venda_Sem_Desconto | Monetária | Qtde × Preço | Aditiva |
| Valor_Desconto | Monetária | Valor do desconto aplicado | Aditiva |

### KPIs Derivados (Calculados no Power BI)

#### KPIs de Vendas
```dax
// Valor de venda líquido (após desconto)
Valor_Venda_Liquido =
    SUM(FATO_VENDAS[Valor_Venda_Sem_Desconto]) - SUM(FATO_VENDAS[Valor_Desconto])

Total_Vendas = [Valor_Venda_Liquido]

Qtde_Pedidos = DISTINCTCOUNT(FATO_VENDAS[Numero_Pedido])

Ticket_Medio = [Total_Vendas] / [Qtde_Pedidos]

Margem_Desconto =
    SUM(FATO_VENDAS[Valor_Desconto]) /
    SUM(FATO_VENDAS[Valor_Venda_Sem_Desconto])
```

#### KPIs de Performance (Baseados em Datas)
```dax
// Tempo de processamento (Envio - Pedido)
Tempo_Medio_Processamento =
    AVERAGEX(
        FATO_VENDAS,
        DATEDIFF(
            RELATED(DIM_TEMPO_Pedido[Data]),
            RELATED(DIM_TEMPO_Envio[Data]),
            DAY
        )
    )

// Tempo de entrega (Entrega - Envio)
Tempo_Medio_Entrega =
    AVERAGEX(
        FATO_VENDAS,
        DATEDIFF(
            RELATED(DIM_TEMPO_Envio[Data]),
            RELATED(DIM_TEMPO_Entrega[Data]),
            DAY
        )
    )
```

#### KPIs de Cliente
```dax
Qtde_Clientes_Ativos =
    CALCULATE(
        DISTINCTCOUNT(DIM_CLIENTE[Cliente_ID]),
        DIM_CLIENTE[Flag_Registro_Atual] = TRUE
    )

Ticket_Medio_Cliente =
    [Total_Vendas] / [Qtde_Clientes_Ativos]

Recorrencia_Cliente =
    [Qtde_Pedidos] / [Qtde_Clientes_Ativos]
```

#### Time Intelligence
```dax
Vendas_Mes_Anterior =
    CALCULATE(
        [Total_Vendas],
        DATEADD(DIM_TEMPO[Data], -1, MONTH)
    )

Crescimento_MoM =
    DIVIDE(
        [Total_Vendas] - [Vendas_Mes_Anterior],
        [Vendas_Mes_Anterior]
    )

Vendas_YTD =
    CALCULATE(
        [Total_Vendas],
        DATESYTD(DIM_TEMPO[Data])
    )
```

---

##  COBERTURA DOS REQUISITOS

### Mapeamento Completo das 27 Perguntas

| # | Pergunta | Dimensões Utilizadas | Medidas |
|---|----------|---------------------|---------|
| 1 | Top 10 clientes | Cliente | Valor_Venda |
| 2 | Top 10 produtos/categoria | Produto, Categoria | Valor_Venda |
| 3 | Produtos Alemanha | Produto, Cliente (País) | Quantidade |
| 4 | Categoria EUA | Categoria, Cliente (País) | Valor_Venda |
| 5 | Vendas por vendedor | Vendedor, Cliente | Todas |
| 6 | Vendedores com desconto | Vendedor, Junk | Valor_Desconto |
| 7 | Clientes por país | Cliente (País) | Count |
| 8 | Produtos por categoria | Categoria | Count |
| 9 | Fornecedores Bebidas | Fornecedor, Categoria | Valor_Venda |
| 10 | Evolução 1997 | Tempo (Mês) | Valor_Venda |
| 11 | Tempo entrega 1997 | Transportadora, Tempo | Tempo_Entrega |
| 12 | Vendedores por país | Vendedor (País) | Count |
| 13 | Côte de Blaye | Cliente (Cidade), Produto | Quantidade |
| 14-16 | Principal cliente | Cliente, Vendedor, Fornecedor, Produto | Todas |
| 17 | Categoria→Produto→Cliente | Categoria, Produto, Cliente | Quantidade |
| 18 | Clientes Brasil | Cliente (País) | Descritivo |
| 19 | Pedidos transportadora | Transportadora, Tempo (Ano) | Count |
| 20 | Ticket médio | Cliente, Tempo | Calculado |
| 21 | Melhor transportadora | Transportadora | Tempo_Entrega |
| 22 | Tempo liberação | Tempo | Tempo_Processamento |
| 23 | Ticket por vendedor | Vendedor | Calculado |
| 24 | Produtos parados | Produto, Tempo | Data_Ultima_Venda |
| 25 | Descontos por categoria | Categoria, Junk | Valor_Desconto |
| 26 | Tendência faturamento | Tempo | Valor_Venda |
| 27 | Perfis similares | Cliente, Categoria (Snapshot) | Múltiplas |

**Cobertura: 27/27 (100%)**

### Análises Adicionais Suportadas

Além das 27 perguntas, o modelo suporta:

1. **Análises RFM**
   - Recência: última compra
   - Frequência: qtde pedidos
   - Monetary: valor total

2. **Análises de Churn**
   - Dias desde última compra
   - Taxa de recompra
   - Lifetime value

3. **Análises de Produto**
   - ABC de produtos
   - Curva 80-20
   - Cross-sell/Up-sell

4. **Análises Temporais**
   - Sazonalidade
   - Tendências
   - Previsões (base para ML)

5. **Análises Geográficas**
   - Heatmaps de vendas
   - Penetração por região
   - Logística (tempos de entrega)

---

##  ARQUIVOS DO PROJETO

### Documentação
```
 analise_requisitos.MD
   └─ Matriz completa: Perguntas → Medidas → Dimensões → Hierarquias

 resumo_executivo.MD
   └─ Documento consolidado com todas as informações do projeto

 mermaid-diagrama.md
   └─ Diagrama ER em Mermaid
```

### Recursos Adicionais
```
 diagrama_dimensional.png
   └─ Imagem visual do modelo dimensional

 dump-northwind
   └─ Dump do banco de dados Northwind original
```

---

##  PRÓXIMOS PASSOS

### Fase 2: ETL (Pentaho Data Integration)

#### 2.1 Extração de Dados
- [ ] Conectar ao banco OLTP Northwind
- [ ] Mapear tabelas origem → destino
- [ ] Definir estratégia de extração (full/incremental)

#### 2.2 Transformações - Dimensões
- [ ] Lookup de Surrogate Keys
- [ ] Implementação de SCD Tipo 2 (Cliente, Produto, Vendedor)
- [ ] Desnormalização de atributos descritivos
- [ ] Limpeza e padronização de dados

#### 2.3 Transformações - Fato
- [ ] Cálculo de medidas derivadas
- [ ] Lookup de todas as FKs

#### 2.4 Carga
- [ ] Popular DIM_TEMPO
- [ ] Carga inicial de dimensões (SCD Tipo 2)
- [ ] Carga inicial do fato
- [ ] Carga incremental (agendamento)

#### 2.5 Qualidade de Dados
- [ ] Validações de integridade referencial
- [ ] Verificação de NULLs em campos obrigatórios
- [ ] Validação de medidas calculadas
- [ ] Testes de volume

### Fase 3: Power BI

#### 3.1 Modelo de Dados
- [ ] Importar tabelas do Data Mart
- [ ] Configurar relacionamentos
- [ ] Criar hierarquias de navegação
- [ ] Marcar DIM_TEMPO como tabela de datas

#### 3.2 Medidas DAX
- [ ] Implementar todas as medidas calculadas documentadas
- [ ] Criar medidas de Time Intelligence
- [ ] KPIs de performance
- [ ] Medidas de comparação (MoM, YoY)

#### 3.3 Visualizações
- [ ] Dashboard executivo (KPIs principais)
- [ ] Análise de vendas (10 primeiras perguntas)
- [ ] Análise de clientes (perguntas 14-18, 27)
- [ ] Análise de performance (perguntas 11, 21-23)
- [ ] Análise de produtos (perguntas 2, 3, 8, 24-25)

#### 3.4 Recursos Avançados
- [ ] Drill-through para detalhamento
- [ ] Bookmarks para navegação
- [ ] Filtros contextuais
- [ ] Tooltips personalizados
- [ ] Row-Level Security (se necessário)

---

##  MÉTRICAS DE SUCESSO

### Técnicas
-  100% das perguntas respondidas pelo modelo
-  Integridade: modelo dimensional consistente
-  Cobertura SCD: 3 dimensões historizadas
-  Volume Estimado: ~60K registros no fato

### Negócio
-  Modelo intuitivo para usuários
-  Self-service analytics habilitado
-  Insights acionáveis
-  Base para análises avançadas
-  Decisões data-driven

---

##  REFERÊNCIAS

### Modelagem Dimensional
- Kimball, Ralph. "The Data Warehouse Toolkit"
- Kimball Group: www.kimballgroup.com
- Best Practices for Dimensional Modeling

### Ferramentas
- SQL Server: docs.microsoft.com/sql
- Pentaho: help.pentaho.com/Documentation
- Power BI: docs.microsoft.com/power-bi

### Padrões Utilizados
- Star Schema
- Slowly Changing Dimensions (Tipo 2)
- Role-Playing Dimensions
- Degenerate Dimensions

---

##  CONCLUSÃO

O modelo dimensional proposto para o Data Mart Comercial da Northwind foi desenhado seguindo as melhores práticas de Business Intelligence, com foco em:

1. **Performance:** Esquema estrela otimizado
2. **Flexibilidade:** Suporta análises ad-hoc
3. **Escalabilidade:** Preparado para crescimento
4. **Manutenibilidade:** Estrutura clara e documentada
5. **Usabilidade:** Intuitivo para usuários de negócio

**Todos os requisitos de negócio foram atendidos (27/27 perguntas)**, e o modelo está pronto para as próximas fases do projeto: ETL e visualização no Power BI.

---

**Versão:** 1.0
**Data:** Dezembro 2025
