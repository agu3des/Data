Excelente. Para cobrir todo o espectro de SQL e PL/SQL (que geralmente se aplica a ambientes Oracle), vou elaborar um conjunto de desafios de dificuldade progressiva, focando desde o básico (DQL, DML) até o avançado (Joins Complexos, Cursors, Triggers, Packages).

Vamos utilizar o cenário de uma **Empresa de Consultoria**.

## Cenário: Empresa de Consultoria Global

Tabelas base:

1.  **GESTAO**
    * `GESTOR_ID` (PK, `NUMBER`)
    * `NOME_GESTOR` (`VARCHAR2(100)`)
    * `AREA_ATUACAO` (`VARCHAR2(50)`)
    * `DEP_ID` (FK para `DEPARTAMENTO`)

2.  **DEPARTAMENTO**
    * `DEP_ID` (PK, `NUMBER`)
    * `NOME_DEPARTAMENTO` (`VARCHAR2(50)`)
    * `LOCALIZACAO` (`VARCHAR2(50)`)

3.  **PROJETO**
    * `PROJ_ID` (PK, `NUMBER`)
    * `TITULO` (`VARCHAR2(100)`)
    * `ORCAMENTO` (`NUMBER(12, 2)`)
    * `STATUS` (`VARCHAR2(20)`) - (Ex: 'ATIVO', 'CONCLUIDO', 'PENDENTE')

4.  **ALOCACAO**
    * `ALOCACAO_ID` (PK, `NUMBER`)
    * `GESTOR_ID` (FK para `GESTAO`)
    * `PROJ_ID` (FK para `PROJETO`)
    * `HORAS_ALOCADAS` (`NUMBER(5)`)
    * `DATA_INICIO` (`DATE`)
    * `DATA_FIM` (`DATE`, pode ser nulo)

---

## Parte 1: Desafios de SQL (DQL, DML, DDL)

### Nível Básico (DQL/DML)

1.  **DQL Simples e Filtragem:** Liste o nome e a localização de todos os departamentos localizados em 'Nova York' ou 'Londres'.
2.  **DQL com Ordenação:** Exiba o título e o orçamento de todos os projetos que estão com o `STATUS` 'PENDENTE', ordenados pelo `ORCAMENTO` de forma decrescente.
3.  **DML (UPDATE):** Atualize o `ORCAMENTO` de todos os projetos com `STATUS` 'ATIVO' em 5%.
4.  **DML (DELETE):** Remova da tabela `GESTAO` todos os gestores cuja `AREA_ATUACAO` seja 'Suporte' e que não estejam vinculados a nenhum departamento (onde `DEP_ID` é nulo).

### Nível Intermediário (Joins e Agregação)

5.  **JOIN Múltiplo:** Liste o nome do gestor, a área de atuação do gestor e o nome do departamento correspondente. Inclua gestores que ainda não têm um departamento (use `LEFT JOIN`).
6.  **Agregação e Group By:** Calcule a soma total de `HORAS_ALOCADAS` por projeto. Exiba o título do projeto e a soma das horas. Filtre o resultado para mostrar apenas projetos que possuem mais de 500 horas alocadas no total.
7.  **Subconsulta Escalar:** Encontre o nome do departamento que possui o maior número de gestores.
8.  **Função de Janela (Window Function - Desafio Avançado em DQL):** Para cada projeto, liste o nome do gestor e sua respectiva `HORAS_ALOCADAS`. Adicione uma coluna extra mostrando a média de horas alocadas para **todos** os projetos, para comparação, sem usar `GROUP BY`. (Use `AVG() OVER()`).

---

## Parte 2: Desafios de PL/SQL (Blocos e Programação)

### Nível Básico (Blocos Anônimos e Exceções)

9.  **Bloco Anônimo e Variáveis:** Crie um bloco anônimo que declare uma variável de número (`v_proj_id = 101`) e uma variável `v_titulo` (usando `%TYPE`). Busque o `TITULO` e o `ORCAMENTO` do projeto com o ID fornecido, armazene-os e exiba uma mensagem: "O projeto [TITULO] tem um orçamento de R$ [ORCAMENTO]".
10. **Exceção (NO_DATA_FOUND):** Modifique o bloco anterior para incluir um tratamento de exceção. Se o `v_proj_id` não existir, o bloco deve capturar o erro `NO_DATA_FOUND` e exibir a mensagem: "Projeto ID 101 não encontrado na base de dados."

### Nível Intermediário (Stored Procedures e Functions)

11. **Stored Procedure com Transação:** Crie uma Stored Procedure chamada `CONCLUIR_PROJETO` que receba um `p_proj_id` como parâmetro.
    * A procedure deve:
        * Atualizar o `STATUS` do projeto para 'CONCLUIDO'.
        * Atualizar o campo `DATA_FIM` na tabela `ALOCACAO` para a data atual, apenas para as alocações que ainda estão ativas (onde `DATA_FIM` é nulo) e pertencem a este projeto.
        * Fazer um `COMMIT` e exibir o número de alocações encerradas (`SQL%ROWCOUNT`).
12. **Function com Cálculo:** Crie uma Function chamada `CALCULAR_SALDO_ORCAMENTO` que receba um `p_proj_id`.
    * A função deve retornar um `NUMBER`.
    * A lógica é: `SALDO = ORCAMENTO - (CUSTO_FIXO_PROJETO)`, onde o `CUSTO_FIXO_PROJETO` é calculado como: `(HORAS_ALOCADAS * 50)`.
    * A função deve buscar o `ORCAMENTO` e a soma total de `HORAS_ALOCADAS` para o projeto, calcular o saldo e retorná-lo.

### Nível Avançado (Cursors, Triggers e Packages)

13. **Cursor Explícito e LOOP:** Crie um bloco anônimo que utilize um **Cursor Explícito** para listar o nome de todos os gestores e o nome dos projetos em que eles estão alocados.
    * Use um `FOR...LOOP` com o cursor.
    * Para cada gestor, liste o nome do gestor e, em seguida, em linhas subsequentes, todos os títulos dos projetos associados a ele.

14. **Trigger de Auditoria:** Crie um **Trigger** `BEFORE UPDATE` na tabela `DEPARTAMENTO`.
    * Se alguém tentar alterar a `LOCALIZACAO` de um departamento, o trigger deve:
        * Verificar se a nova `LOCALIZACAO` é diferente da antiga.
        * Se for, impedir a operação (emitir uma exceção) e exibir a mensagem: "A alteração de Localização não é permitida por motivos regulatórios."

15. **Package (Organização de Código):** Crie um **Package** chamado `PKG_GESTAO_RH`.
    * Dentro do `Package Specification` (corpo do package):
        * Declare a Function `CALCULAR_SALDO_ORCAMENTO` (do Desafio 12).
        * Declare a Procedure `CONCLUIR_PROJETO` (do Desafio 11).
    * O objetivo é apenas mover a estrutura de código para o package para demonstrar organização e escopo de acesso.

**Boa sorte com os desafios! Eles abrangem a maioria dos tópicos importantes em SQL e PL/SQL.**