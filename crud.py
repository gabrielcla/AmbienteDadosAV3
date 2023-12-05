from Configs import *
import pymysql
import pandas as pd

#|###############################################################################################|#
#|					COMANDO						            :	RETORNA         | Retornar None	 |#
#|__________________________________________________________:___________________|________________|#
#| conectar(host, usuario, senha, banco_dados)	            : Objeto de Conexão | -     		 |#
#| desconectar(conexao)                         	        : - 				| -		         |#
#|__________________________________________________________:____________________________________|#
#| selecionar_registros(conexao, tabela)				    : Lista de tuplas   | Deu erro       |#
#| inserir_registro(conexao, tabela, dados)		            : Bool 			    | Deu erro		 |#
#| atualizar_registro(conexao, tabela, id_registro, dados): : Bool				| Deu erro		 |#
#| excluir_registro(conexao, tabela, id_registro)	        : Bool				| Deu erro		 |#
#| mostrar_registros(conexao, tabela)                       : -                 | -              |#
#| ultimo_id(conexao, tabela)                               :                   | Tabela vazia   |#
#| consulta_sql(conexao, consulta)                          : Lista de tuplas   | Deu erro       |#
# colunas_tabela(conexao, tabela)
# fazer_consulta(consulta_sql)
#|__________________________________________________________:____________________________________|#


#|##########################################| CONEXÃO |##########################################|#

# Inicia a conexão ao banco de dados
# Retorna o banco de dados
def conectar(host, usuario, senha, banco_dados):
    # Conectar ao banco de dados
    conexao = pymysql.connect(
        host=host,
        user=usuario,
        password=senha,
        database=banco_dados
    )
    return conexao

# Desconecta do banco de dados
def desconectar(conexao):
    # Fechar a conexão
    conexao.close()


###################################################################################################
#|___________________________________| CRUD |_____________________________________________________#
#| conexao 	    : PyMysql	| Armazena os dados da conexao
#| tabela 	    : String	| Nome da tabela que será manipulada
#| id_registro 	: Int	    | Identificador do registro
#| dados	    : Dic	    | Dicionário com as colunas e valores dos registros correspondentes
#|________________________________________________________________________________________________#

# Recebe a conexão e o nome da tabela
# Retorna lista de registros da tabela
def selecionar_registros(conexao, tabela):
    try:
        with conexao.cursor() as cursor:
            # Executar a consulta SQL para selecionar todas as linhas da tabela
            consulta_sql = f"SELECT * FROM {tabela}"
            cursor.execute(consulta_sql)

            # Recuperar todas as linhas
            linhas = cursor.fetchall()

            # Imprimir os resultados
            return linhas

    except pymysql.Error as e:
        print(f"Erro ao selecionar registros: {e}")
        return None


# Recebe a conexão, nome da tabela e dicionario com os valores e colunas do registro
# Retorna True se inseriu o registro com sucesso e None caso contrário
# 
def inserir_registro(tabela, dados):
    # Conectar ao banco de dados MySQL usando pymysql
    conexao = conectar(host, usuario, senha, banco_dados)
    
    try:
        with conexao.cursor() as cursor:
            # Montar a consulta SQL para inserção
            colunas = ', '.join(dados.keys())
            valores = ', '.join(['%s'] * len(dados))
            consulta_sql = f"INSERT INTO {tabela} ({colunas}) VALUES ({valores})"
            
            # Executar a consulta SQL
            cursor.execute(consulta_sql, tuple(dados.values()))
        
    # Se der erro
    except:
        print("Erro ao inserir registros")
        conexao.rollback()      # Se der erro, desfaz as inserções
        desconectar(conexao)
        raise
    # Se der certo
    else:
        # Commit para salvar as alterações no banco de dados
        conexao.commit()
        # Desconecta a conexão

        desconectar(conexao)
        print("Registro inserido com sucesso!")



# Recebe a conexão, tabela, id do registro e dic com novos dados (só precisa os dados que vão ser alterados)
# Retorna True se atualizou o registro com sucesso e None caso contrário
def atualizar_registro(tabela, id_registro, dados):
    # Conectar ao banco de dados MySQL usando pymysql
    conexao = conectar(host, usuario, senha, banco_dados)
    try:
        with conexao.cursor() as cursor:
            # Montar a consulta SQL para atualização
            atualizacoes = ', '.join([f"{coluna} = %s" for coluna in dados.keys()])
            consulta_sql = f"UPDATE {tabela} SET {atualizacoes} WHERE id = %s"

            # Executar a consulta SQL
            cursor.execute(consulta_sql, (*dados.values(), id_registro))
            
            # Commit para salvar as alterações no banco de dados
            conexao.commit()

            # Desconecta a conexão
            desconectar(conexao)

            print("Registro atualizado com sucesso!\n")
            return True

    except pymysql.Error as e:
        print(f"Erro ao atualizar registro: {e}")
        return None


