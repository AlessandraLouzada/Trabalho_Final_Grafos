from math import*
import time
import timeit
import networkx as nx
import matplotlib.pyplot as plt

##################################################################################
inicio = time.time() #Para calculo do tempo de execuçao
print("Digite o nome do arquivo que deseja executar: ")
nome= input() #Pega do usuario o nome do arquivo 
arquivo = open(nome+".txt", "r")#Abre o arquivo
linha = arquivo.readline() #Lê toda a linha
espaco = linha.split() #Separa em espaços a linha
dimensao = int(espaco[2]) #Salva em dimensao a quantidade de cidades do arquivo



linha = arquivo.readline() #Lê toda a linha
espaco = linha.split()#Separa em espaços a linha
veiculos = int(espaco[2]) #Salva em veiculos a quantidade de veiculos do arquivo

linha = arquivo.readline() #Lê toda a linha
espaco = linha.split()#Separa em espaços a linha
sets = int(espaco[2]) #Salva em sets a quantidade de regioes do arquivo

linha = arquivo.readline() #Lê toda a linha
espaco = linha.split()#Separa em espaços a linha
capacidade = int(espaco[2]) #Salva em capacidade a capaidade dos veiculos do arquivo

cidade=[] #Cidade onde tem um caminhão
cidade.append(0)
veiculoCapacidade = {} # Capacidade atual de cada caminhão
caminho = {} #Caminho percorrido por cada caminhão
vetorCaminhao = {} #Dicionario que armazena as cidade que um caminhão pode ir
qtdSets = {} #Dicionario que armazena para quantas regioes um determinado caminhão pode ir e atender sua demanda


saiu = 0 #Variavel para controle 
capacidadeTotal = veiculos*capacidade # Variavel para armazenar qual a capacidade total 
demandaTotal = 0 # Variavel que calcula qual é minha demanda total, para saber qual função chamar
distPercorrida = 0 #Variavel que calcula qual é minha distancia percorrida, para poder calcular o numero de respostas no fim

vetorDist=[] #Vetor que armazena as distancias das cidades que meu caminhão ainda pode ir. Usado quando a demandaTotal é igual a capacidadeTotal e meu caminhão não pode ir para algum lugar		
vetorDemanda=[] #Vetor que contem as demandas de todas as regioes
matrizSets = [] # Matriz com o conjunto de regioes
matrizDist= [] #Matriz com as distancias calculadas de todos para todos
distGalpao = [] #Vetor com a distancia das cidades para o galpão

#Inicializar os dicionarios, suas chaves serao os caminhoes
for i in range(1,veiculos+1):
	veiculoCapacidade[i] = capacidade
	caminho[i] = []
	vetorCaminhao[i] = []
	qtdSets[i]=[]
	caminho[i].append(1)




##################################################################################

#Função que calcula a distancia
def dist(x1,y1,x2,y2):
	distancia = sqrt(((x1-x2)**2) + ((y1-y2)**2))
	return int(distancia)

#Função que exclui a cidade que ja foi visitada e visitou outra cidade a partir dela. Chamada quando a demandaTotal é igual a capacidadeTotal.
#Manda como parametro a cidade a ser excluida
def exluirCidadeVisitadaIgual(cidadeAnterior):
	excluir=-1
	if cidadeAnterior+1 != 1:
		for e in range(len(cidade)):
			if cidade[e] == cidadeAnterior:
				excluir=e
		if(excluir!=-1):
			del(cidade[excluir])
	#Quando saiu for igual a veiculo, significa que não tenho mais veiculos no meu deposito, logo posso excluir ela da minha lista
	else:
		if saiu == veiculos:
			del(cidade[0])
			
