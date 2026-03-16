```
erDiagram
    FATO_VENDAS ||--o{ DIM_CLIENTE : "SK_Cliente"
    FATO_VENDAS ||--o{ DIM_PRODUTO : "SK_Produto"
    FATO_VENDAS ||--o{ DIM_VENDEDOR : "SK_Vendedor"
    FATO_VENDAS ||--o{ DIM_TRANSPORTADORA : "SK_Transportadora"
    FATO_VENDAS ||--o{ DIM_TEMPO : "SK_Data_Pedido"
    FATO_VENDAS ||--o{ DIM_TEMPO : "SK_Data_Envio"
    FATO_VENDAS ||--o{ DIM_TEMPO : "SK_Data_Entrega_Prevista"
    FATO_VENDAS ||--o{ DIM_TEMPO : "SK_Data_Entrega_Real"
    DIM_PRODUTO ||--o{ DIM_CATEGORIA : "SK_Categoria"
    DIM_PRODUTO ||--o{ DIM_FORNECEDOR : "SK_Fornecedor"

    FATO_VENDAS {
        int SK_Cliente FK
        int SK_Produto FK
        int SK_Vendedor FK
        int SK_Transportadora FK
        int SK_Data_Pedido FK
        int SK_Data_Envio FK
        int SK_Data_Entrega_Prevista FK
        int SK_Data_Entrega_Real FK
        string Numero_Pedido "DD"
        int Numero_Item_Pedido "DD"
        decimal Quantidade
        decimal Preco_Unitario
        decimal Valor_Venda_Sem_Desconto
        decimal Valor_Desconto

    }

    DIM_CLIENTE {
        int SK_Cliente PK
        string Cliente_ID "NK"
        string Nome_Empresa
        string Cidade
        string Regiao_Estado
        string PaisISO
        date Data_Inicio_Vigencia "SCD2"
        date Data_Fim_Vigencia "SCD2"
        boolean Flag_Registro_Atual "SCD2"
    }

    DIM_PRODUTO {
        int SK_Produto PK
        string Produto_ID "NK"
        string Nome_Produto
        int SK_Categoria FK
        int SK_Fornecedor FK
        decimal Preco_Unitario
        int Unidades_Estoque
        int Unidades_Pedidas
        int Nivel_Reposicao
        boolean Descontinuado
        date Data_Inicio_Vigencia "SCD2"
        date Data_Fim_Vigencia "SCD2"
        boolean Flag_Registro_Atual "SCD2"
    }

    DIM_CATEGORIA {
        int SK_Categoria PK
        string Categoria_ID "NK"
        string Nome_Categoria
        string Descricao_Categoria
    }

    DIM_FORNECEDOR {
        int SK_Fornecedor PK
        string Fornecedor_ID "NK"
        string Nome_Fornecedor
        string Cidade
        string Regiao
        string Pais
    }

    DIM_VENDEDOR {
        int SK_Vendedor PK
        string Vendedor_ID "NK"
        string Sobrenome
        string Nome
        date Data_Nascimento
        string Cidade
        string Regiao
        string Pais
        string Nome_Supervisor
        date Data_Inicio_Vigencia "SCD2"
        date Data_Fim_Vigencia "SCD2"
        boolean Flag_Registro_Atual "SCD2"
    }

    DIM_TRANSPORTADORA {
        int SK_Transportadora PK
        string Transportadora_ID "NK"
        string Nome_Transportadora
    }

    DIM_TEMPO {
        int SK_Data PK
        date Data
        int Dia
        int Dia_Semana
        string Nome_Dia_Semana
        int Semana_Ano
        int Dia_Ano
        int Mes
        string Nome_Mes
        int Trimestre
        string Nome_Trimestre
        int Ano
        int Ano_Mes
        boolean Fim_Semana
        boolean Feriado
        string Nome_Feriado
    }
```