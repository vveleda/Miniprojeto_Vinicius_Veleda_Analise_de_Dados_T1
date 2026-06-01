"""
Mini-Projeto Avaliativo - Análise de Dados com Python [T1]
Aluno: Vinícius Veleda
Turma: Analise_de_Dados_T1

Objetivo:
Realizar uma Análise Exploratória de Dados (AED) na base de varejo,
identificando problemas, limpando os dados, gerando estatísticas descritivas
e agrupamentos básicos.

Como executar no VSCode:
1. Coloque este arquivo .py na pasta do projeto.
2. Coloque a base Base_Varejo.csv dentro da pasta dados/.
3. No terminal, instale as dependências:
   pip install pandas
4. Execute:
   python miniprojeto_varejo_vinicius_veleda.py
"""

import csv
from pathlib import Path
import pandas as pd


# ---------------------------------------------------------------------
# CONFIGURAÇÕES INICIAIS
# ---------------------------------------------------------------------

CAMINHO_BASE = Path("dados") / "Base_Varejo.csv"
CAMINHO_SAIDA = Path("saida")
CAMINHO_DF_LIMPO = CAMINHO_SAIDA / "df_limpo.csv"
CAMINHO_RELATORIO = CAMINHO_SAIDA / "relatorio_saida.txt"


# ---------------------------------------------------------------------
# SPRINT 1 - IMPORTAÇÃO DOS DADOS
# ---------------------------------------------------------------------

def carregar_csv_com_dictreader(caminho_arquivo: Path) -> pd.DataFrame:
    """
    Carrega um arquivo CSV usando csv.DictReader e transforma em DataFrame.

    Por que usar csv.DictReader?
    - O csv.DictReader lê cada linha como um dicionário.
    - Isso ajuda a entender a estrutura original do arquivo.
    - Depois transformamos a lista de dicionários em DataFrame para trabalhar
      com pandas, que facilita limpeza, filtros, estatísticas e agrupamentos.
    """
    if not caminho_arquivo.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho_arquivo}. "
            "Verifique se a base está na pasta dados/."
        )

    linhas = []

    with open(caminho_arquivo, mode="r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")

        for linha in leitor:
            linhas.append(linha)

    df = pd.DataFrame(linhas)
    return df


def mostrar_estrutura_inicial(df: pd.DataFrame) -> str:
    """
    Gera um texto com a visão inicial da base:
    quantidade de registros, colunas e tipos de dados.
    """
    texto = []
    texto.append("=== SPRINT 1 - ESTRUTURA INICIAL DA BASE ===")
    texto.append(f"Número de registros: {df.shape[0]}")
    texto.append(f"Número de colunas: {df.shape[1]}")
    texto.append("\nColunas encontradas:")
    texto.append(str(list(df.columns)))
    texto.append("\nTipos de dados iniciais:")
    texto.append(str(df.dtypes))
    texto.append("\nPrimeiras 5 linhas:")
    texto.append(str(df.head()))
    return "\n".join(texto)


# ---------------------------------------------------------------------
# SPRINT 2 - TRANSFORMAÇÃO DE STRINGS, INTEIROS, FLOATS E DATAS
# ---------------------------------------------------------------------

def limpar_texto(valor):
    """
    Padroniza textos:
    - remove espaços extras;
    - transforma em maiúsculas;
    - mantém valores vazios como string vazia para tratamento posterior.
    """
    if pd.isna(valor):
        return ""

    return str(valor).strip().upper()


def limpar_categoria(valor):
    """
    Trata categoria de produto usando condicional if/else.

    Regra usada:
    - Se a categoria estiver vazia, nula ou marcada como #N/D,
      preencher com 'SEM CATEGORIA'.
    - Caso contrário, manter a categoria já padronizada.
    """
    valor_limpo = limpar_texto(valor)

    if valor_limpo == "" or valor_limpo == "NAN" or valor_limpo == "#N/D":
        return "SEM CATEGORIA"
    else:
        return valor_limpo


def limpar_nome_produto(valor):
    """
    Trata nome do produto usando condicional if/else.

    Caso não exista nome, será preenchido como 'SEM NOME'.
    """
    valor_limpo = limpar_texto(valor)

    if valor_limpo == "" or valor_limpo == "NAN":
        return "SEM NOME"
    else:
        return valor_limpo