#Função que adiciona uma cidade ao caminho. Chamada quando a demandaTotal é igual a capacidadeTotal.
#Manda como parametro a cidadeAnterior e Ciadade Proxima esta a cidade a ser adicionada no caminho e aquela a cidade pela qual cheguei nesta.
def addCaminhoIgual(cidadeAnterior, cidadeProxima):
	#Variavel de controle que recebe true quando a cidade é adicionada, para interromper o laço de repetição
	adicionou=False
	# Laço para verificar qual caminhão deve ir para a cidade a ser adicionada
	for caminhao in caminho:
		
		ultimo = len(caminho[caminhao])-1
		#Caso a cidadeAnterior seja igual a ultima cidade do caminhão, minha cidadeProxima será adicionada no caminho desse caminhão
		if cidadeAnterior == caminho[caminhao][ultimo]:
			global distPercorrida
			#Quando a cidadeAnterior for igual a 1, a variavel saiu sera somada em mais um, para controle de quantas vezes posso sair do deposito
			if cidadeAnterior == 1:
				global saiu
				saiu = saiu+1
			#Verifica a demanda da região da cidade que desejo ir
			demandaSet=verificarSet(cidadeProxima)
			#Para onde quero ir irá deixar minha capacidade negativa, tratar caso 
			if veiculoCapacidade[caminhao]!=0 and (veiculoCapacidade[caminhao]-vetorDemanda[demandaSet]) < 0:
				#Variavel para saber se existe algum caminho que posso fazer
				entrou = False
				#Percorrer o vetor de demanda
				for i in range(sets):
					#Se o vetor de demanda na posição i for menor que minha capacidade restante do caminhão
					if vetorDemanda[i]!= 0 and vetorDemanda[i] <= veiculoCapacidade[caminhao]:
						#Armazenar em vetorDist as cidades que consigo atender a demanda
						for j in range(len(matrizSets[i])):
							vetorDist.append (matrizSets[i][j])	
						#Muda para True caso exista alguma região que o caminhão possa ir 
						entrou=True
				#Caso tenha alguma região que consiga atender a demanda
				if entrou:
					#Percorre o tamanho de vetorDist
					for per in range(len(vetorDist)):
						menor = 0
						#Percorre novamente o tamanho de vetorDist para ver qual a menor distancia entre as cidades disponiveis
						for per in range(len(vetorDist)):
							#Troca o valor de menor se o valor da posição que eu estou na matrizDist é menor que menor
							if  matrizDist[cidadeAnterior-1][vetorDist[per]-1] < menor and matrizDist[cidadeAnterior-1][vetorDist[per]-1]!= 0 or menor == 0 :
								menor = matrizDist[cidadeAnterior-1][vetorDist[per]-1]
								#Salva como cidadeProxima a coluna corresponte do menor encontrado
								cidadeProxima=vetorDist[per]
						#Confere se consigo atender  demanda	
						if vetorDemanda[demandaSet]!=0 and (veiculoCapacidade[caminhao]-vetorDemanda[demandaSet]) >= 0:
							#Decremento a capacidade do caminhao a medida que percorro uma região
							veiculoCapacidade[caminhao] = veiculoCapacidade[caminhao]-vetorDemanda[demandaSet]
							#Marco como zero para saber que a região ja foi visitada
							vetorDemanda[demandaSet]= 0
							#Adicionar a cidade na rota do caminhão
							caminho[caminhao].append(cidadeProxima)
							#Adicionar a cidadeProxima em cidade para saber as cidades ja percorridas e de quais posso sair
							cidade.append(cidadeProxima-1)
							#Excluir cidadeAnterior de cidade, pois ja não posso mais sair dela
							exluirCidadeVisitadaIgual(cidadeAnterior-1)
							#Incrementa a distPercorrida om o valor da distancia, para calculo do bkv no final
							distPercorrida = distPercorrida + menor
							#Marcar que cidadeProxima ja foi visitada
							excluirSet(matrizDist, dimensao, (cidadeProxima-1))
							#Recebe a cidade que acabou de ser incluida, para o proximo calculo
							cidadeAnterior=cidadeProxima
						#Verifica a demanda da região da cidade que desejo ir
						demandaSet=verificarSet(cidadeProxima)
						#Caso a capacidade do veiculo seja igual a 0, significa que não ha mais para onde ir
						if veiculoCapacidade[caminhao]==0:
							#Excluir cidadeAnterior de cidade, pois ja não posso mais sair dela
							exluirCidadeVisitadaIgual(cidadeAnterior-1)
							#Incrementa a distPercorrida com o valor da distancia, para calculo do bkv no final
							distPercorrida=distPercorrida + distGalpao[cidadeProxima]
				
			#Para onde quero ir consigo atender a demanda 
			elif veiculoCapacidade[caminhao]!=0 and (veiculoCapacidade[caminhao]-vetorDemanda[demandaSet]) >= 0:
				#Decremento a capacidade do caminhao a medida que percorro uma região
				veiculoCapacidade[caminhao] = veiculoCapacidade[caminhao]-vetorDemanda[demandaSet]
				#Marco como zero para saber que a região ja foi visitada				
				vetorDemanda[demandaSet]= 0
				#Adicionar a cidade na rota do caminhão
				caminho[caminhao].append(cidadeProxima)
				#Adicionar a cidadeProxima em cidade para saber as cidades ja percorridas e de quais posso sair				
				cidade.append(cidadeProxima-1)
				#Excluir cidadeAnterior de cidade, pois ja não posso mais sair dela
				exluirCidadeVisitadaIgual(cidadeAnterior-1)
				#Incrementa a distPercorrida com o valor da distancia, para calculo do bkv no final
				distPercorrida = distPercorrida + matrizDist[cidadeAnterior][cidadeProxima]
				#Marcar que cidadeProxima ja foi visitada
				excluirSet(matrizDist, dimensao, (cidadeProxima-1))
				#Troca o valor de adicionou para parar o laço
				adicionou=True
		#Caso adicionou seja igual a True, para o laço
		if adicionou:
			break
	
