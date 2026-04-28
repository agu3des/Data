# Documentação do Projeto ETL: Northwind Data Warehouse

Este documento descreve a implementação de um ambiente analítico (Data Warehouse) utilizando a base de dados transacional Northwind. O foco principal é o processo de **ETL** desenvolvido para transformar dados relacionais em um modelo **Star Schema** (Esquema Estrela), garantindo a integridade histórica através de **SCD Tipo 2**.

## 1. Arquitetura e Modelagem
O projeto utiliza um modelo **Star Schema** para otimizar a performance de consultas analíticas.

* **Tabelas de Dimensão:** Armazenam o contexto (Quem, Onde, O quê).
    * `dim_cliente`, `dim_funcionarios`, `dim_produto`, `dim_transportadora`, `dim_tempo`.
* **Tabela de Fatos:** Armazena as métricas quantitativas e chaves para as dimensões.
    * `fato_vendas`.
* **Surrogate Keys (SK):** Chaves artificiais inteiras utilizadas para ligar fatos e dimensões, independentes dos IDs dos sistemas de origem.



---

## 2. Passo a Passo do ETL: Dimensões (SCD Tipo 2)

O maior desafio técnico foi a implementação do **SCD (Slowly Changing Dimension) Tipo 2**, que permite rastrear o histórico de alterações.

### 2.1 Configuração Base (O Segredo da Data de Vigência)
Para que as vendas históricas (de 1996 a 1998) encontrassem seus respectivos clientes, configuramos:
* **Min. Year:** `1900` (Garante cobertura total).
* **Start Date Alternative:** `None/Null` (Faz com que o primeiro registro de cada item comece em 01/01/1900 em vez da data de hoje).

### 2.2 Transformação: Dimensão Produto (Desnormalização)
Diferente das outras, esta dimensão foi "achatada" no SQL de origem para evitar múltiplos JOINS no DW:
1.  **Extração:** SQL com `LEFT JOIN` entre `Produtos`, `Categorias` e `Fornecedores`.
2.  **Carga:** Uso do step *Dimension Lookup/Update* mapeando `nome_categoria` e `nome_fornecedor` como campos de **Insert** (SCD2).

### 2.3 Transformação: Dimensão Tempo
Criada de forma programática no Pentaho:
1.  **Gerador de Linhas:** Criamos 5.500 dias.
2.  **Cálculo de SK:** A chave primária é gerada no formato `YYYYMMDD` (Ex: 19970101) para facilitar a leitura humana e performance.

---

## 3. Passo a Passo do ETL: Tabela de Fatos (Vendas)

A `fato_vendas` é o coração do projeto. O fluxo segue esta ordem lógica:

### Etapa 1: Extração e Limpeza
* **Leitura:** Extraímos dados das tabelas `Pedidos` e `Detalhes do Pedido`.
* **Tratamento de Datas:** Resolvemos o erro de driver do PostgreSQL forçando a máscara `yyyy/MM/dd HH:mm:ss.SSS` no step *Select Values*.

### Etapa 2: Cálculos de Negócio e Datas
* **Entrega Prevista:** Calculada via step *Calculator* (`data_pedido + 15 dias`).
* **Métricas Financeiras:** Cálculo do `valor_liquido` subtraindo o desconto do valor bruto (`quantidade * preco`).

### Etapa 3: Geração de Surrogate Keys (SKs)
Transformamos as datas em Inteiros para bater com a `dim_tempo`:
1.  Converter Data para String (`yyyyMMdd`).
2.  Converter String para Inteiro (Usando a máscara `#` para evitar erros de formatação regional/Locale).
3.  Tratamento de Nulos: Datas de envio vazias são convertidas para o SK padrão `19000101`.

### Etapa 4: Lookups Dimensionais
Buscamos a SK correta em cada dimensão usando a data do pedido como referência de vigência:
* **Configuração Crítica:** Alteração do campo de versão padrão de `version` para adequar ao banco de dados, usando o truque de marcar "Update" temporariamente para editar o campo.

---

## 4. Tecnologias Utilizadas
* **Pentaho Data Integration (PDI):** Orquestração dos fluxos de dados.
* **PostgreSQL:** Motor de banco de dados para o DW.
* **SQL Power Architect:** Desenho do modelo dimensional.

---

### Entendendo a Lógica SCD Tipo 2 na Prática
Abaixo, você pode explorar como o banco de dados se comporta quando um atributo (como a cidade de um cliente) muda. Note como o sistema "encerra" um registro e "abre" outro para manter a história viva.

```json?chameleon
{"component":"LlmGeneratedComponent","props":{"height":"700px","prompt":"Crie um simulador interativo de SCD Tipo 2 (Slowly Changing Dimension). O usuário deve ver uma tabela representando a 'dim_cliente'. Inicialize com um registro: SK=1, ID=ALFKI, Nome=Alfreds Futterkiste, Cidade=Berlin, Versao=1, Inicio=1900-01-01, Fim=9999-12-31. Ofereça um controle para 'Mudar Cidade do Cliente'. Quando o usuário mudar a cidade para 'Frankfurt', o widget deve simular o processo de ETL: 1. O registro atual (Versão 1) deve ter sua Data de Fim atualizada para a data de hoje. 2. Um novo registro (Versão 2) deve ser inserido com a nova cidade, Versão=2, Inicio=Hoje e Fim=9999-12-31. Mostre visualmente a tabela atualizando. Adicione uma explicação textual simples sobre por que isso é importante para a integridade dos relatórios históricos de vendas.","id":"im_45ebba551b4983c4"}}
```