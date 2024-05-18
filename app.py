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

# def sortear_times(jogadores):
#   # Dividir jogadores por posição
#   goleiros = [jogador for jogador in jogadores 
#                 if jogador['posicao'] == 'goleiro'
#   ]
#   print (goleiros)
#   outros_jogadores = [
#       jogador for jogador in jogadores if jogador['posicao'] != 'goleiro'
#   ]
#   # Garantir que os goleiros não caiam no mesmo time
#   random.shuffle(goleiros)
#   meio_goleiros = len(goleiros) // 2
#   goleiros_time1 = goleiros[:meio_goleiros]
#   goleiros_time2 = goleiros[meio_goleiros:]

#   # Sortear os outros jogadores de forma equilibrada
#   random.shuffle(outros_jogadores)
#   meio_outros = len(outros_jogadores) // 2
#   outros_time1 = outros_jogadores[:meio_outros]
#   outros_time2 = outros_jogadores[meio_outros:]

#   time1 = goleiros_time1 + outros_time1
#   time2 = goleiros_time2 + outros_time2

#   # Calcular somatório dos níveis para cada time
#   somatorio_niveis_time1 = sum(jogador['nivel'] for jogador in time1)
#   somatorio_niveis_time2 = sum(jogador['nivel'] for jogador in time2)

#   return {
#       "time1": time1,
#       "time2": time2,
#       "somatorio_niveis_time1": somatorio_niveis_time1,
#       "somatorio_niveis_time2": somatorio_niveis_time2
#   }

def realizar_sorteio():
    jogadores = carregar_jogadores()

    # Verificar se há jogadores pendentes
    if any(jogador['status'] == 'pendente' for jogador in jogadores):
        mensagem = "Aguarde até que todos os jogadores confirmem o status."
        return None, mensagem
    else:
        # Filtrar jogadores que estão dentro
        jogadores_dentro = [
            jogador for jogador in jogadores if jogador['status'] == 'dentro'
        ]
        goleiro_dentro = [
           jogador for jogador in jogadores if jogador['status'] == 'dentro' and jogador['posicao'] == 'Goleiro'
        ]

        # Ordenar jogadores por posição desejada
        posicoes_desejadas = ['Goleiro', 'Zagueiro', 'Meia', 'Atacante']
        jogadores_dentro.sort(
            key=lambda x: (posicoes_desejadas.index(x['posicao']), x['nivel']))

        print (len(jogadores_dentro))
        print (len(goleiro_dentro))

        numero_jogadores = len(jogadores_dentro)-len(goleiro_dentro)
        if numero_jogadores <=10:
          num_times = 2
        elif numero_jogadores >10 and numero_jogadores <15:
          num_times = 3
        elif numero_jogadores >=15:
           num_times =4

        print (num_times)

        # Dividir jogadores por nota e posição
        #jogadores_dentro.sort(key=lambda x: (x['nivel'], x['posicao']))

        # Dividir jogadores em mnos times, garantindo equilíbrio nas notas e posições
        time1 = ""
        time2 = ""
        time3 = ""
        time4 = ""
        if num_times == 2:
          time1 = jogadores_dentro[::2]
          time2 = jogadores_dentro[1::2]

          print ("time 1: " + str(len(time1)))
          print ("time 2: " + str(len(time2)))

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
          time1 = jogadores_dentro[::3]
          time2 = jogadores_dentro[1::3]
          time3 = jogadores_dentro[2::3]

          print ("time 1: " + str(len(time1)))
          print ("time 2: " + str(len(time2)))
          print ("time 3: " + str(len(time3)))

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
          time1 = jogadores_dentro[::4]
          time2 = jogadores_dentro[1::4]
          time3 = jogadores_dentro[2::4]
          time4 = jogadores_dentro[3::4]

          print ("time 1: " + str(len(time1)))
          print ("time 2: " + str(len(time2)))
          print ("time 3: " + str(len(time3)))
          print ("time 4: " + str(len(time4)))

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