def transformar_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajusta os tipos das colunas principais.

    Por que converter tipos?
    - Datas como texto impedem análises por ano, mês e período.
    - Números como texto impedem cálculos estatísticos.
    - Textos sem padronização dificultam agrupamentos corretos.
    """
    df = df.copy()

    # Remove colunas totalmente vazias criadas por separadores extras no CSV.
    colunas_vazias = [col for col in df.columns if col.startswith("Unnamed")]
    df = df.drop(columns=colunas_vazias)

    # Padronização de textos.
    colunas_texto = ["CL_GENERO", "CL_SEG", "PR_CAT", "PR_NOME"]
    for coluna in colunas_texto:
        if coluna in df.columns:
            df[coluna] = df[coluna].apply(limpar_texto)

    # Tratamento específico de categoria e produto.
    df["PR_CAT"] = df["PR_CAT"].apply(limpar_categoria)
    df["PR_NOME"] = df["PR_NOME"].apply(limpar_nome_produto)

    # Conversão de datas.
    # dayfirst=True porque a base está no padrão brasileiro: dia/mês/ano.
    df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True, errors="coerce")

    # Conversão de colunas numéricas.
    colunas_numericas = ["CO_ID", "CL_ID", "CL_EC", "CL_FHL", "PR_ID"]
    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    return df


# ---------------------------------------------------------------------
# SPRINT 3 - LIMPEZA DE NULOS E DUPLICATAS
# ---------------------------------------------------------------------

def relatorio_problemas(df_original: pd.DataFrame, df_transformado: pd.DataFrame) -> str:
    """
    Identifica problemas básicos:
    - valores nulos;
    - duplicatas;
    - datas inválidas;
    - categorias vazias/inconsistentes.
    """
    texto = []
    texto.append("\n=== SPRINT 3 - PROBLEMAS ENCONTRADOS ===")

    texto.append("\nValores nulos por coluna na base original:")
    texto.append(str(df_original.isna().sum()))

    texto.append("\nValores nulos por coluna após transformação:")
    texto.append(str(df_transformado.isna().sum()))

    duplicatas = df_transformado.duplicated().sum()
    texto.append(f"\nQuantidade de linhas duplicadas após remover colunas vazias: {duplicatas}")

    datas_invalidas = df_transformado["DATA"].isna().sum()
    texto.append(f"Quantidade de datas inválidas após conversão: {datas_invalidas}")

    categorias_sem_categoria = (df_transformado["PR_CAT"] == "SEM CATEGORIA").sum()
    texto.append(f"Quantidade de categorias preenchidas como SEM CATEGORIA: {categorias_sem_categoria}")

    return "\n".join(texto)


def limpar_nulos_e_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica a limpeza mínima necessária.

    Escolhas realizadas:
    - DATA, CO_ID, CL_ID e PR_ID são campos essenciais. Se algum deles estiver
      nulo, a linha perde sentido para a análise e será removida.
    - PR_CAT vazia foi preenchida como SEM CATEGORIA para não perder o registro.
    - Duplicatas completas foram removidas para evitar contagem repetida.
    """
    df = df.copy()

    # Remove linhas sem campos essenciais.
    colunas_essenciais = ["DATA", "CO_ID", "CL_ID", "PR_ID"]
    df = df.dropna(subset=colunas_essenciais)

    # Garante que número de filhos nulo seja tratado.
    # Nesta base não havia nulos em CL_FHL, mas a regra fica pronta.
    if df["CL_FHL"].isna().sum() > 0:
        mediana_filhos = df["CL_FHL"].median()
        df["CL_FHL"] = df["CL_FHL"].fillna(mediana_filhos)

    # Remove duplicatas completas.
    df = df.drop_duplicates()

    return df