#Exclui do vetor cidade a cidade mandada por parametro
def exluirCidadeVisitada(cidadeAnterior):
	excluir=-1
	#Percorre o vetor de cidade
	for e in range(len(cidade)):
		#Verifica se o valor da posição que estou é igual a cidadeAnterior, se sim salva o valor de 'e' em excluir
		if cidade[e] == cidadeAnterior:
			excluir=e
	#Se excluir tiver sido alterado
	if(excluir!=-1):
		#Deletar essa posição do vetor
		del(cidade[excluir])

#Adiciona o caminho quando a demandaTotal é menor que a capacidadeTotal
def addCaminho (cidadeAnterior, cidadeProxima, caminhao):
	ultimo = len(caminho[caminhao])-1
	#Caso a cidadeAnterior seja igual a ultima cidade do caminhão, minha cidadeProxima será adicionada no caminho desse caminhão
	if cidadeAnterior == caminho[caminhao][ultimo]:
		#Verifica a demanda da região da cidade que desejo ir		
		demandaSet = verificarSet(cidadeProxima)
		#Para onde quero ir consigo atender a demanda 
		if (veiculoCapacidade[caminhao]-vetorDemanda[demandaSet]) > 0:
			#Adicionar a cidade na rota do caminhão
			caminho[caminhao].append(cidadeProxima)
			#Adicionar a cidadeProxima em cidade para saber as cidades ja percorridas e de quais posso sair							
			cidade.append(cidadeProxima-1)
			#Excluir cidadeAnterior de cidade, pois ja não posso mais sair dela
			exluirCidadeVisitada(cidadeAnterior-1)
			
#Verificar qual a regiao que a cidade esta
def verificarSet(cidadeProxima):
	for i in range(sets):
		for j in range(len(matrizSets[i])):
			#Se valor armazenado em matrizSets[i][j] for igual a cidadeProxima, retorna o valor de i, que corresponde a região da cidade
			if(matrizSets[i][j]==cidadeProxima):
				return i
	
#Marca como zero toda as cidades das regioes que ja foram vistadas
def excluirSet(matriz, tam, cidadeExcluir):
	#Marca como zero toda a coluna de cidadeExcluir
	for i in range(tam):
		matriz[i][cidadeExcluir] = 0
	
	for i in range(tam):
		#Verifica quais as cidades que estão na mesma regiao que cidade excluir e marca elas como zero
		if matriz[cidadeExcluir][i] == 0 and i!=cidadeExcluir:
			for j in range(tam):
				matriz[j][i] = 0
				
