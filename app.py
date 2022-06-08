import requests
import streamlit

def extrai_tipos(tipos):
    tipo1 = tipos[0]['type']['name']
    try:
        tipo2 = tipos[1]['type']['name']
    except IndexError:
        tipo2 = None
    return [tipo1, tipo2]

def extrai_evolucao(evolucoes):
    url_evolution = requests.get(evolucoes).json()['evolution_chain']['url']
    primeiro_pokemon = requests.get(url_evolution).json()['chain']['species']['name']
    try:
        segundo_pokemon = requests.get(url_evolution).json()['chain']['evolves_to'][0]['species']['name']
    except:
        segundo_pokemon = None
    try:
        terceiro_pokemon = requests.get(url_evolution).json()['chain']['evolves_to'][0]['evolves_to'][0]['species']['name']
    except:
        terceiro_pokemon = None
    return [primeiro_pokemon, segundo_pokemon, terceiro_pokemon]

def pokemon_from_api(response):
    infos = response.json()
    id = infos['id']
    altura = infos['height'] 
    peso = infos['weight']
    tipos = infos['types']
    nome = infos['name']
    imagem = infos['sprites']['front_default']
    habilidade = (infos['abilities'][0]['ability']['name'], 
                  infos['abilities'][0]['ability']['url'])
    movimentos = [(move['move']['name'], move['move']['url']) for move in infos['moves']]
    evolucoes = infos['species']['url']
    return {
        'id':id,
        'nome':nome,
        'tipo1':extrai_tipos(tipos)[0],
        'tipo2':extrai_tipos(tipos)[1],
        'peso': peso,
        'altura': altura,
        'habilidade': f'{habilidade}',
        'movimentos': f'{movimentos}',
        'evolucao1': extrai_evolucao(evolucoes)[0],
        'evolucao2': extrai_evolucao(evolucoes)[1],
        'evolucao3': extrai_evolucao(evolucoes)[2],
        'imagem': imagem
    }