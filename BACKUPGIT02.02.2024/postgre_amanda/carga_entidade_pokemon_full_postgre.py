
import requests
import json
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import JSONB


def obter_informacoes_pokemon(id_pokemon):
    url_pokemon = f'https://pokeapi.co/api/v2/pokemon/{id_pokemon}/'
    
    response_pokemon = requests.get(url_pokemon)

    if response_pokemon.status_code == 200:
        pokemon_data = response_pokemon.json()

        # Extrair informações desejadas
        id_pokemon = int(pokemon_data['id'])  # Converter para número inteiro
        name_pokemon = pokemon_data['name']
        weight = pokemon_data['weight']
        height = pokemon_data['height']


        # Extrair informações das sprites (imagens)
        #image = {'back_default': pokemon_data['sprites']['back_default']}
        image = pokemon_data['sprites']['back_default']
        

        # Consultar informações da espécie
        url_species = f'https://pokeapi.co/api/v2/pokemon-species/{id_pokemon}/'
        response_species = requests.get(url_species)
        if response_species.status_code == 200:
            species_data = response_species.json()
            
            # Extrair informações da evolução anterior
            evolves_from_species = species_data.get('evolves_from_species', None)
            if evolves_from_species:
                id_evolution = int(evolves_from_species['url'].split('/')[-2])
                name_evolution = evolves_from_species['name']
            else:
                id_evolution = None
                name_evolution = None

            # Extrair descrição (flavor_text) na versao red 
            flavor_text = None
            for flavor_entry in species_data.get('flavor_text_entries', []):
                if flavor_entry['language']['name'] == 'en' and flavor_entry['version']['name'] == 'red':
                    flavor_text = flavor_entry['flavor_text']
                    break
                
            # Extrair informações do habitat
            habitat_data = species_data.get('habitat', None)
            if habitat_data:
                id_habitat = int(habitat_data['url'].split('/')[-2])
                name_habitat = habitat_data['name']
            else:
                id_habitat = None
                name_habitat = None

            # Adicionar informações ao dicionário
            pokemon_info = {
                'id_pokemon': id_pokemon,
                'name_pokemon': name_pokemon,
                'description_red_version': flavor_text,
                'id_habitat':id_habitat,
                'weight': weight,
                'height': height,
                'image': image,
                'evolves_from_id': id_evolution,
                'evolves_from_name': name_evolution
                }
            
            

            return pokemon_info
        else:
            print(f'Erro ao obter informações da espécie do Pokémon {id_pokemon}. Código de status: {response_species.status_code}')
            return None
    else:
        print(f'Erro ao obter informações do Pokémon {id_pokemon}. Código de status: {response_pokemon.status_code}')
        return None

def salvar_json(data, nome_arquivo='entidade_pokemons_1a150.json'):
    with open(nome_arquivo, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # IDs dos Pokémon a serem consultados (de 1 a 150)
    ids_pokemon = list(range(1, 151))

    # Lista para armazenar informações dos Pokémon
    informacoes_pokemon = []

    for id_pokemon in ids_pokemon:
        pokemon_info = obter_informacoes_pokemon(id_pokemon)
        if pokemon_info:
            informacoes_pokemon.append(pokemon_info)

    if informacoes_pokemon:
        # Salvar informações em um DataFrame
        df = pd.DataFrame(informacoes_pokemon)


        # Configurar a conexão com o PostgreSQL
        passwd = "U*gYt>?QvKD&\\2V["
        engine = create_engine(f'postgresql://amanda:{passwd}@34.66.212.40:5432/amanda')

        # Carregar DataFrame para o PostgreSQL
        df.to_sql('entity_pokemon_full', con=engine, if_exists='replace', index=False, dtype={
            'evolves_from_species': JSONB,
            'image': JSONB
            })
        print('Dados inseridos no PostgreSQL com sucesso!')

    else:
        print('Não foi possível obter a entidade pokemon.')