# Construir API --> Flask
from flask import Flask, request
import joblib
import sqlite3
from datetime import datetime
# Instanciar o aplicativo
Aplicativo = Flask(__name__)

# Carregar modelo
modelo = joblib.load('random_forest_reg_v1.pkl')


#--------------------FUNÇÃO DA API----------------------
# Função para receber a API
@Aplicativo.route('/API_Preditivo/<area>;<rooms>;<bathroom>;<parking_spaces>;<floor>;<animal>;<furniture>;<hoa>;<property_tax>', methods=['GET'])
def funcao_01(area,rooms,bathroom,parking_spaces,floor,animal,furniture,hoa,property_tax):
    # Recebendo os imputs da API
    lista= [[
        float(area),float(rooms),float(bathroom),float(parking_spaces),
        float(floor),float(animal),float(furniture),float(hoa),float(property_tax)
    ]]
    tempo_inicio = datetime.now()

    try:

        previsao = modelo.predict(lista)
        lista.append(previsao[0])
        # Concatenando a lista
        input = ''
        for i in lista:
            input = input + ';' + str(i)
        tempo_fim = datetime.now()
        tempo_processamento = tempo_fim - tempo_inicio

        #----------------CONEXÃO BANCO DE DADOS----------------
        # Criar a conexão com o banco de Dados
        conexao_banco = sqlite3.connect('Banco_dados_API.db')
        cursor = conexao_banco.cursor()

        # Query 
        query_inserindo_dados = f'''
            INSERT INTO Log_API (Inputs, Inicio, Fim, Processamento)
            VALUES ( '{input}', '{tempo_inicio}', '{tempo_fim}', '{tempo_processamento}' )
        '''
        # Executar a Query
        cursor.execute( query_inserindo_dados)
        conexao_banco.commit()
        cursor.close()

        return {'Valor aluguel': previsao[0]}

    except:
        return {'Aviso': 'Deu algum erro!'}


if __name__ == '__main__':
    Aplicativo.run(debug=True)