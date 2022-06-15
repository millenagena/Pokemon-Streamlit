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

def extrai_imagem(response):
    imagem = response.json()['sprites']['front_default']
    return imagem

def extrai_evolucao(evolucoes):
    url_evolution = requests.get(evolucoes).json()['evolution_chain']['url']
    infos_evolucoes_pokemon = requests.get(url_evolution).json()
    primeiro_pokemon = infos_evolucoes_pokemon['chain']['species']['name']
    imagem_primeiro_pokemon = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{infos_evolucoes_pokemon["chain"]["species"]["url"].split("/")[-2]}.png'
    try:
        segundo_pokemon = infos_evolucoes_pokemon['chain']['evolves_to'][0]['species']['name']
        imagem_segundo_pokemon = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{infos_evolucoes_pokemon["chain"]["evolves_to"][0]["species"]["url"].split("/")[-2]}.png'
    except:
        segundo_pokemon = None
        imagem_segundo_pokemon = None
    try:
        terceiro_pokemon = infos_evolucoes_pokemon['chain']['evolves_to'][0]['evolves_to'][0]['species']['name']
        imagem_terceiro_pokemon = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{infos_evolucoes_pokemon["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["url"].split("/")[-2]}.png'
    except:
        terceiro_pokemon = None
        imagem_terceiro_pokemon= None
    return [primeiro_pokemon, segundo_pokemon, terceiro_pokemon, imagem_primeiro_pokemon, imagem_segundo_pokemon, imagem_terceiro_pokemon]

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
        'img_evolucao1': extrai_evolucao(evolucoes)[3],
        'img_evolucao2': extrai_evolucao(evolucoes)[4],
        'img_evolucao3': extrai_evolucao(evolucoes)[5],
        'imagem': imagem
    }

with st.container():
    _,center,_ = st.columns(3)
    with center:
        st.image('https://logosmarcas.net/wp-content/uploads/2020/05/Pokemon-Logo.png', width = 256)


        
nome_pokemon = st.text_input('Digite o nome ou ID do Pokemon:').lower()

try:
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
            st.markdown('### Evoluções')
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(infos_pokemon['img_evolucao1'], width=128, caption = infos_pokemon['evolucao1'].title())
            if infos_pokemon['evolucao2']:
                with col2:
                    st.image(infos_pokemon['img_evolucao2'], width=128, caption = infos_pokemon['evolucao2'].title())
            if infos_pokemon['evolucao3']:
                with col3:
                    st.image(infos_pokemon['img_evolucao3'], width=128, caption = infos_pokemon['evolucao3'].title())
                    
except:
    st.write("Pokémon Inválido")
            