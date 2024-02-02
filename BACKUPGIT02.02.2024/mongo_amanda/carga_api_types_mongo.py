import requests
import pandas as pd
from pymongo import MongoClient

def obter_relacao_types():
    url_types = 'https://pokeapi.co/api/v2/type/'
    response_types = requests.get(url_types)

    if response_types.status_code == 200:
        types_data = response_types.json()
        relacao_types = []

        for types in types_data['results']:
            relacao_types.append({'id_type': int(types['url'].split('/')[-2]),'name': types['name'],'url': types['url']})

        return relacao_types
    else:
        print(f'Erro ao obter informações dos tipos. Código de status: {response_types.status_code}')
        return None

if __name__ == '__main__':
    relacao_types = obter_relacao_types()

    if relacao_types:
        df = pd.DataFrame(relacao_types)

        # Configurar a conexão com o MongoDB
        # Certifique-se de substituir 'seu_banco' pelo nome do seu banco de dados
        client = MongoClient('mongodb+srv://amanda:V5lHRFDWhzCN46gU@crafters.dezge1q.mongodb.net/')
        db = client['amanda']

        # Substitua 'types_2' pelo nome da sua coleção no MongoDB
        collection = db['types_pokemons']

        # Carregar DataFrame para o MongoDB
        records = df.to_dict(orient='records')
        collection.insert_many(records)

        print('Dados inseridos no MongoDB com sucesso.')
    else:
        print('Não foi possível obter a relação de types.')