#TSP Vizinho mais proximo adaptado, para calcular qual a distancia mais proxima das cidades disponiveis em cidade. Chamada quando a demandaTotal e menor que a capacidadeTotal
def distanciaMaisProxima():
	#Percorrer os caminhoes, para verificar no caminho de qual posso adicionar a cidade
	for caminhao in caminho:
		cont = 0 
		#Percorrer a quantidade de regioes
		for j in range(sets):
			#Verifica se o camiinhao consegue ir para a região e atnder sua demanda
			if veiculoCapacidade[caminhao] - vetorDemanda[j] > 0 and vetorDemanda[j] != 0:
				#Percorre a quantidade salva na linha de matrizSets[j]
				for k in range(len(matrizSets[j])): 
					#Salva a cidade armazenada em matrizSets[j][k] no vetorCaminhao
					vetorCaminhao[caminhao].append(matrizSets[j][k])
				#Soma mais um em cont para saber quantas regioes o caminhão pode passar 
				cont=cont+1
				#Decremento a capacidade do caminhao a medida que salvo uma região no vetor
				veiculoCapacidade[caminhao]=veiculoCapacidade[caminhao]-vetorDemanda[j]
				#Recebe zero para saber que a região ja foi verificada				
				vetorDemanda[j]=0
		#Quantidade de regioes que o cada caminhão passa
		qtdSets[caminhao]=cont
	#Percorrer os caminhoes, para verificar no caminho de qual posso adicionar a cidade	
	for caminhao in caminho:
		menor = 0
		cidadeProxima = -1
		cidadeAnterior = -1	
		#Percorre o tamanho do vetorCaminhao na chave caminhao
		for k in range(len(vetorCaminhao[caminhao])):
			#Faz a comparação do menor caminho saindo do deposito para cada caminhão
			if matrizDist[0][(vetorCaminhao[caminhao][k])-1] < menor and matrizDist[0][(vetorCaminhao[caminhao][k]-1)]!=0 or menor == 0:
				menor = matrizDist[0][(vetorCaminhao[caminhao][k]-1)] 
				cidadeAnterior = 1
				cidadeProxima = vetorCaminhao[caminhao][k]
		#Muda o valor de saiu para caminhão, pois todos os meus caminhões ja sairam do deposito
		global saiu
		saiu = caminhao
		#Chama a função para adicionar cidadeProxima no meu caminho
		addCaminho (cidadeAnterior, cidadeProxima, caminhao)
		#Incrementa a distPercorrida com o valor da distancia, para calculo do bkv no final
		global distPercorrida
		distPercorrida = distPercorrida + menor
		#Marcar que cidadeProxima ja foi visitada
		excluirSet(matrizDist, dimensao, (cidadeProxima-1))
		#Variavel de controle
		aux=0
		# Enquanto a variavel de controle foi diferente do valor de qtdSets[caminhao]
		while aux != qtdSets[caminhao]:
			#Chama a função percorre para calcular o caminho do caminhão
			per=percorrer(caminhao)
			#Retira do vetor cidade a per, que foi a cidade retornada
			exluirCidadeVisitada(per)
			aux=aux+1
		#Incrementa a distPercorrida com o valor da distancia, para calculo do bkv no final
		distPercorrida=distPercorrida+distGalpao[per]

#Calcula a distancia mais proxima a ser percorrida pelo caminhão 	
def percorrer(caminhao):
	#Percorre o vetor cidade
	for l in cidade:
			menor = 0
			cidadeProxima = -1
			cidadeAnterior = -1	
			#Percorre o tamanho do vetorCaminhao na chave caminhao
			for i in range(len(vetorCaminhao[caminhao])):
				#Faz a comparação do menor caminho saindo da cidade l para o caminhão
				if matrizDist[l][(vetorCaminhao[caminhao][i])-1] < menor and matrizDist[l][(vetorCaminhao[caminhao][i]-1)]!=0 or menor == 0:
					menor = matrizDist[l][(vetorCaminhao[caminhao][i]-1)] 
					cidadeAnterior = l+1
					cidadeProxima = (vetorCaminhao[caminhao][i])
			#Caso menor seja diferente de 0
			if menor!=0:
				#Chama a função addCaminho para adicionar a cidadeProxima no caminho do caminhao 
				addCaminho (cidadeAnterior, cidadeProxima, caminhao)
				#Incrementa a distPercorrida com o valor da distancia, para calculo do bkv no final
				global distPercorrida
				distPercorrida = distPercorrida + menor
			#Marcar que cidadeProxima ja foi visitada
			excluirSet(matrizDist, dimensao, (cidadeProxima-1))
	#Retorna a cidade a ser removida do vetor cidade
	return l