def validar_regra_compra(df: pd.DataFrame) -> str:
    """
    Valida a regra do identificador de compra.

    Interpretação:
    - CO_ID representa o identificador da compra.
    - Uma mesma compra pode aparecer em várias linhas, pois cada linha representa
      um produto comprado.
    - Por isso, CO_ID repetido não é necessariamente erro. Ele indica uma compra
      com mais de um produto.
    """
    qtd_linhas = len(df)
    qtd_compras_unicas = df["CO_ID"].nunique()
    media_itens_por_compra = qtd_linhas / qtd_compras_unicas

    compras_com_mais_de_um_item = (
        df.groupby("CO_ID")["PR_ID"]
        .count()
        .reset_index(name="qtd_itens")
        .query("qtd_itens > 1")
        .shape[0]
    )

    texto = []
    texto.append("\n=== VALIDAÇÃO DA REGRA DE NEGÓCIO - IDENTIFICADOR DE COMPRA ===")
    texto.append(f"Quantidade de linhas/itens analisados: {qtd_linhas}")
    texto.append(f"Quantidade de compras únicas (CO_ID): {qtd_compras_unicas}")
    texto.append(f"Média de itens por compra: {media_itens_por_compra:.2f}")
    texto.append(f"Compras com mais de um item: {compras_com_mais_de_um_item}")
    texto.append(
        "Conclusão: CO_ID repetido é esperado, pois uma compra pode conter vários produtos."
    )
    return "\n".join(texto)


# ---------------------------------------------------------------------
# SPRINT 4 - ESTATÍSTICA DESCRITIVA
# ---------------------------------------------------------------------

def estatisticas_numero_filhos(df: pd.DataFrame) -> str:
    """
    Gera estatísticas descritivas da coluna CL_FHL,
    que representa o número de filhos do cliente.
    """
    coluna = df["CL_FHL"]

    texto = []
    texto.append("\n=== SPRINT 4 - ESTATÍSTICA DESCRITIVA: NÚMERO DE FILHOS ===")
    texto.append(f"Contagem: {coluna.count()}")
    texto.append(f"Média: {coluna.mean():.2f}")
    texto.append(f"Mediana: {coluna.median():.2f}")
    texto.append(f"Desvio padrão: {coluna.std():.2f}")
    texto.append(f"Moda: {list(coluna.mode())}")
    texto.append(f"Mínimo: {coluna.min()}")
    texto.append(f"Máximo: {coluna.max()}")
    texto.append("\nQuartis:")
    texto.append(str(coluna.quantile([0.25, 0.50, 0.75])))
    texto.append("\nResumo com describe():")
    texto.append(str(coluna.describe()))

    return "\n".join(texto)


# ---------------------------------------------------------------------
# SPRINT 5 - AGRUPAMENTOS, RELATÓRIO E CONCLUSÕES
# ---------------------------------------------------------------------

def gerar_agrupamentos(df: pd.DataFrame):
    """
    Cria agrupamentos para encontrar padrões na base.

    Como a base não possui coluna de valor monetário, a análise de vendas
    será feita por:
    - quantidade de itens/registros;
    - quantidade de compras únicas;
    - quantidade de clientes únicos.
    """
    vendas_por_genero = (
        df.groupby("CL_GENERO")
        .agg(
            qtd_itens=("PR_ID", "count"),
            compras_unicas=("CO_ID", "nunique"),
            clientes_unicos=("CL_ID", "nunique"),
        )
        .sort_values("qtd_itens", ascending=False)
    )

    vendas_por_categoria = (
        df.groupby("PR_CAT")
        .agg(
            qtd_itens=("PR_ID", "count"),
            compras_unicas=("CO_ID", "nunique"),
            clientes_unicos=("CL_ID", "nunique"),
        )
        .sort_values("qtd_itens", ascending=False)
    )

    vendas_por_segmento = (
        df.groupby("CL_SEG")
        .agg(
            qtd_itens=("PR_ID", "count"),
            compras_unicas=("CO_ID", "nunique"),
            clientes_unicos=("CL_ID", "nunique"),
        )
        .sort_values("qtd_itens", ascending=False)
    )

    vendas_por_ano = (
        df.assign(ANO=df["DATA"].dt.year)
        .groupby("ANO")
        .agg(
            qtd_itens=("PR_ID", "count"),
            compras_unicas=("CO_ID", "nunique"),
        )
    )

    return vendas_por_genero, vendas_por_categoria, vendas_por_segmento, vendas_por_ano


