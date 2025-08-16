### Import de Libs
import requests
import os
import zipfile
import io
import pandas as pd

### Definição das Instituições Financeiras que serão monitoradas
bancos = [
    {"nome": "Bradesco", "cnpj": "60746948"},
    {"nome": "Banco do Brasil", "cnpj": "00000000"},  # substituir pelo CNPJ correto se necessário
    {"nome": "Itaú Unibanco", "cnpj": "60701190"},
    {"nome": "Santander Brasil", "cnpj": "90400888"},
    {"nome": "Caixa Econômica Federal", "cnpj": "00360320"},
    {"nome": "Banco Safra", "cnpj": "75614311"},
    {"nome": "Banco BTG Pactual", "cnpj": "33476024"},
    {"nome": "Banco Mercantil do Brasil", "cnpj": "60700874"}
]

bancos = pd.DataFrame(bancos)

cnpjs = list(bancos.cnpj.unique())

### Definição do Período do Monitoramento
# Período de Extração
ano_inicio = 2023
ano_fim = 2025  

anos_meses = []

for ano in range(ano_inicio, ano_fim + 1):
    for mes in range(1, 13):
        ano_mes = f"{ano}{mes:02d}"  # formata mês MM
        anos_meses.append(ano_mes)

for cnpj in cnpjs:
    for ano_mes in anos_meses:
        # Local para salvar os arquivos
        path_arq_raw = 'Projeto_CADOC_4010_4016\\Arquivos_Raw'
        path_arq_processados = 'Projeto_CADOC_4010_4016\\Arquivos_Processados'

        # Endpoint para listar arquivos disponíveis
        url_lista = f'https://www3.bcb.gov.br/informes/rest/balanco//arquivosCosif?anoMes={ano_mes}&cnpj={cnpj}&periodo=1'

        # Obtendo lista de arquivos
        resp = requests.get(url_lista)
        resp.raise_for_status()
        arquivos = resp.json()

        if not arquivos:
            print(f"⚠ Nenhum arquivo disponível para CNPJ {cnpj} no período {ano_mes}")
            continue  # pula para o próximo ano_mes

        arquivos_extraidos = []  # Lista auxiliar para armazenar os arquivos do zip

        # 1. Baixar e extrair os .zip em memória
        for item in arquivos:
            nome_zip = item['nomeArquivo']
            url_download = f'https://www3.bcb.gov.br/informes/rest/balanco//download/{nome_zip}?cnpj={cnpj}&anoMes={ano_mes}'
            
            print(f'Baixando {nome_zip} ...')
            r = requests.get(url_download)
            r.raise_for_status()
            
            # Abrindo o zip em memória
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                for nome_interno in z.namelist():
                    with z.open(nome_interno) as f:
                        conteudo = f.read()
                        arquivos_extraidos.append({
                            'zip_origem': nome_zip,
                            'nome': nome_interno,
                            'conteudo': conteudo
                        })

        print('✅ Todos os arquivos foram extraídos para a memória.')

        # 2. Salvando os arquivos raw em disco
        for arq in arquivos_extraidos:
            caminho = os.path.join(path_arq_raw, arq["nome"])
            with open(caminho, "wb") as f:
                f.write(arq["conteudo"])
            print(f'✔ Arquivo salvo em: {caminho}')

        # 3. Salvando os arquivos processados em disco
        for arq in arquivos_extraidos:
            nome = arq['nome']
            conteudo = arq['conteudo']
            
            try:
                # Convertendo bytes para string usando encoding latin1
                texto = conteudo.decode('latin1')
                
                # Retirando o cabeçalho
                linhas = texto.splitlines()
                for i, linha in enumerate(linhas):
                    if linha.startswith("#DATA_BASE"):
                        inicio = i
                        break
                
                # Lendo CSV a partir da linha correta
                df = pd.read_csv(io.StringIO("\n".join(linhas[inicio:])), sep=';')
                print(f"✔ Arquivo {nome} Salvo. Shape: {df.shape}")
                caminho = os.path.join(path_arq_processados, nome)
                df.to_csv(caminho, index = False)
                
            except Exception as e:

                print(f"⚠ Não foi possível processar o arquivo {nome}: {e}")
