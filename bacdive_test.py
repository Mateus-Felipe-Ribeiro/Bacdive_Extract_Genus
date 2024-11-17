import pandas as pd
import bacdive
client = bacdive.BacdiveClient('login', 'senha')

def extrair_dados_bacterianos(resposta_api):
    # Inicializa um dicionário para armazenar os dados extraídos
    dados_extraidos = {}

    # Extrai dados gerais
    general = resposta_api.get("General", {})
    dados_extraidos["BacDive_ID"] = general.get("BacDive-ID")
    dados_extraidos["Descricao"] = general.get("description")
    dados_extraidos["DOI_bacdive"] = general.get("doi")
    dados_extraidos["Palavras_chave"] = general.get("keywords", [])
    ncbi_id_obj = general.get("NCBI tax id", {})
    dados_extraidos["NCBI_id"] = ncbi_id_obj.get("NCBI tax id")
    dados_extraidos["NCBI_match_lvl"] = ncbi_id_obj.get("Matching level")

    # Extrai classificação taxonômica
    taxonomia = resposta_api.get("Name and taxonomic classification", {})
    dados_extraidos["Dominio"] = taxonomia.get("domain")
    dados_extraidos["Filo"] = taxonomia.get("phylum")
    dados_extraidos["Classe"] = taxonomia.get("class")
    dados_extraidos["Ordem"] = taxonomia.get("order")
    dados_extraidos["Familia"] = taxonomia.get("family")
    dados_extraidos["Genero"] = taxonomia.get("genus")
    dados_extraidos["Especie"] = taxonomia.get("species")
    dados_extraidos["Designacao_cep"] = taxonomia.get("strain designation")
    dados_extraidos["Cep_tipo"] = taxonomia.get("type strain")

    # Extrai morfologia celular e colônica
    morfologia = resposta_api.get("Morphology", {})
    
    # Verifica e extrai os dados da morfologia celular
    morfologia_celular = morfologia.get("cell morphology", [])
    dados_extraidos["Morfologia_Celular"] = []
    if isinstance(morfologia_celular, dict):  # Caso único
        dados_extraidos["Morfologia_Celular"].append({
            "Corante_Gram": morfologia_celular.get("gram stain"),
            "Comprimento": morfologia_celular.get("cell length"),
            "Largura": morfologia_celular.get("cell width"),
            "Forma": morfologia_celular.get("cell shape"),
            "Motilidade": morfologia_celular.get("motility"),
            "Arranjo_Flagelo": morfologia_celular.get("flagellum arrangement")
        })
    elif isinstance(morfologia_celular, list):  # Caso lista de dicionários
        for celula in morfologia_celular:
            dados_celula = {
                "Corante_Gram": celula.get("gram stain"),
                "Comprimento": celula.get("cell length"),
                "Largura": celula.get("cell width"),
                "Forma": celula.get("cell shape"),
                "Motilidade": celula.get("motility"),
                "Arranjo_Flagelo": celula.get("flagellum arrangement")
            }
            dados_extraidos["Morfologia_Celular"].append(dados_celula)

    # Verifica e extrai os dados da morfologia colônica
    morfologia_colonia = morfologia.get("colony morphology", [])
    dados_extraidos["Morfologia_Colonia"] = []
    if isinstance(morfologia_colonia, dict):  # Caso único
        dados_extraidos["Morfologia_Colonia"].append({
            "Tamanho": morfologia_colonia.get("colony size"),
            "Cor": morfologia_colonia.get("colony color"),
            "Forma": morfologia_colonia.get("colony shape"),
            "Periodo_Incubacao": morfologia_colonia.get("incubation period"),
            "Meio_Usado": morfologia_colonia.get("medium used")
        })
    elif isinstance(morfologia_colonia, list):  # Caso lista de dicionários
        for colonia in morfologia_colonia:
            dados_colonia = {
                "Tamanho": colonia.get("colony size"),
                "Cor": colonia.get("colony color"),
                "Forma": colonia.get("colony shape"),
                "Periodo_Incubacao": colonia.get("incubation period"),
                "Meio_Usado": colonia.get("medium used")
            }
            dados_extraidos["Morfologia_Colonia"].append(dados_colonia)    # Extrai condições de cultura e crescimento

    # cultura = resposta_api.get("Culture and growth conditions", {})
    # meio_cultura = cultura.get("culture medium")
    # if isinstance(meio_cultura, dict):  # Caso único
    #     dados_extraidos["Meio_de_Cultura"] = meio_cultura.get("name")
    # elif isinstance(meio_cultura, list):  # Caso lista
    #     dados_extraidos["Meio_de_Cultura"] = [m.get("name") for m in meio_cultura if isinstance(m, dict)]
    # dados_extraidos["Temperaturas_Cultura"] = cultura.get("culture temp", [])
    # dados_extraidos["PH_Cultura"] = cultura.get("culture pH", [])

    # Extrai dados de fisiologia e metabolismo
    fisiologia = resposta_api.get("Physiology and metabolism", {})

    Tolerancia_Oxigenio_obj = fisiologia.get("oxygen tolerance", [])
    dados_extraidos["Tolerancia_Oxigenio"] = []
    if isinstance(Tolerancia_Oxigenio_obj, dict):
        dados_extraidos["Tolerancia_Oxigenio"].append({"oxygen_tolerance": Tolerancia_Oxigenio_obj.get("oxygen tolerance")})
    elif isinstance(Tolerancia_Oxigenio_obj, list):
        for tolerancia in Tolerancia_Oxigenio_obj:
            dados_tolerancia = {
                "oxygen_tolerance": tolerancia.get("oxygen tolerance")
            }
            dados_extraidos["Tolerancia_Oxigenio"].append(dados_tolerancia)
    
    Tipo_Nutricao_obj = fisiologia.get("nutrition type", {})
    dados_extraidos["Tipo_Nutricao"] = []
    if isinstance(Tipo_Nutricao_obj, dict):
        dados_extraidos["Tipo_Nutricao"].append({"type": Tipo_Nutricao_obj.get("type")})
    elif isinstance(Tipo_Nutricao_obj, list):
        for nutricao in Tipo_Nutricao_obj:
            dados_nutricao = {
                "type": nutricao.get("type")
            }
            dados_extraidos["Tipo_Nutricao"].append(dados_nutricao)
    # dados_extraidos["Tipo_Nutricao"] = Tipo_Nutricao_obj.get("type")
    # dados_extraidos["Halofilia"] = fisiologia.get("halophily", []) # é uma lista de porcentagem de concentrações
    # exemplo:
    # "halophily":[
    #      {
    #         "@ref":65231,
    #         "salt":"NaCl",
    #         "growth":"positive",
    #         "tested relation":"growth",
    #         "concentration":"0-1.5 %"
    #      },
    #      {
    #         "@ref":65231,
    #         "salt":"NaCl",
    #         "growth":"no",
    #         "tested relation":"growth",
    #         "concentration":">2 %"
    #      }
    #   ],
    # dados_extraidos["Utilizacao_Metabolitos"] = fisiologia.get("metabolite utilization", []) # é uma lista de enzimas
    # "metabolite utilization":[
    #      {
    #         "@ref":65231,
    #         "Chebi-ID":30089,
    #         "metabolite":"acetate",
    #         "utilization activity":"+",
    #         "kind of utilization tested":"carbon source"
    #      },
    #      {
    #         "@ref":65231,
    #         "Chebi-ID":29016,
    #         "metabolite":"arginine",
    #         "utilization activity":"-",
    #         "kind of utilization tested":"carbon source"
    #      }
    # ],

    # External links - "literature"
    links_externos = resposta_api.get("External links", {})
    literatura = links_externos.get("literature", {})
    dados_extraidos["DOI_article"] = []
    if isinstance(literatura, dict):
        dados_extraidos["DOI_article"].append({"DOI_article": literatura.get("DOI")})
    elif isinstance(literatura, list):
        for lit in literatura:
            dados_lit = {
                "DOI_article": lit.get("DOI")
            }
            dados_extraidos["DOI_article"].append(dados_lit)

    return dados_extraidos

