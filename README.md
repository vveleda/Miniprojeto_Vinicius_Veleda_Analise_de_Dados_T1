# Miniprojeto - Análise Exploratória da Base Varejo

**Aluno:** Vinícius Veleda  
**Turma:** Analise_de_Dados_T1  
**Arquivo principal:** `miniprojeto_varejo_vinicius_veleda.py`

## 1. Objetivo do projeto

Este projeto tem como objetivo realizar uma Análise Exploratória de Dados (AED) usando Python, aplicando etapas básicas de importação, verificação da qualidade dos dados, limpeza, transformação de tipos, estatística descritiva e agrupamentos.

A base utilizada é a `Base_Varejo.csv`, contendo registros de compras de clientes, produtos, categorias e datas.

## 2. Como executar no VSCode

### Passo 1 - Abrir a pasta do projeto

Abra a pasta do projeto no VSCode:

`Miniprojeto_Vinicius_Veleda_Analise_de_Dados_T1`

A estrutura esperada é:

```text
Miniprojeto_Vinicius_Veleda_Analise_de_Dados_T1/
│
├── dados/
│   └── Base_Varejo.csv
│
├── saida/
│   ├── df_limpo.csv
│   └── relatorio_saida.txt
│
├── miniprojeto_varejo_vinicius_veleda.py
├── README.md
├── README_Vinicius_Veleda_Analise_de_Dados_T1.md
└── requirements.txt
```

### Passo 2 - Criar ambiente virtual

No terminal do VSCode:

```bash
python -m venv .venv
```

Ativar no Windows:

```bash
.venv\Scripts\activate
```

### Passo 3 - Instalar dependências

```bash
pip install -r requirements.txt
```

### Passo 4 - Executar o script

```bash
python miniprojeto_varejo_vinicius_veleda.py
```

Ao final, serão gerados:

- `saida/df_limpo.csv`: base tratada;
- `saida/relatorio_saida.txt`: relatório textual com resultados da análise.

## 3. Sprints do projeto

## Sprint 1 - Importação dos dados

A base foi carregada a partir do arquivo `Base_Varejo.csv`.

Foi utilizado `csv.DictReader` para realizar a leitura estruturada do CSV, linha por linha, e depois os dados foram convertidos para um DataFrame do pandas.

Essa escolha foi feita porque o `csv.DictReader` ajuda a visualizar a estrutura original do arquivo, enquanto o pandas facilita a análise, limpeza e criação de agrupamentos.

Nesta etapa foram verificados:

- número de registros;
- número de colunas;
- nomes das colunas;
- tipos de dados iniciais;
- primeiras linhas da base.

## Sprint 2 - Transformação de strings, inteiros, floats e datas

Nesta etapa foram criadas funções para padronizar os dados.

Foram realizadas as seguintes transformações:

- remoção de espaços extras nos textos;
- conversão de textos para letras maiúsculas;
- tratamento de categorias vazias ou inválidas;
- conversão da coluna `DATA` para o tipo `datetime`;
- conversão das colunas numéricas para tipo numérico.

A coluna `DATA` foi convertida com `dayfirst=True`, pois as datas estão no formato brasileiro, ou seja, dia/mês/ano.

## Sprint 3 - Limpeza de nulos e duplicatas

Foram identificados os seguintes problemas principais:

- existência de colunas vazias criadas por separadores extras no CSV;
- existência de registros duplicados;
- categorias marcadas como `#N/D`;
- necessidade de conversão da coluna de data.

As colunas `Unnamed` foram removidas porque estavam completamente vazias.

As categorias vazias, nulas ou `#N/D` foram preenchidas como `SEM CATEGORIA`, pois o registro de compra ainda pode ser útil mesmo sem categoria definida.

As duplicatas completas foram removidas para evitar contagem repetida na análise.

## Sprint 4 - Estatística descritiva

Foi analisada a coluna `CL_FHL`, que representa o número de filhos do cliente.

Foram calculados:

- média;
- mediana;
- desvio padrão;
- moda;
- máximo;
- mínimo;
- contagem;
- quartis;
- resumo com `describe()`.

## Sprint 5 - Relatório e documentação

O script gera um relatório final no terminal e também salva o arquivo `saida/relatorio_saida.txt`.

Também foram feitos agrupamentos para buscar padrões nos dados.

Como a base não possui coluna de valor monetário, a análise de vendas foi feita por quantidade de itens/registros e quantidade de compras únicas.

Agrupamentos criados:

- vendas por gênero;
- vendas por categoria;
- vendas por segmento do cliente;
- vendas por ano.

## Sprint 6 - Versionamento

Sugestão de criação do repositório público no GitHub:

Nome do repositório:

```text
Miniprojeto_Vinicius_Veleda_Analise_de_Dados_T1
```

Sugestão de commits para demonstrar progresso:

```bash
git init
git add README.md README_Vinicius_Veleda_Analise_de_Dados_T1.md requirements.txt
git commit -m "docs: cria documentacao inicial do miniprojeto"

git add dados/Base_Varejo.csv
git commit -m "data: adiciona base de varejo"

git add miniprojeto_varejo_vinicius_veleda.py
git commit -m "feat: implementa importacao e limpeza da base"

git add saida/df_limpo.csv saida/relatorio_saida.txt
git commit -m "feat: adiciona base limpa e relatorio final"
```

Depois, criar o repositório no GitHub e enviar:

```bash
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/Miniprojeto_Vinicius_Veleda_Analise_de_Dados_T1.git
git push -u origin main
```

## 4. Principais resultados encontrados

Após a limpeza, a base final ficou com **733.447 registros**.

O período analisado vai de **04/01/2019 até 08/12/2022**.

A categoria com maior quantidade de itens vendidos foi **ALIMENTOS**, com **384.197 registros**.

O gênero com maior quantidade de itens comprados foi **F**, com **382.427 registros**.

A moda do número de filhos é **0**, indicando que muitos clientes da base não possuem filhos registrados.

A base não possui coluna de valor monetário. Por isso, as análises de venda foram feitas por quantidade de itens e compras únicas, e não por faturamento.

## 5. Reflexão teórica sobre ETL e qualidade de dados

ETL significa Extração, Transformação e Carga dos dados.

Neste projeto, a extração aconteceu quando a base CSV foi carregada para o Python.

A transformação aconteceu durante a limpeza dos dados, com padronização de textos, conversão de datas, conversão de colunas numéricas, tratamento de categorias inconsistentes e remoção de duplicatas.

A carga aconteceu quando a base limpa foi salva no arquivo `df_limpo.csv` e o relatório final foi salvo em `relatorio_saida.txt`.

A qualidade dos dados é importante porque dados duplicados, tipos incorretos ou categorias vazias podem gerar análises erradas. Por exemplo, se as duplicatas não fossem removidas, algumas compras seriam contadas mais de uma vez. Se a data continuasse como texto, seria mais difícil fazer análises por ano ou período.

## 6. Observações finais

Este projeto foi desenvolvido de forma simples e objetiva, com comentários no código, para demonstrar o processo de aprendizado inicial em análise de dados com Python.

A base foi tratada para permitir análises exploratórias básicas e preparar os dados para usos futuros, como dashboards, relatórios ou análises mais avançadas.
