import requests
import pandas as pd
from pymongo import MongoClient


def obter_relacao_abilities():
    url_abilities = 'https://pokeapi.co/api/v2/ability/?offset=00&limit=400'

    response_abilities = requests.get(url_abilities)

    if response_abilities.status_code == 200:
        abilities_data = response_abilities.json()

        # Criar um dicionário para armazenar a relação chave-valor de abilities
        relacao_abilities = []

        # Iterar sobre cada ability na lista de results
        for ability in abilities_data['results']:
            relacao_abilities.append({'id_ability': int(ability['url'].split('/')[-2]),'name': ability['name'], 'url': ability['url']})
            
        return relacao_abilities
    else:
        print(f'Erro ao obter informações das abilities. Código de status: {response_abilities.status_code}')
        return None

if __name__ == '__main__':
    relacao_abilities = obter_relacao_abilities()

    if relacao_abilities:
                
        df = pd.DataFrame(relacao_abilities)
        


        # Configurar a conexão com o MongoDB
        # Certifique-se de substituir 'seu_banco' pelo nome do seu banco de dados
        client = MongoClient('mongodb+srv://amanda:V5lHRFDWhzCN46gU@crafters.dezge1q.mongodb.net/')
        db = client['amanda']

        # Substitua 'types_2' pelo nome da sua coleção no MongoDB
        collection = db['abilities_pokemons']

        # Carregar DataFrame para o MongoDB
        records = df.to_dict(orient='records')
        collection.insert_many(records)

        print('Dados inseridos no MongoDB com sucesso.')
    else:
        print('Não foi possível obter a relação de abilities.')


