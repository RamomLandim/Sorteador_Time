import random

# Lista de jogadores
jogadores = [
    {"nome": "Samuel", "nivel": 10, "posicao": "Goleiro", "status": "fora"},
    {"nome": "Felipe", "nivel": 7, "posicao": "Goleiro", "status": "fora"},
    {"nome": "Anderson", "nivel": 10, "posicao": "Goleiro", "status": "fora"},
    {"nome": "Renato", "nivel": 5, "posicao": "Goleiro", "status": "fora"},
    {"nome": "Thailan", "nivel": 7, "posicao": "Meia", "status": "fora"},
    {"nome": "Carlinho", "nivel": 5, "posicao": "Zagueiro", "status": "fora"},
    {"nome": "Renan", "nivel": 9, "posicao": "Meia", "status": "dentro"},
    {"nome": "Flavio", "nivel": 6, "posicao": "Atacante", "status": "dentro"},
    {"nome": "Eduardo", "nivel": 6, "posicao": "Zagueiro", "status": "dentro"},
    {"nome": "Kaio", "nivel": 5, "posicao": "Zagueiro", "status": "dentro"},
    {"nome": "Douglas", "nivel": 9, "posicao": "Meia", "status": "dentro"},
    {"nome": "Thiago", "nivel": 8, "posicao": "Atacante", "status": "dentro"},
    {"nome": "Vinicius", "nivel": 9, "posicao": "Zagueiro", "status": "dentro"},
    {"nome": "Tadeu", "nivel": 5, "posicao": "Zagueiro", "status": "dentro"},
    {"nome": "Cristian", "nivel": 7, "posicao": "Zagueiro", "status": "fora"},
    {"nome": "Andre", "nivel": 6, "posicao": "Zagueiro", "status": "fora"},
    {"nome": "Tiago", "nivel": 6, "posicao": "Atacante", "status": "dentro"},
    {"nome": "Gabriel", "nivel": 9, "posicao": "Meia", "status": "dentro"},
    {"nome": "Elvis", "nivel": 7, "posicao": "Zagueiro", "status": "dentro"},
    {"nome": "Luiz Felipe", "nivel": 9, "posicao": "Atacante", "status": "dentro"},
    {"nome": "Marcelo", "nivel": 9, "posicao": "Zagueiro", "status": "dentro"},
    {"nome": "Ozeas", "nivel": 3, "posicao": "Zagueiro", "status": "dentro"},
    {"nome": "Bruno", "nivel": 7, "posicao": "Zagueiro", "status": "dentro"},
    {"nome": "Felipe", "nivel": 9, "posicao": "Meia", "status": "fora"},
    {"nome": "Ramom", "nivel": 8, "posicao": "Meia", "status": "dentro"},
    {"nome": "Lucas", "nivel": 7, "posicao": "Meia", "status": "dentro"}
]

# Filtra jogadores "dentro"
jogadores_dentro = [jogador for jogador in jogadores if jogador["status"] == "dentro"]

# Ordena jogadores por nível (do maior para o menor)
jogadores_dentro.sort(key=lambda x: x["nivel"], reverse=True)

# Função para criar grupos equilibrados
def criar_grupos(jogadores, tamanho_grupo=5):
    num_jogadores = len(jogadores)
    num_grupos_cheios = num_jogadores // tamanho_grupo
    num_jogadores_restantes = num_jogadores % tamanho_grupo
    
    grupos = [[] for _ in range(num_grupos_cheios + (1 if num_jogadores_restantes > 0 else 0))]
    niveis_grupos = [0] * len(grupos)

    # Adiciona jogadores aos grupos de maneira balanceada
    for jogador in jogadores:
        # Encontra o grupo com o menor nível total e ainda não está cheio
        if len(grupos[0]) < tamanho_grupo:
            indice_melhor_grupo = 0
        elif len(grupos[1]) < tamanho_grupo:
            indice_melhor_grupo = 1
        elif len(grupos[2]) < tamanho_grupo:
            indice_melhor_grupo = 2
        else:
            indice_melhor_grupo = niveis_grupos.index(min(niveis_grupos))
        
        grupos[indice_melhor_grupo].append(jogador)
        niveis_grupos[indice_melhor_grupo] += jogador["nivel"]

    return grupos

# Cria os grupos
grupos = criar_grupos(jogadores_dentro)

# Exibe os grupos
for idx, grupo in enumerate(grupos):
    print(f"Grupo {idx + 1}:")
    for jogador in grupo:
        print(f"  {jogador['nome']} - Nível: {jogador['nivel']}")
    print()
