# Análise de Requisitos - Northwind BI

## Matriz Completa de Requisitos

| # | Pergunta | Medidas | Dimensões | Hierarquia | Observações |
|---|----------|---------|-----------|------------|-------------|
| 1 | Ranking com os 10 maiores clientes (vendas) | Valor de Venda, Quantidade Vendida | Cliente, Tempo | Cliente > País > Cidade | Agregação por cliente |
| 2 | Ranking com os 10 maiores produtos (vendas) por categoria | Valor de Venda, Quantidade Vendida | Produto, Categoria | Categoria > Produto | Análise dentro de cada categoria |
| 3 | Relação dos produtos mais vendidos para os clientes da Alemanha | Quantidade Vendida, Valor de Venda | Produto, Cliente (País) | País > Cliente > Produto | Filtro: País = Alemanha |
| 4 | Categoria de produto mais representativa (vendas) nos clientes dos EUA | Valor de Venda | Categoria, Cliente (País) | País > Categoria | Filtro: País = EUA |
| 5 | Relação dos vendedores e o detalhamento das vendas de cada um para os respectivos clientes | Valor de Venda, Quantidade Vendida | Vendedor, Cliente | Vendedor > Cliente | Drill-down de vendedor para cliente |
| 6 | Vendedores que mais dão descontos nos seus pedidos | Valor de Desconto, % Desconto, Qtde Pedidos com Desconto | Vendedor | Vendedor > País Vendedor | Necessário calcular % desconto |
| 7 | Quantidade de clientes existentes por cada país | Count Distinct Clientes | Cliente (País) | País > Cidade > Cliente | Medida de contagem |
| 8 | Quantidade de produtos existentes por cada categoria | Count Distinct Produtos | Categoria, Produto | Categoria > Produto | Medida de contagem |
| 9 | Fornecedores, cujos produtos são os mais vendidos na categoria de Bebidas | Quantidade Vendida, Valor de Venda | Fornecedor, Categoria, Produto | Categoria > Produto > Fornecedor | Filtro: Categoria = Bebidas |
| 10 | Evolução mensal das vendas no ano de 1997 | Valor de Venda, Quantidade Vendida | Tempo | Ano > Trimestre > Mês | Filtro: Ano = 1997, análise temporal |
| 11 | Tempo médio de entrega (em dias) de cada transportadora no ano de 1997 | Tempo de Entrega (dias), Qtde Pedidos | Transportadora, Tempo | Transportadora, Ano > Mês | Filtro: Ano = 1997, necessário calcular diferença de datas |
| 12 | Distribuição da qtde. de vendedores por país de origem | Count Distinct Vendedores | Vendedor (País) | País | Medida de contagem, dimensão degenerada possível |
| 13 | Cidades que mais consomem (qtde) o produto "Côte de Blaye" | Quantidade Vendida | Cliente (Cidade), Produto | Cidade > Cliente | Filtro: Produto específico |
| 14 | Vendedores que participaram nas vendas do principal cliente | Valor de Venda, Quantidade Vendida | Vendedor, Cliente | Cliente > Vendedor | Filtro: Top 1 Cliente |
| 15 | Fornecedores vinculados às vendas do principal cliente | Valor de Venda, Quantidade Vendida | Fornecedor, Cliente, Produto | Cliente > Produto > Fornecedor | Filtro: Top 1 Cliente |
| 16 | Produtos mais vendidos do principal cliente | Quantidade Vendida, Valor de Venda | Produto, Cliente | Cliente > Produto | Filtro: Top 1 Cliente |
| 17 | Relação contendo cada Categoria, os Produtos mais vendidos e os principais clientes de cada produto | Quantidade Vendida, Valor de Venda | Categoria, Produto, Cliente | Categoria > Produto > Cliente | Análise multinível |
| 18 | Relação dos clientes do Brasil com informações de contato | - | Cliente | País > Estado > Cidade > Cliente | Filtro: País = Brasil, dados descritivos |
| 19 | Relação da quantidade de pedidos atendidos por transportadora nos anos 96, 97 e 98 | Qtde Pedidos | Transportadora, Tempo | Ano, Transportadora | Filtro: Anos 1996-1998 |
| 20 | Ticket médio por pedido (Geral, por Cliente/País/Cidade) | Valor de Venda, Qtde Pedidos, Ticket Médio | Cliente, Tempo | País > Cidade > Cliente | Medida calculada: Venda/Pedidos |
| 21 | Transportadoras com melhor tempo de Entrega | Tempo de Entrega (dias), Qtde Pedidos | Transportadora | Transportadora | Ordenação por tempo médio |
| 22 | Tempo médio para liberação dos produtos para entrega | Tempo de Processamento (dias), Qtde Pedidos | Tempo, Produto | Ano > Mês, Categoria > Produto | Diferença entre data pedido e data envio |
| 23 | Vendedores e respectivos tickets médios por pedido | Valor de Venda, Qtde Pedidos, Ticket Médio | Vendedor | Vendedor > País Vendedor | Medida calculada |
| 24 | Produtos que não estão tendo movimentação de venda | Quantidade Vendida, Data Última Venda | Produto, Tempo | Categoria > Produto | Filtro: Qtde = 0 em período |
| 25 | Categorias de produtos que mais se dão descontos | Valor de Desconto, % Desconto | Categoria | Categoria | Análise de desconto por categoria |
| 26 | Tendência no faturamento, com base no histórico de vendas | Valor de Venda, Tendência (calculada) | Tempo | Ano > Trimestre > Mês | Análise temporal com projeção |
| 27 | Existem clientes com perfil de consumo similar? | Valor de Venda, Quantidade Vendida, Categorias Consumidas | Cliente, Categoria, Produto | País > Cidade > Cliente | Análise de cluster/segmentação |
