#Bibliotecas requeridas para execução do código
import os #Biblioteca para limpar a consola
import requests #Biblioteca para fazer requisições no protocolo HTTP
from tabulate import tabulate #Biblioteca para imprimir dados esteticamente tabulados

#Menu principal do programa
def menu():
    print("""
[1] - Ver previsão do tempo
[2] - Sair
""")

def saudation():
    print("----------- BEM-VINDO A PREVISÃO DO TEMPO -----------")

#getting _cities: Função responsável por consumir a API que retorna os locais com seus respetivos id_locais
#Essa função requisita, trata, armazena em uma estrutura de dados e retorna os arquivos JSON devolvidos pela API
def getting_cities():
    datas_from_api = requests.get('https://api.ipma.pt/open-data/distrits-islands.json')
    datas_json = datas_from_api.json()
    
    locals = [(item["local"], item["globalIdLocal"]) for item in datas_json["data"]]
    return locals    

#showing_cities: Funçao responsável que exibe a lista de locais para o utilizador 
def showing_cities(LOCALS):
    ind = 1
    for local in LOCALS:
        print(f"[{ind}] - {local[0]}")
        ind += 1

#verify_option: Verifica se o indice escolhido pelo utilizador é valido
def verify_option(option, size_locals_list):
    if option.isnumeric():
        option_int = int(option)
        if option_int > size_locals_list:
            status = False
        else:
            status = True
    else:
        status = False
    
    return status

#getting_id_local: Função responsável por retornar uma tupla com: Nome da cidade e globalIdlocal da cidade
def getting_id_local(option, LOCALS):
    option = int(option)
    option -= 1
    for i in range(0, len(LOCALS)):
        if i == option:
            id_local = LOCALS[i]
            break
    return id_local

#preparing_resulst: Função responsável por consumir a API que retorna os índices requeridos, armazenar esses dados em uma estrutura
#formata-los com a função tabulate e retorna-los para serem exibidos em outra fução
def preparing_results(id_local):
    datas_from_api = requests.get(f"https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{id_local[1]}.json")
    datas_json = datas_from_api.json()
    
    indexes = [(item["forecastDate"], item["tMin"], item["tMax"], item["precipitaProb"]) for item in datas_json["data"]]
    
    headers = ["Data", "Mín", "Máx", "Probabilidade chuva (%)"]

    datas_tabulated = tabulate(indexes, headers=headers, tablefmt="grid")
    return datas_tabulated

#showing_results: Função responsável por exibir os dados vindos da função preparing_results
def showing_results(response, id_local):
    while True:
        os.system("cls")
        print(f"Cidade: {id_local[0]}")
        print(response)
        option = input("->Digite 0 p/a encerrar: ")
        if option == '0':
            os.system("cls")
            break

#call_api: Função responsável por abrigar a: Escolha do utilizador("getting_id_local"), resposta da requisição("preparing_results") e exibição #de resultados("showing_results")
def call_api(option, LOCALS):
    id_local = getting_id_local(option, LOCALS)
    response = preparing_results(id_local)
    showing_results(response, id_local)

#show_prevision: Função responsável por abrigar: 1º A recolha de nomes de local e id("getting_cities"), 2º Recolher a escolha do utilizador e 
#3º Direcionar os dados para a função call_api
def show_prevision():
    LOCALS = getting_cities()
    size_locals_list = len(LOCALS)
    while True:
        showing_cities(LOCALS)
        
        print()
        print("-"*40)
        
        option = input("->Escolha uma cidade (0 p/a encerrar): ")

        if option == '0':
            os.system("cls")
            break
        else:
            if verify_option(option, size_locals_list):
                os.system("cls")
                call_api(option, LOCALS)
                break


#main: Função responsável por ser o ponto de partida do programa
def main():
    while True:
        saudation()
        menu()

        option = input("->Digite sua opção: ")
        if option == "2":
            os.system("cls")
            break

        elif option == "1":
            os.system("cls")
            show_prevision()
        
        else:
            os.system("cls")

main()
