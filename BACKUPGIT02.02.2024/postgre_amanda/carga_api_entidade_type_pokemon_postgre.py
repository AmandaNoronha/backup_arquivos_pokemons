import requests
import json
import pandas as pd
from sqlalchemy import create_engine

def obter_informacoes_pokemon(id_pokemon):
    url_pokemon = f'https://pokeapi.co/api/v2/pokemon/{id_pokemon}/'
    
    response_pokemon = requests.get(url_pokemon)

    if response_pokemon.status_code == 200:
        pokemon_data = response_pokemon.json()

        # Extrair informações desejadas
        id_pokemon = int(pokemon_data['id'])  # Converter para número inteiro
        name_pokemon = pokemon_data['name']

        # Extrair informações do type (tipo)
        types = [{'id': int(type_info['type']['url'].split('/')[-2]), 'name': type_info['type']['name']} for type_info in pokemon_data['types']]

        # Adicionar informações ao dicionário
        pokemon_info_list = []
        for type_info in types:
            pokemon_info = {
                'id_pokemon': id_pokemon,
                'name_pokemon': name_pokemon,
                'id_type': type_info['id'],
                'name_type': type_info['name']
            }
            pokemon_info_list.append(pokemon_info)

        return pokemon_info_list
    else:
        print(f'Erro ao obter informações do Pokémon {id_pokemon}. Código de status: {response_pokemon.status_code}')
        return None

if __name__ == '__main__':
    # IDs dos Pokémon a serem consultados (de 1 a 150)
    ids_pokemon = list(range(1, 151))

    # Lista para armazenar informações dos Pokémon
    informacoes_pokemon = []

    for id_pokemon in ids_pokemon:
        pokemon_info = obter_informacoes_pokemon(id_pokemon)
        if pokemon_info:
            informacoes_pokemon.extend(pokemon_info)

    if informacoes_pokemon:
        # Salvar informações em um DataFrame
        df = pd.DataFrame(informacoes_pokemon)

        # Configurar a conexão com o PostgreSQL
        passwd = "U*gYt>?QvKD&\\2V["
        engine = create_engine(f'postgresql://amanda:{passwd}@34.66.212.40:5432/amanda')

        # Carregar DataFrame para o PostgreSQL
        df.to_sql('type_pokemons', con=engine, if_exists='replace', index=False)
        print('Dados inseridos no PostgreSQL com sucesso!')

    else:
        print('Não foi possível obter informações para a tabela "type_pokemons".')