def montar_conclusoes(df: pd.DataFrame, vendas_por_categoria: pd.DataFrame, vendas_por_genero: pd.DataFrame) -> str:
    """
    Monta um bloco simples de conclusões com 3 a 6 tópicos.
    """
    categoria_top = vendas_por_categoria.index[0]
    qtd_categoria_top = vendas_por_categoria.iloc[0]["qtd_itens"]

    genero_top = vendas_por_genero.index[0]
    qtd_genero_top = vendas_por_genero.iloc[0]["qtd_itens"]

    data_min = df["DATA"].min().strftime("%d/%m/%Y")
    data_max = df["DATA"].max().strftime("%d/%m/%Y")

    texto = []
    texto.append("\n=== CONCLUSÕES PRINCIPAIS ===")
    texto.append(f"1. A base final ficou com {len(df)} registros limpos, após remoção de duplicatas e ajustes de tipos.")
    texto.append(f"2. O período analisado vai de {data_min} até {data_max}.")
    texto.append(f"3. A categoria com maior quantidade de itens vendidos foi {categoria_top}, com {qtd_categoria_top} registros.")
    texto.append(f"4. O gênero com maior quantidade de itens comprados foi {genero_top}, com {qtd_genero_top} registros.")
    texto.append("5. A moda do número de filhos é 0, indicando que muitos clientes da base não possuem filhos registrados.")
    texto.append("6. A base não possui coluna de valor monetário; por isso, as análises de venda foram feitas por quantidade de itens e compras únicas.")

    return "\n".join(texto)


def gerar_relatorio_final(df_original: pd.DataFrame, df_transformado: pd.DataFrame, df_limpo: pd.DataFrame) -> str:
    """
    Junta todas as partes do relatório final.
    """
    vendas_por_genero, vendas_por_categoria, vendas_por_segmento, vendas_por_ano = gerar_agrupamentos(df_limpo)

    partes = []
    partes.append(mostrar_estrutura_inicial(df_original))
    partes.append(relatorio_problemas(df_original, df_transformado))
    partes.append(validar_regra_compra(df_limpo))
    partes.append(estatisticas_numero_filhos(df_limpo))

    partes.append("\n=== AGRUPAMENTO 1 - VENDAS POR GÊNERO ===")
    partes.append(str(vendas_por_genero))

    partes.append("\n=== AGRUPAMENTO 2 - VENDAS POR CATEGORIA ===")
    partes.append(str(vendas_por_categoria))

    partes.append("\n=== AGRUPAMENTO 3 - VENDAS POR SEGMENTO DO CLIENTE ===")
    partes.append(str(vendas_por_segmento))

    partes.append("\n=== AGRUPAMENTO 4 - VENDAS POR ANO ===")
    partes.append(str(vendas_por_ano))

    partes.append(montar_conclusoes(df_limpo, vendas_por_categoria, vendas_por_genero))

    return "\n\n".join(partes)


# ---------------------------------------------------------------------
# FUNÇÃO PRINCIPAL
# ---------------------------------------------------------------------

def main():
    """
    Executa o fluxo completo do mini-projeto.
    """
    CAMINHO_SAIDA.mkdir(exist_ok=True)

    print("Iniciando Mini-Projeto de Análise de Dados...")
    print("Carregando base de dados...")

    df_original = carregar_csv_com_dictreader(CAMINHO_BASE)

    print("Transformando tipos e padronizando dados...")
    df_transformado = transformar_tipos(df_original)

    print("Limpando nulos e duplicatas...")
    df_limpo = limpar_nulos_e_duplicatas(df_transformado)

    print("Gerando relatório final...")
    relatorio = gerar_relatorio_final(df_original, df_transformado, df_limpo)

    # Salva a base limpa e o relatório.
    df_limpo.to_csv(CAMINHO_DF_LIMPO, index=False, encoding="utf-8-sig")
    with open(CAMINHO_RELATORIO, mode="w", encoding="utf-8") as arquivo:
        arquivo.write(relatorio)

    print(relatorio)
    print("\nArquivos gerados:")
    print(f"- {CAMINHO_DF_LIMPO}")
    print(f"- {CAMINHO_RELATORIO}")
    print("\nProjeto finalizado com sucesso!")


if __name__ == "__main__":
    main()
