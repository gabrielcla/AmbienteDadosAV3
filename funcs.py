from crud import *
import csv

# Recebe o caminho do arquivo csv e retorna uma lista de dicionários com cada linha do arquivo
def importar_csv(file_path):
    data = []  # Lista para armazenar os dados

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            data.append(row)
    return data


# Recebe DataFrame e o nome do arquivo que será exportado com o DataFrame
def gravar_csv(df, nome):
    df.to_csv(nome, index=False)
    print('Arquivo gravado com sucesso!')


# Recebe o nome_tabela e arquivo csv e adiciona na tabela fornecida todas as entradas do arquivo csv
# Já usando transaction
# Recebe o nome_tabela e arquivo csv e adiciona na tabela fornecida todas as entradas do arquivo csv
def cadastrar_em_massa_dados_csv(nome_tabela, arquivo_csv):
    conexao = conectar(host, usuario, senha, banco_dados)   # Conectar ao banco de dados
    
    # Lê o arquivo csv
    dic_csv = importar_csv(arquivo_csv)
    
    # Só continua se tiver colunas
    if len(dic_csv)==0:
        print('Arquivo vazio')
        return None
    
    # Monta o comando sql pra fazer a inserção
    colunas = ', '.join(dic_csv[0].keys())   
    valores = ', '.join(['%s'] * len(dic_csv[0].keys()) )
    consulta_sql = f"INSERT INTO {nome_tabela} ({colunas}) VALUES ({valores})"

    try:
        # Iniciar a transação
        with conexao.cursor() as cursor:
            # Executa a consulta que insere cada registro
            for i in range(len(dic_csv)):
                vals = tuple(dic_csv[i].values())
                cursor.execute(consulta_sql, vals)

            # No final, faz o commit para aplicar as inserções no banco de dados
            conexao.commit()
    # Se der erro
    except:
        print("Erro ao inserir registros")
        conexao.rollback()      # Se der erro, desfaz as inserções
        desconectar(conexao)    # Desconectar
        raise
    # Se der certo
    else:
        conexao.commit()
        desconectar(conexao)
        print("Registros inseridos com sucesso!")