# Recebe a conexão, tabela, id e dic com novos dados
# Return True caso a exclusão dê certo e None caso contrário
def excluir_registro(tabela, id_registro):
    # Conectar ao banco de dados MySQL usando pymysql
    conexao = conectar(host, usuario, senha, banco_dados)
    try:
        with conexao.cursor() as cursor:
            # Montar a consulta SQL para exclusão
            consulta_sql = f"DELETE FROM {tabela} WHERE id = %s"

            # Executar a consulta SQL
            cursor.execute(consulta_sql, (id_registro,))
            
            # Commit para salvar as alterações no banco de dados
            conexao.commit()

            # Desconecta a conexão
            desconectar(conexao)

            print("Registro excluído com sucesso!\n")
            return True

    except pymysql.Error as e:
        print(f"Erro ao excluir registro: {e}")
        return None


###################################################################################################
#|___________________________________________| Outras |___________________________________________#



# Retorna um df com todos os elementos da tabela
def mostrar_registros(tabela):
    # LER TODOS OS REGISTROS DE UMA TABELA
    consulta_sql = f"SELECT * FROM {tabela}"
    df = fazer_consulta(consulta_sql)
    return df

###################################################################################################
#|________________________________________________________________________________________________#

# Recebe a conexão e uma string com a consulta SQL que deseja fazer
# Retorna TUPLA de registros que correspondem a sua busca
def consulta_sql(consulta):
    # Conectar ao banco de dados MySQL usando pymysql
    conexao = conectar(host, usuario, senha, banco_dados)
    try:
        with conexao.cursor() as cursor:
            # Executar a consulta SQL para selecionar todas as linhas da tabela
            cursor.execute(consulta)

            # Recuperar todas as linhas
            linhas = cursor.fetchall()
            # Converte pra lista
            ll = []
            for l in linhas:
                ll.append(list(l))
            
            # Desconecta a conexão
            desconectar(conexao)
            return ll

    except pymysql.Error as e:
        print(f"Erro ao selecionar registros: {e}")
        return None


# Retorna o id do ultimo elemento da tabela fornecida
def ultimo_id(tabela):
    # Montar a consulta SQL para exclusão
    consulta = f"SELECT id FROM {tabela} ORDER BY id DESC LIMIT 1;"
    resp = consulta_sql(consulta)
    
    # Se a tabela estiver vazia, retorna None
    if len(resp)==0:
        return None
    
    # Se não tiver vazia, retorna o ultimo id
    return resp[0][0]



# Recebe uma string com a consulta sql que vai ser realizada
# Retorna um DataFrame com os resultados da consulta sql
def fazer_consulta(consulta_sql):
    # Conectar ao banco de dados MySQL usando pymysql
    conexao = conectar(host, usuario, senha, banco_dados)

    # Criar um cursor para executar a consulta
    cursor = conexao.cursor()

    # Executar a consulta SQL
    cursor.execute(consulta_sql)

    # Obter os resultados da consulta
    dados = cursor.fetchall()

    # Obter os nomes das colunas
    colunas = [i[0] for i in cursor.description]

    # Criar um DataFrame Pandas
    df = pd.DataFrame(dados, columns=colunas)

    # Fechar o cursor e a conexão com o banco de dados
    cursor.close()
    conexao.close()
    
    return df

# Recebe a tabela
# Return True caso a exclusão dê certo e None caso contrário
def excluir_todos_registros(tabela):
    # Conectar ao banco de dados MySQL usando pymysql
    conexao = conectar(host, usuario, senha, banco_dados)
    try:
        with conexao.cursor() as cursor:
            # Montar a consulta SQL para exclusão
            consulta_sql = f"DELETE FROM {tabela}"
            # Executar a consulta SQL
            cursor.execute(consulta_sql)
            # Commit para salvar as alterações no banco de dados
            conexao.commit()
        # Desconecta a conexão
        desconectar(conexao)
        print("Todos os registros da tabela foram excluídos com sucesso!")
#         return True
    # Se der errto
    except pymysql.Error as e:
        print(f"Erro ao excluir registros: {e}")
        return None