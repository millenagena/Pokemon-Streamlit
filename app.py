import requests
import streamlit as st

def get_pokemon_by_name(name):
    return requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')

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
    habilidade = [infos['abilities'][0]['ability']['name'], 
                  infos['abilities'][0]['ability']['url']]
    movimentos = [(move['move']['name'], move['move']['url']) for move in infos['moves']]
    evolucoes = infos['species']['url']
    return {
        'id':id,
        'nome':nome,
        'tipo1':extrai_tipos(tipos)[0],
        'tipo2':extrai_tipos(tipos)[1],
        'peso': float(peso),
        'altura': float(altura),
        'habilidade': habilidade,
        'movimentos': f'{movimentos}',
        'evolucao1': extrai_evolucao(evolucoes)[0],
        'evolucao2': extrai_evolucao(evolucoes)[1],
        'evolucao3': extrai_evolucao(evolucoes)[2],
        'imagem': imagem
    }

st.title('Pokemons')
nome_pokemon = st.text_input('Digite o nome do Pokemon:').lower()


if(nome_pokemon):
    response = get_pokemon_by_name(nome_pokemon)
    infos_pokemon = pokemon_from_api(response)
    habilidade_pokemon = requests.get(infos_pokemon['habilidade'][1]).json()
    for descricao in habilidade_pokemon['effect_entries']:
        if descricao['language']['name'] == 'en':
            descricao_habilidade = descricao['short_effect']
    st.title(f'{infos_pokemon["nome"].title()} - Nº {infos_pokemon["id"]}')
    with st.container():
        coluna1, coluna2 = st.columns(2)
        with coluna1:
            st.image(infos_pokemon['imagem'], width=128)
            st.markdown('#### Tipos')
            st.markdown(infos_pokemon['tipo1'].title())
            if infos_pokemon['tipo2']:
                st.markdown(infos_pokemon['tipo2'].title())
        with coluna2:
            st.markdown('#### Altura')
            st.markdown(infos_pokemon["altura"])
            st.markdown('#### Peso')
            st.markdown(infos_pokemon["peso"])
            st.markdown('#### Habilidade')
            with st.expander(infos_pokemon["habilidade"][0].title()):
                st.markdown(descricao_habilidade)
    with st.container():
        coluna1, coluna2, coluna3
            