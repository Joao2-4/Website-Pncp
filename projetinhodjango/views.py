from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
from datetime import datetime, timedelta
import os
import time
from tqdm import tqdm
from django.http import HttpRequest
import random

file_name = ""
mensagem = ""

# python manage.py runserver - CODIGO PARA RODAR SERVER


def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%Y%m%d')

def pncp3(data_inicial, data_final, tamanho_pagina, cod_municipio_ibge, esfera):
    global file_name
    global mensagem
    url = 'https://pncp.gov.br/api/consulta/v1/contratos'
    headers = {'accept': '*/*'}
    todos_os_registros = []

    params = {
        'dataInicial': data_inicial,
        'dataFinal': data_final,
        'pagina': '1',
        'tamanhoPagina': tamanho_pagina,
        'codigoMunicipioIbge': cod_municipio_ibge
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        dados = response.json()
        total_paginas = dados['totalPaginas']
        print("Total de páginas:", total_paginas)
        todos_os_registros.extend(dados['data'])
    except requests.exceptions.RequestException as e:
        mensagem = (f"Erro ao fazer a requisição: {e}")
        print(mensagem)
        return {'error': str(e)}

    # Filtrar os registros pela esfera especificada
    registros_filtrados = [
        item for item in todos_os_registros
        if item['orgaoEntidade']['esferaId'] == esfera
    ]

    random_code = str(random.randint(1000, 9999))
    file_name = f"data_{data_inicial}_{data_final}_{random_code}.json"
    templates_dir = os.path.join(os.path.dirname(__file__), 'Arquivos_temp')
    file_path = os.path.join(templates_dir, file_name)


    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)

    # Salvar os registros filtrados em um arquivo JSON
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(registros_filtrados, f, ensure_ascii=False, indent=4)

    return registros_filtrados


def proposta_codigo(data_final_formatada, tamanho_pagina, modalidade, esfera):
    global file_name
    global mensagem

    url = 'https://pncp.gov.br/api/consulta/v1/contratacoes/proposta'
    headers = {'accept': '*/*'}
    todos_os_registros = []

    params = {
        'dataFinal': data_final_formatada,
        'pagina': '1',
        'tamanhoPagina': tamanho_pagina,
        'codigoModalidadeContratacao': modalidade
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        dados = response.json()
        print("Dados recebidos:", dados)
        total_paginas = dados['totalPaginas']
        print("Total de páginas:", total_paginas)
        todos_os_registros.extend(dados['data'])
    except requests.exceptions.RequestException as e:
        mensagem = (f"Erro ao fazer a requisição: {e}")
        print(mensagem)
        return {'error': str(e)}


    registros_filtrados = [
        item for item in todos_os_registros
        if item['orgaoEntidade']['esferaId'] == esfera
    ]
    
    random_code = str(random.randint(1000, 9999))
    file_name = f"data_{data_final_formatada}_{random_code}.json"
    templates_dir = os.path.join(os.path.dirname(__file__), 'Arquivos_Temp')
    file_path = os.path.join(templates_dir, file_name)

    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(registros_filtrados, f, ensure_ascii=False, indent=4)

    return registros_filtrados  

def pncp2(data_inicial, data_final, ModNovo, tamanho_pagina, cod_municipio_ibge, esfera):
    global file_name
    global mensagem
    url = 'https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao'
    headers = {'accept': '*/*'}
    todos_os_registros = []

    params = {
        'dataInicial': data_inicial,
        'dataFinal': data_final,
        'pagina': '1',
        'tamanhoPagina': tamanho_pagina,
        'codigoMunicipioIbge': cod_municipio_ibge,
        'codigoModalidadeContratacao': ModNovo
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        dados = response.json()
        print("Dados recebidos:", dados)
        total_paginas = dados['totalPaginas']
        print("Total de páginas:", total_paginas)
        todos_os_registros.extend(dados['data'])
    except requests.exceptions.RequestException as e:
        mensagem = (f"Erro ao fazer a requisição: {e}")
        print(mensagem)
        return {'error': str(e)}
    
    registros_filtrados = [
        item for item in todos_os_registros
        if item['orgaoEntidade']['esferaId'] == esfera
    ]

    random_code = str(random.randint(1000, 9999))
    file_name = f"data_{data_inicial}_{data_final}_{random_code}.json"
    templates_dir = os.path.join(os.path.dirname(__file__), 'Arquivos_temp')
    file_path = os.path.join(templates_dir, file_name)

    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(registros_filtrados, f, ensure_ascii=False, indent=4)

    return registros_filtrados

      

def consulta_view(request):
    if request.method == 'POST':
        data_inicial = request.POST.get('data-inicial')
        data_final = request.POST.get('data-final')
        tamanho_pagina = request.POST.get('tamanho-pagina')
        cod_municipio_ibge = request.POST.get('municipios')
        esfera = request.POST.get('esfera')

        # Formatar as datas para o formato YYYYMMDD
        data_inicial_formatada = format_date(data_inicial)
        data_final_formatada = format_date(data_final)

        resultado = pncp3(data_inicial_formatada, data_final_formatada, tamanho_pagina, cod_municipio_ibge, esfera)

    return render(request, 'projetinhodjango/contratos.html')

def proposta(request):
    if request.method == 'POST':
        data_final = request.POST.get('data-final')
        tamanho_pagina = request.POST.get('tamanho-pagina')
        modalidade = request.POST.get('modalidade')
        esfera = request.POST.get('esfera')


    
        data_final_formatada = format_date(data_final)
        resultado = proposta_codigo(data_final_formatada,tamanho_pagina,modalidade,esfera)
   
    return render(request, 'projetinhodjango/proposta.html')

def pub(request):
    if request.method == 'POST':
        data_inicial = request.POST.get('data-inicial')
        data_final = request.POST.get('data-final')
        codigo_modalidade = request.POST.get('modalidade')
        tamanho_pagina = request.POST.get('tamanho-pagina')
        cod_municipio_ibge = request.POST.get('municipios')
        esfera = request.POST.get('esfera')



        # Formatar as datas para o formato YYYYMMDD
        data_inicial_formatada = format_date(data_inicial)
        data_final_formatada = format_date(data_final)
        ModNovo = int(codigo_modalidade)


        resultado = pncp2(data_inicial_formatada, data_final_formatada, ModNovo, tamanho_pagina, cod_municipio_ibge, esfera)
        
    return render(request, 'projetinhodjango/pub.html')

def ultimo(request: HttpRequest):
    # Caminho para o arquivo JSON
    json_file_path = os.path.join('C:\\Users\\joaovvs\\Desktop\\Pdjango\\projetinhodjango\\Arquivos_temp', file_name)
    
    context = {}
    
    try:
        # Tenta ler o arquivo JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            context['data'] = json.dumps(data, indent=4)
    except FileNotFoundError:
        # Se o arquivo não for encontrado, define a mensagem de erro
        context['mensagem'] = mensagem

    return render(request, 'projetinhodjango/arquivo_final.html', context)