# Função para limpar o dado
def extrair_nome_genus(dados):
    # Verifica se o valor de "Nome" e "Genus" é uma string
    if isinstance(dados['Nome'], str):
        dados['Nome'] = dados['Nome'].split(';')[0]  # Primeiro elemento para 'Nome'
    
    if isinstance(dados['Genus'], str):
        dados['Genus'] = dados['Genus'].split(';')[-2]  # Penúltimo elemento para 'Genus'
    
    return dados

def verificar_genus_existente(resultado_final, genus):
    """
    Verifica se o gênero já foi processado na lista resultado_final.
    Retorna True se o gênero já existir, caso contrário, False.
    """
    return any(item['genus'] == genus for item in resultado_final)

# Ler arquivo planilha e extrair nomes
# Vamos ler a planilha Excel e extrair as colunas 'A' e 'G' (que equivalem a índices 0 e 6 em Python)
arquivo_excel = 'C:/Users/Mateus Ribeiro/Documents/Mestrado/base mestrado/Proj1/tab_tax_bacs_ex1.csv'  # Substitua pelo caminho do seu arquivo
df = pd.read_csv(arquivo_excel)       # Leitura da planilha
df_filtrado = df.iloc[:, [0, -1]]        # Seleciona a primeira coluna (A) e a penúltima (G)
df_filtrado.columns = ['Nome', 'Genus'] # Renomeia as colunas para facilitar a leitura

