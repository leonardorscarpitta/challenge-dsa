# Controle de Consumo de Insumos em Unidades de Diagnóstico

Este projeto simula o consumo diário de insumos (reagentes e descartáveis) em unidades de diagnóstico, utilizando estruturas de dados e algoritmos para organizar, buscar e ordenar os dados de forma eficiente. A seguir, explicamos como cada estrutura e algoritmo foi utilizado no contexto do problema:

## Estruturas de Dados

### 1. Fila (`FilaConsumo`)
- **Uso:** Registra o consumo diário de insumos em ordem cronológica.
- **Contexto:** Permite visualizar o histórico de uso dos insumos, facilitando o acompanhamento do consumo ao longo do tempo.
- **Métodos:**
  - `registrar_consumo`: Adiciona um registro de consumo ao final da fila.
  - `listar_consumos`: Retorna todos os consumos na ordem em que foram registrados.

### 2. Pilha (`PilhaConsumo`)
- **Uso:** Consulta os últimos consumos realizados.
- **Contexto:** Útil para auditoria ou conferência rápida dos insumos mais recentemente utilizados.
- **Métodos:**
  - `registrar_consumo`: Adiciona um registro de consumo ao topo da pilha.
  - `listar_consumos_inverso`: Retorna os consumos em ordem inversa (do mais recente ao mais antigo).

## Algoritmos de Busca

### 1. Busca Sequencial (`busca_sequencial`)
- **Uso:** Percorre todos os registros para localizar um insumo pelo nome.
- **Contexto:** Adequado para listas pequenas, onde a eficiência não é crítica.

### 2. Busca Binária (`busca_binaria`)
- **Uso:** Localiza insumos rapidamente em listas ordenadas pelo nome.
- **Contexto:** Mais eficiente para grandes volumes de dados, pois reduz o número de comparações necessárias.

## Algoritmos de Ordenação

### 1. Merge Sort (`merge_sort`)
- **Uso:** Organiza os insumos por quantidade consumida, validade ou qualquer outro campo.
- **Contexto:** Utilizado para facilitar o controle e a reposição dos insumos, além de permitir a persistência dos dados ordenados no arquivo.

### 2. Quick Sort (`quick_sort`)
- **Uso:** Alternativa ao Merge Sort para ordenar insumos por diferentes campos.
- **Contexto:** Oferece boa performance na maioria dos casos e é utilizado para comparar diferentes métodos de ordenação.

## Geração de Dados Aleatórios
- **Uso:** Simula cenários reais de consumo de insumos, permitindo testar todas as funcionalidades do sistema.
- **Contexto:** Gera insumos com dados variados para alimentar as estruturas e algoritmos implementados.

---

Este projeto demonstra como o uso adequado de estruturas de dados e algoritmos clássicos pode melhorar o controle de estoque e a previsão de reposição de insumos em ambientes de diagnóstico, tornando o processo mais eficiente e confiável.