#TSP Vizinho mais proximo adaptado, para calcular qual a distancia mais proxima das cidades disponiveis em cidade. Chamada quando a demandaTotal e menor que a capacidadeTotal 
def distanciaMaisProximaIgual(matriz, tam):
		menor = 0
		cidadeProxima = -1
		cidadeAnterior = -1
		#Percorre o vetor cidade
		for l in cidade:
			#'i' vai ate o tam(dimensao)
			for i in range(tam):
				#Faz a comparação do menor caminho saindo da cidade l
				if matriz[l][i] < menor and matriz[l][i] != 0 or menor == 0:
					menor = matriz[l][i]
					cidadeAnterior = l+1
					cidadeProxima = i+1
		
		#Caso menor seja diferente de 0
		if menor!=0 :
			#Chama a função addCaminho para adicionar a cidadeProxima no caminho de algum caminhao 
			addCaminhoIgual(cidadeAnterior, cidadeProxima)	


def main():
	linha = arquivo.readline() #Salta os espaços que indicam o que cada dado representa
	espaco = linha.split()
	linha = arquivo.readline() #Salta os espaços que indicam o que cada dado representa
	espaco = linha.split()
	
	##################################################################################
	#Matriz que conterá as cordenadas
	matrizCord = []
	#'i' vai ate dimensao
	for i in range(dimensao):
		linha = arquivo.readline() #Lê toda a linha
		espaco = linha.split() #Separa em espaços a linha
		#Vetor que recebe os dados
		tmp = []
		#'j' vai ate 3
		for j in range(3):
			elemento = int(espaco[j]) #elemento recebe o que esta na posição j de espaco
			tmp.append(elemento) #Adiciona elemento no vetor temp
		matrizCord.append(tmp[:]) #Adiciona o vetor temp como linha da matrizCord

	
	#################################################################################
	linha = arquivo.readline() #Salta os espaços que indicam o que cada dado representa
	espaco = linha.split() 
	#'i' vai ate sets
	for i in range(sets):
		linha = arquivo.readline() #Lê toda a linha
		espaco = linha.split() #Separa em espaços a linha
		#Vetor que recebe os dados
		aux = []
		cont = int(espaco[1]) #cont recebe o que esta na posição j de espaco
		ite=2 # ite começa em 2, pois já recebi uma posição
		#Para o laço quando cont for -1
		while cont != -1:
			aux.append(cont) #Adiciona elemento no vetor aux
			cont = int(espaco[ite]) #cont recebe o que esta na posição ite de espaco
			ite=ite+1 #Soma mais um a ite
		matrizSets.append(aux[:]) #Adiciona o vetor aux como linha da matrizSets

	##################################################################################
	linha = arquivo.readline()  #Salta os espaços que indicam o que cada dado representa
	espaco = linha.split() 
	#'i' vai ate sets
	for i in range(sets):
		ite=1 #ite começa em 1, pois já recebi uma posição
		linha = arquivo.readline() #Lê toda a linha
		espaco = linha.split() #Separa em espaços a linha
		vetorDemanda.append(int(espaco[ite])) #Adiciona  em vetorDemanda o que esta na posição ite de espaco
		#Incrementa a demandaTotal com o valor que esta na posição ite de espaco
		global demandaTotal
		demandaTotal=demandaTotal+ int(espaco[ite])
		
	arquivo.close() #Fecha o arquivo
	
	##################################################################################
	#'i' vai ate dimensao
	for i in range(dimensao):
		#Vetor que recebe os dados
		coluna = []
		#'j' vai ate dimensao
		for j in range(dimensao):
			#Se estiver no galpão
			if i == 0:
				if(j!=0):
					#Chama a função dist para calcular a distancia das cordenadas passadas por parametro
					distancia = dist(matrizCord[i][1],matrizCord[i][2],matrizCord[j][1],matrizCord[j][2])
					coluna.append(distancia) #Adiciona em coluna distancia
				#Se j for igual a 0 
				else:
					coluna.append(0) #Adiciona em coluna 0
			#Se i for diferente de 0
			else:
				coluna.append(0) #Adiciona em coluna 0
		matrizDist.append(coluna[:])  #Adiciona coluna como linha da matrizdDist
	
	#'linha1' vai ate sets
	for linha1 in range(sets):
		#'coluna1' vai ate o tamanho de matrizSets[linha1]
		for coluna1 in range(len(matrizSets[linha1])):
			#local recebe o valor de matrizSets[linha1][coluna1]
			local = matrizSets[linha1][coluna1]
			#'linha2' vai ate sets
			for linha2 in range(sets):
				if (linha2 != linha1):
					#'coluna2' vai ate o tamanho de matrizSets[linha2]
					for coluna2 in range(len(matrizSets[linha2])):
						#local2 recebe o valor de matrizSets[linha1][coluna1]
						local2 = matrizSets[linha2][coluna2]
						#Chama a função dist para calcular a distancia das cordenadas passadas por parametro
						distancia=dist(matrizCord[local-1][1], matrizCord[local-1][2],matrizCord[local2-1][1],matrizCord[local2-1][2])
						matrizDist[local-1][local2-1]=distancia #Adiciona distancia nessa posição da matriz

	###############################################################################
	print("Caso queira gerar uma imagem, digite -img, e nome do arquivo")
	respImg = input()#Recebe o que o usuario digitar
	nomeImg=input()#Nome da imagem
	print("Caso queira gerar uma rota detalhada, digite -sol, e nome do arquivo")
	respSol =   input()#Recebe o que o usuario digitar
	nomeSol= input()#Nome do arquivo
	#Calcula a distancia do das cidades para o galpão
	for i in range(dimensao):
		distGalpao.append(matrizDist[0][i])
		
	#Se a demandaTotal for igual a capacidadeTotal, chamarei as funçoes destinadas para isso
	if demandaTotal == capacidadeTotal:
		distanciaMaisProximaIgual(matrizDist, dimensao)
		for i in range(sets):
			distanciaMaisProximaIgual(matrizDist, dimensao)
	#Se a demandaTotal for menor que  a capacidadeTotal, chamarei as funçoes destinadas para isso
	elif demandaTotal < capacidadeTotal:
		distanciaMaisProxima()
		
	fim = time.time() #Para calculo do tempo de execuçao
	tempo = fim-inicio #Armazena o tempo gasto
	
	#Abrir arquivo para calculo do bkv
	arquivo2= open("bkv.txt", 'r')
	encontrou=False
	while encontrou == False:
		linha = arquivo2.readline() #Lê toda a linha do arquivo
		espaco = linha.split() #Separa em espaços a linha
		#Se o que tem em espaco[0] for igual a nome, bkv recebe o conteudo de espaco[1] e troco entrou para true
		if espaco[0] == nome:
			bkv=int(espaco[1])
			encontrou=True
	#Calculodo bkv
	resposta = int(((distPercorrida-bkv)/bkv)*100) 
	arq = open("alessandra-201810966-resultados.txt", 'a') #Abre o arquivo para gravar os resultados
	arq.write(nome) 
	arq.write(' ')
	arq.write(str(resposta))
	arq.write(' ')
	arq.write(str(tempo))
	arq.write('\n')
	arq.close()

	if(respImg == "-img"):
		
		dici = {} 
		dici[1]=[]
		for caminhao in caminho:
			dici[1].append(caminho[caminhao][1])
			for i in range(1,len(caminho[caminhao])):
				if i == (len(caminho[caminhao])-1):
					dici[caminho[caminhao][i]] = []
					dici[caminho[caminhao][i]].append(1)
				else:
					dici[caminho[caminhao][i]] = []
					dici[caminho[caminhao][i]].append(caminho[caminhao][i+1])			
			
		G = nx.Graph(dici) #liga cada caminho que cada caminhao fez 
		edges = G.edges()
		pos = nx.circular_layout(G)
		edge_labels = nx.get_edge_attributes(G,'subtitle')
		nx.draw(G,pos,with_labels=True)
		nx.draw_networkx_edge_labels(G,pos,with_labels=True, edge_labels=edge_labels,font_size=8) # desenha o grafo
		
		plt.savefig(nomeImg, dpi=199)
		plt.show() # mostra na tela
		
	if(respSol == "-sol"):
		arqRota = open(nomeSol, 'w') #Escreve a rota no arquivo 
		#Percorre para saber a rota de cada caminhão
		for caminhao in caminho:
			arqRota.write(str(caminhao))
			arqRota.write(" ")
			#Percorre o tamanho de caminho na chave caminhão
			for i in range(len(caminho[caminhao])):
				arqRota.write(str(caminho[caminhao][i]))
				arqRota.write(" ")
			arqRota.write('\n')
		
		arqRota.close()


main()