# Converte o DataFrame em uma lista de dicionários para facilitar o processamento
dados = df_filtrado.to_dict('records')

# Pesquisa por gênero
resultado_final = []  # Lista para armazenar os resultados finais com os atributos desejados

# Aplica a função para corrigir os valores de 'Nome' e 'Genus' em cada dicionário individualmente
dados_corrigidos = [extrair_nome_genus(item) for item in dados]
#print(dados_corrigidos)

for item in dados_corrigidos:
    genus = item['Genus']
    nome = item['Nome']

    # Verifica se o gênero é diferente de 'unclassified'
    if genus != 'Unclassified' and genus != 'Candidatus Udaeobacter' and genus != '':
        # client = []
        print(genus)

        # Verifica se o gênero já foi processado
        if verificar_genus_existente(resultado_final, genus):
            continue  # Pula para o próximo item, pois o gênero já foi processado
        else:
            result = client.search(taxonomy=genus)  # Realiza a pesquisa usando o gênero

            # Recupera os resultados da API
            if result:
                for strain in client.retrieve():
                    # print(strain)
                    dados_processados = extrair_dados_bacterianos(strain)
                    # print(dados_processados)

                    # Verifica se há dados de morfologia celular e colônia
                    if len(dados_processados["Morfologia_Celular"]) > 0:
                        for itens in dados_processados["Morfologia_Celular"]:
                            morfologia_celular = itens
                            if morfologia_celular.get("Comprimento", '') != '':
                                break
                    else: 
                        morfologia_celular = {}

                    if len(dados_processados["Morfologia_Colonia"]) > 0:
                        for itens in dados_processados["Morfologia_Colonia"]:
                            morfologia_colonia = itens
                            if morfologia_colonia.get("Tamanho", '') != '':
                                break
                    else: 
                        morfologia_colonia = {}

                    # verifica tolerancia oxigenio
                    if len(dados_processados["Tolerancia_Oxigenio"]) > 0:
                        for itens in dados_processados["Tolerancia_Oxigenio"]:
                            toleracia_oxigenio = itens
                            if toleracia_oxigenio.get("oxygen_tolerance", '') != '':
                                break
                    else: 
                        toleracia_oxigenio = {}
                    
                    # verifica doi
                    if len(dados_processados["DOI_article"]) > 0:
                        for itens in dados_processados["DOI_article"]:
                            DOI_article = itens
                            if DOI_article.get("DOI_article", '') != '':
                                break
                    else: 
                        DOI_article = {}

                    # verifica nutrição
                    if len(dados_processados["Tipo_Nutricao"]) > 0:
                        for itens in dados_processados["Tipo_Nutricao"]:
                            Tipo_Nutricao = itens
                            if Tipo_Nutricao.get("type", '') != '':
                                break
                    else: 
                        Tipo_Nutricao = {}

                    resultado = {
                        'asv': nome,
                        'genus': genus,
                        'cell_morphology_length': morfologia_celular.get("Comprimento", '') if morfologia_celular else '',
                        'cell_morphology_width': morfologia_celular.get("Largura", '') if morfologia_celular else '',
                        'colony_size': morfologia_colonia.get("Tamanho", '') if morfologia_colonia else '',
                        'BacDive_ID': dados_processados["BacDive_ID"],
                        'class': dados_processados["Classe"],
                        'order': dados_processados["Ordem"],
                        'family': dados_processados["Familia"],
                        'specie': dados_processados["Especie"],
                        'oxygen_tolerance': toleracia_oxigenio.get("oxygen_tolerance", '') if toleracia_oxigenio else '',
                        'nutrition_type': Tipo_Nutricao.get("type", '') if Tipo_Nutricao else '',
                        'article_DOI': DOI_article.get("DOI_article", '') if DOI_article else '',
                        'NCBI_id': dados_processados["NCBI_id"],
                        'NCBI_match_lvl': dados_processados["NCBI_match_lvl"],
                        'bacdive_DOI': dados_processados["DOI_bacdive"],
                    }

                    resultado_final.append(resultado)

# Exibe o resultado final
#print(resultado_final)

# Salvar o resultado final em um novo arquivo Excel
df_resultado = pd.DataFrame(resultado_final)
df_resultado.to_csv('C:/Users/Mateus Ribeiro/Documents/Mestrado/base mestrado/Proj1/resultado_morfologia_taxonomia_filtrado.csv', index=False)
