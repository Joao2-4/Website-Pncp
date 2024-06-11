from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
from datetime import datetime, timedelta
import os
import time
from tqdm import tqdm
from django.http import HttpRequest



# python manage.py runserver - CODIGO PARA RODAR SERVER


def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%Y%m%d')

def pncp3(data_inicial, data_final, tamanho_pagina, cod_municipio_ibge, esfera):
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
        # Printar a query para depuração
        print("Query parameters:", params)

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        dados = response.json()
        todos_os_registros.extend(dados['data'])
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

    # Filtrar os registros pela esfera especificada
    registros_filtrados = [
        item for item in todos_os_registros
        if item['orgaoEntidade']['esferaId'] == esfera
    ]

    templates_dir = os.path.join(os.path.dirname(__file__), 'templates/projetinhodjango')
    file_path = os.path.join(templates_dir, 'data.json')

    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)

    # Salvar os registros filtrados em um arquivo JSON
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(registros_filtrados, f, ensure_ascii=False, indent=4)

    return registros_filtrados


def proposta_codigo(data_final_formatada, tamanho_pagina, modalidade, esfera):
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
        print(dados)
        total_paginas = dados['totalPaginas']
        print(total_paginas)
        todos_os_registros.extend(dados['data'])
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

    registros_filtrados = [
        item for item in todos_os_registros
        if item['orgaoEntidade']['esferaId'] == esfera
    ]

    templates_dir = os.path.join(os.path.dirname(__file__), 'templates/projetinhodjango')
    file_path = os.path.join(templates_dir, 'data.json')

    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(registros_filtrados, f, ensure_ascii=False, indent=4)

    return registros_filtrados


def pncp2(data_inicial, data_final, ModNovo, tamanho_pagina, cod_municipio_ibge, esfera):
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
        total_paginas = dados['totalPaginas']
        print(total_paginas)
        print("Dados recebidos:", dados)  # Debug: verificar os dados recebidos
        todos_os_registros.extend(dados.get('data', []))
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
    
    registros_filtrados = [
        item for item in todos_os_registros
        if item['orgaoEntidade']['esferaId'] == esfera
    ]

    templates_dir = os.path.join(os.path.dirname(__file__), 'templates\projetinhodjango')
    file_path = os.path.join(templates_dir, 'data.json')

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
    json_file_path = 'C:\\Users\\joaovvs\\Desktop\\Pdjango\\projetinhodjango\\templates\\projetinhodjango\\data.json'
    
    # Lê o arquivo JSON de forma segura usando 'with'
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Passa os dados para o template, já formatados em JSON
    context = {'data': json.dumps(data, indent=4)}
    return render(request, 'projetinhodjango/arquivo_final.html', context)
