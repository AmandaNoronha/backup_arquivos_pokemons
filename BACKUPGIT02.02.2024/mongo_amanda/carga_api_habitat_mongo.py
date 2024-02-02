import requests
import pandas as pd
from pymongo import MongoClient


def obter_informacoes_habitats_pokemon():
    url_habitats = 'https://pokeapi.co/api/v2/pokemon-habitat/'
    
    response_habitats = requests.get(url_habitats)

    if response_habitats.status_code == 200:
        habitats_data = response_habitats.json()

        # Lista para armazenar informações dos habitats
        habitats_pokemon = []

        # Iterar sobre cada habitat na lista de results
        for habitat in habitats_data['results']:
            habitat_info = {
                'id_habitat': int(habitat['url'].split('/')[-2]),
                'name_habitat': habitat['name'],
                'url': habitat['url']
            }
            habitats_pokemon.append(habitat_info)

        return habitats_pokemon
    else:
        print(f'Erro ao obter informações dos habitats. Código de status: {response_habitats.status_code}')
        return None

if __name__ == '__main__':
    informacoes_habitats = obter_informacoes_habitats_pokemon()

    if informacoes_habitats:
        df = pd.DataFrame(informacoes_habitats)

        # Configurar a conexão com o MongoDB
        # Certifique-se de substituir 'seu_banco' pelo nome do seu banco de dados
        client = MongoClient('mongodb+srv://amanda:V5lHRFDWhzCN46gU@crafters.dezge1q.mongodb.net/')
        db = client['amanda']

        # Substitua 'types_2' pelo nome da sua coleção no MongoDB
        collection = db['habitats_pokemons']

        # Carregar DataFrame para o MongoDB
        records = df.to_dict(orient='records')
        collection.insert_many(records)

        print('Dados inseridos no MongoDB com sucesso.')
    else:
        print('Não foi possível obter a relação de habitats.')



