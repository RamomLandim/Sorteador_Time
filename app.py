# app.py
from flask import Flask, render_template, request, redirect, url_for
import os
import json
import random

# *********************** MAIN *********************************

app = Flask(__name__)

def carregar_jogadores(caminho_arquivo='jogadores.json'):
    # Obtenha o caminho absoluto para o diretório do script
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Construa o caminho completo para o arquivo de jogadores
    caminho_arquivo_completo = os.path.join(diretorio_atual, caminho_arquivo)

    try:
        with open(caminho_arquivo_completo, 'r') as file:
            jogadores = json.load(file)
    except FileNotFoundError:
        jogadores = []

    return jogadores

jogadores = carregar_jogadores()  # usa o caminho padrão 'jogadores.json'

def salvar_jogadores(jogadores):
  with open('jogadores.json', 'w') as file:
    json.dump(jogadores, file, indent=2)


def criar_tabela_jogadores():
  jogadores = carregar_jogadores()
  salvar_jogadores(jogadores)

def adicionar_jogador(nome, nivel, posicao):
  jogadores = carregar_jogadores()
  jogadores.append({
      "nome": nome.upper(),
      "nivel": nivel,
      "posicao": posicao,
      "status": 'pendente'
  })
  salvar_jogadores(jogadores)

def realizar_sorteio():
    jogadores = carregar_jogadores()

    # Verificar se há jogadores pendentes
    if any(jogador['status'] == 'pendente' for jogador in jogadores):
        mensagem = "Aguarde até que todos os jogadores confirmem o status."
        return None, mensagem
    else:
        # Filtrar jogadores que estão dentro
        jogadores_dentro = [
            jogador for jogador in jogadores if jogador['status'] == 'dentro' and jogador['posicao'] != 'Goleiro'
        ]
        goleiro_dentro = [
           jogador for jogador in jogadores if jogador['status'] == 'dentro' and jogador['posicao'] == 'Goleiro'
        ]

        # Ordena jogadores por nível (do maior para o menor)
        jogadores_dentro.sort(key=lambda x: (x['nivel']), reverse=True)
        
        random.shuffle(jogadores_dentro)
        random.shuffle(goleiro_dentro)

        for i in reversed(goleiro_dentro):
          jogadores_dentro.insert(0,i)

        numero_jogadores = len(jogadores_dentro)-len(goleiro_dentro)
        if numero_jogadores <=10:
          num_times = 2
        elif numero_jogadores >10 and numero_jogadores <15:
          num_times = 3
        elif numero_jogadores >=15:
           num_times = 4

        # Dividir jogadores em mnos times, garantindo equilíbrio nas notas e posições
        time1 = ""
        time2 = ""
        time3 = ""
        time4 = ""
        
        somas = [0 for _ in range(num_times)]
        if num_times == 2:
          somas = [0 for _ in range(2)]
          grupos = [[],[]]
          
          index = 0
          while index < len(jogadores_dentro):
            # Encontrar o grupo com a menor soma atual
            indice_grupo = somas.index(min(somas))
            # Adicionar a pessoa ao grupo e atualizar a soma
            pessoa = jogadores_dentro[index]
            grupos[indice_grupo].append(pessoa)
            somas[indice_grupo] += pessoa["nivel"]
            # Incrementar o índice
            index += 1

          time1 = grupos[0]
          time2 = grupos[1]

          if len(time1)>6:
            time1.sort(key=lambda x: (x['nivel'], x['posicao']))
            if time1[len(time1)-1]['posicao'] == 'Goleiro':
              time2.append(time1[len(time1)-2])
              time1.pop(len(time1)-2)
            else:
              time2.append(time1[len(time1)-1])
              time1.pop(len(time1)-1)

          somatorio_niveis_time1 = sum(jogador['nivel'] for jogador in time1)
          somatorio_niveis_time2 = sum(jogador['nivel'] for jogador in time2)

          porcentagem_goleiros_zagueiros_time1, porcentagem_meia_time1, porcentagem_atacante_time1 = calculo_time(time1)
          porcentagem_goleiros_zagueiros_time2, porcentagem_meia_time2, porcentagem_atacante_time2 = calculo_time(time2)

          times_sorteados = {
          "time1": time1,
          "time2": time2,
          "somatorio_niveis_time1": somatorio_niveis_time1,
          "somatorio_niveis_time2": somatorio_niveis_time2,
          "porcentagem_goleiros_zagueiros_time1": porcentagem_goleiros_zagueiros_time1,
          "porcentagem_meia_time1": porcentagem_meia_time1,
          "porcentagem_atacante_time1": porcentagem_atacante_time1,
          "porcentagem_goleiros_zagueiros_time2": porcentagem_goleiros_zagueiros_time2,
          "porcentagem_meia_time2": porcentagem_meia_time2,
          "porcentagem_atacante_time2": porcentagem_atacante_time2
          }
        elif num_times == 3:
          somas = [0 for _ in range(3)]
          grupos = [[] for _ in range(3)]
          
          index = 0
          while index < len(jogadores_dentro):
            # Encontrar o grupo com a menor soma atual
            indice_grupo = somas.index(min(somas))
            # Adicionar a pessoa ao grupo e atualizar a soma
            pessoa = jogadores_dentro[index]
            grupos[indice_grupo].append(pessoa)
            somas[indice_grupo] += pessoa["nivel"]
            # Incrementar o índice
            index += 1

          time1 = grupos[0]
          time2 = grupos[1]
          time3 = grupos[2]

          index = 0
          while index <6:
            if len(time1)<6:
              time3.sort(key=lambda x: (x['nivel'], x['posicao']))
              if time3[len(time3)-1]['posicao'] == 'Goleiro':
                time1.append(time3[len(time3)-2])
                time3.pop(len(time3)-2)
              else:
                time1.append(time3[len(time3)-1])
                time3.pop(len(time3)-1)
            index = len(time1)
          
          while index <6:
            if len(time2)<6:
              time3.sort(key=lambda x: (x['nivel'], x['posicao']))
              if time3[len(time3)-1]['posicao'] == 'Goleiro':
                time2.append(time3[len(time3)-2])
                time3.pop(len(time3)-2)
              else:
                time2.append(time3[len(time3)-1])
                time3.pop(len(time3)-1)
            index = len(time2)
             

          somatorio_niveis_time1 = sum(jogador['nivel'] for jogador in time1)
          somatorio_niveis_time2 = sum(jogador['nivel'] for jogador in time2)
          somatorio_niveis_time3 = sum(jogador['nivel'] for jogador in time3)

          porcentagem_goleiros_zagueiros_time1, porcentagem_meia_time1, porcentagem_atacante_time1 = calculo_time(time1)
          porcentagem_goleiros_zagueiros_time2, porcentagem_meia_time2, porcentagem_atacante_time2 = calculo_time(time2)
          porcentagem_goleiros_zagueiros_time3, porcentagem_meia_time3, porcentagem_atacante_time3 = calculo_time(time3)

          times_sorteados = {
          "time1": time1,
          "time2": time2,
          "time3": time3,
          "somatorio_niveis_time1": somatorio_niveis_time1,
          "somatorio_niveis_time2": somatorio_niveis_time2,
          "somatorio_niveis_time3": somatorio_niveis_time3,
          "porcentagem_goleiros_zagueiros_time1": porcentagem_goleiros_zagueiros_time1,
          "porcentagem_meia_time1": porcentagem_meia_time1,
          "porcentagem_atacante_time1": porcentagem_atacante_time1,
          "porcentagem_goleiros_zagueiros_time2": porcentagem_goleiros_zagueiros_time2,
          "porcentagem_meia_time2": porcentagem_meia_time2,
          "porcentagem_atacante_time2": porcentagem_atacante_time2,
          "porcentagem_goleiros_zagueiros_time3": porcentagem_goleiros_zagueiros_time3, 
          "porcentagem_meia_time3": porcentagem_meia_time3,
          "porcentagem_atacante_time3": porcentagem_atacante_time3
          }
        else:
          somas = [0 for _ in range(4)]
          grupos = [[] for _ in range(4)]
          
          index = 0
          while index < len(jogadores_dentro):
            # Encontrar o grupo com a menor soma atual
            indice_grupo = somas.index(min(somas))
            # Adicionar a pessoa ao grupo e atualizar a soma
            pessoa = jogadores_dentro[index]
            grupos[indice_grupo].append(pessoa)
            somas[indice_grupo] += pessoa["nivel"]
            # Incrementar o índice
            index += 1
          
          time1 = grupos[0]
          time2 = grupos[1]
          time3 = grupos[2]
          time4 = grupos[3]
          
          time1, time2 = recalcula_grupo(time1,time2)
          time2, time3 = recalcula_grupo(time2,time3)
          time3, time4 = recalcula_grupo(time3,time4)

          index = len(time1)
          while index <6:
            if len(time1)<6:
              time4.sort(key=lambda x: (x['nivel'], x['posicao']))
              if time4[len(time4)-1]['posicao'] == 'Goleiro':
                time1.append(time4[len(time4)-2])
                time4.pop(len(time4)-2)
              else:
                time1.append(time4[len(time4)-1])
                time4.pop(len(time4)-1)
            elif len(time1)>6:
              time4.append(time1[len(time1)-1])
              time1.pop(len(time1)-1)
            index = len(time1)

          index = len(time2)
          while index <6:
            if len(time2)<6:
              time4.sort(key=lambda x: (x['nivel'], x['posicao']))
              if time4[len(time4)-1]['posicao'] == 'Goleiro':
                time2.append(time4[len(time4)-2])
                time4.pop(len(time4)-2)
              else:
                time2.append(time4[len(time4)-1])
                time4.pop(len(time4)-1)
            elif len(time2)>6:
              time4.append(time2[len(time2)-1])
              time2.pop(len(time2)-1)
            index = len(time2)

          index = len(time3)
          while index <6:
            if len(time3)<6:
              time4.sort(key=lambda x: (x['nivel'], x['posicao']))
              if time4[len(time4)-1]['posicao'] == 'Goleiro':
                time3.append(time4[len(time4)-2])
                time4.pop(len(time4)-2)
              else:
                time3.append(time4[len(time4)-1])
                time4.pop(len(time4)-1)
            index = len(time2)

          somatorio_niveis_time1 = sum(jogador['nivel'] for jogador in time1)
          somatorio_niveis_time2 = sum(jogador['nivel'] for jogador in time2)
          somatorio_niveis_time3 = sum(jogador['nivel'] for jogador in time3)
          somatorio_niveis_time4 = sum(jogador['nivel'] for jogador in time4)

          porcentagem_goleiros_zagueiros_time1, porcentagem_meia_time1, porcentagem_atacante_time1 = calculo_time(time1)
          porcentagem_goleiros_zagueiros_time2, porcentagem_meia_time2, porcentagem_atacante_time2 = calculo_time(time2)
          porcentagem_goleiros_zagueiros_time3, porcentagem_meia_time3, porcentagem_atacante_time3 = calculo_time(time3)
          porcentagem_goleiros_zagueiros_time4, porcentagem_meia_time4, porcentagem_atacante_time4 = calculo_time(time4)
          
          times_sorteados = {
          "time1": time1,
          "time2": time2,
          "time3": time3,
          "time4": time4,
          "somatorio_niveis_time1": somatorio_niveis_time1,
          "somatorio_niveis_time2": somatorio_niveis_time2,
          "somatorio_niveis_time3": somatorio_niveis_time3,
          "somatorio_niveis_time4": somatorio_niveis_time4,
          "porcentagem_goleiros_zagueiros_time1": porcentagem_goleiros_zagueiros_time1,
          "porcentagem_meia_time1": porcentagem_meia_time1,
          "porcentagem_atacante_time1": porcentagem_atacante_time1,
          "porcentagem_goleiros_zagueiros_time2": porcentagem_goleiros_zagueiros_time2,
          "porcentagem_meia_time2": porcentagem_meia_time2,
          "porcentagem_atacante_time2": porcentagem_atacante_time2,
          "porcentagem_goleiros_zagueiros_time3": porcentagem_goleiros_zagueiros_time3, 
          "porcentagem_meia_time3": porcentagem_meia_time3,
          "porcentagem_atacante_time3": porcentagem_atacante_time3,
          "porcentagem_goleiros_zagueiros_time4": porcentagem_goleiros_zagueiros_time4, 
          "porcentagem_meia_time4": porcentagem_meia_time4,
          "porcentagem_atacante_time4": porcentagem_atacante_time4
          }

        return times_sorteados, None, num_times

def recalcula_grupo(time1,time2):
  tamanho1 = len(time1)
  tamanho2 = len(time2)

  if tamanho1 == tamanho2:
    print("times com mesmo numero")

  elif tamanho1 < tamanho2:
    i = 0
    index = tamanho2 - tamanho1
    while i < index:
      time2.sort(key=lambda x: (x['nivel'], x['posicao']))
      if time2[len(time2)-1]['posicao'] == 'Goleiro':
          time1.append(time2[len(time2)-2])
          time2.pop(len(time2)-2)
      else:
          time1.append(time2[len(time2)-1])
          time2.pop(len(time2)-1)
      i+=1

  elif  tamanho2 < tamanho1:
    i = 0
    index = tamanho1 - tamanho2
    while i < index:
      time1.sort(key=lambda x: (x['nivel'], x['posicao']))
      if time1[len(time1)-1]['posicao'] == 'Goleiro':
          time2.append(time1[len(time1)-2])
          time1.pop(len(time1)-2)
      else:
          time2.append(time1[len(time1)-1])
          time1.pop(len(time1)-1)
      i+=1

  return time1,time2



def criar_grupos(jogadores, tamanho_grupo=6):
    grupos = [[] for _ in range((len(jogadores) + tamanho_grupo - 1) // tamanho_grupo)]
    niveis_grupos = [0] * len(grupos)

    for jogador in jogadores:
        # Encontra o grupo com o menor nível total
        indice_melhor_grupo = niveis_grupos.index(min(niveis_grupos))
        grupos[indice_melhor_grupo].append(jogador)
        niveis_grupos[indice_melhor_grupo] += jogador["nivel"]

    return grupos

def calculo_time(time):
   # Calcular somatório dos níveis para cada setor do Time 1
        soma_niveis_goleiros_zagueiros_time1 = sum(jogador['nivel'] for jogador in time if jogador['posicao'] in ('Goleiro', 'Zagueiro'))
        soma_niveis_meias_time1 = sum(jogador['nivel'] for jogador in time if jogador['posicao'] == 'Meia')
        soma_niveis_atacantes_time1 = sum(jogador['nivel'] for jogador in time if jogador['posicao'] == 'Atacante')

        # Calcular somatório total dos níveis para o Time 1
        somatorio_niveis_time1 = soma_niveis_goleiros_zagueiros_time1 + soma_niveis_meias_time1 + soma_niveis_atacantes_time1

        # Cálculos de porcentagem para o Time 1
        porcentagem_goleiros_zagueiros_time1 = round((soma_niveis_goleiros_zagueiros_time1 / somatorio_niveis_time1) * 100)
        porcentagem_meia_time1 = round((soma_niveis_meias_time1 / somatorio_niveis_time1) * 100)
        porcentagem_atacante_time1 = round((soma_niveis_atacantes_time1 / somatorio_niveis_time1) * 100)

        return porcentagem_goleiros_zagueiros_time1, porcentagem_meia_time1, porcentagem_atacante_time1
  

@app.route('/sortear', methods=['POST'])
def sortear():
  times_sorteados, mensagem_erro, num_times = realizar_sorteio()

  if num_times == 2:
    if times_sorteados:
      return render_template('resultado.html', resultado_sorteio=times_sorteados)
    else:
      # print("Erro no sorteio:", mensagem_erro)
      return render_template('erro_sorteio.html', mensagem_erro=mensagem_erro)

  elif num_times == 3:
    if times_sorteados:
      return render_template('resultado_3.html', resultado_sorteio=times_sorteados)
    else:
      # print("Erro no sorteio:", mensagem_erro)
      return render_template('erro_sorteio.html', mensagem_erro=mensagem_erro)
  
  elif num_times == 4:
    if times_sorteados:
      return render_template('resultado_4.html', resultado_sorteio=times_sorteados)
    else:
      # print("Erro no sorteio:", mensagem_erro)
      return render_template('erro_sorteio.html', mensagem_erro=mensagem_erro)

@app.route('/', methods=['GET', 'POST'])
def index():
  criar_tabela_jogadores()

  if request.method == 'POST':
    nome = request.form['nome']
    try:
      nivel = int(request.form['nivel'])
      if not 0 <= nivel <= 10:
        raise ValueError("O nível deve estar entre 0 e 10.")
    except ValueError:
      return "Valor inválido para o nível. Insira um valor entre 0 e 10."

    posicao = request.form['posicao']
    adicionar_jogador(nome, nivel, posicao)

  jogadores = carregar_jogadores()
  return render_template('index.html', jogadores=jogadores)

@app.route('/resetar', methods=['POST'])
def resetar_status():
  jogadores = carregar_jogadores()
  for jogador in jogadores:
    jogador['status'] = 'pendente'
  salvar_jogadores(jogadores)
  return redirect(url_for('index'))

@app.route('/mudar_status/<nome>', methods=['POST'])
def mudar_status(nome):
  jogadores = carregar_jogadores()
  for jogador in jogadores:
    if jogador['nome'] == nome:
      novo_status = request.form.get('novo_status')
      jogador['status'] = novo_status
  salvar_jogadores(jogadores)
  return redirect(url_for('index')) 

if __name__ == '__main__':
    # Ativa o modo de depuração para reiniciar automaticamente o servidor em caso de alterações no código
    #app.run(host='0.0.0.0', port=9090, debug=True)
    app.run(debug=True)