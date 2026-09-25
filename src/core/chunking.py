import pandas as pd

def criar_chunks(df_corpus):
    # Lista vazia que vai guardar todos os pedaços de texto
    lista_de_chunks = []
    
    # Passa por cada documento da base de dados
    for indice, linha in df_corpus.iterrows():
        texto_completo = linha['texto']
        doc_id = linha['doc_id']
        titulo = linha['titulo']
        status = linha['status']
        
        # Corta o texto toda vez que encontrar uma quebra de linha seguida de "## "
        # garante que só vai cortar em títulos de seção.
        partes = texto_completo.split('\n## ')
        
        # Transformando apenas indice 1 em diante em chunk já que o cabeçalho não vira
        secoes = partes[1:]
        
        # Analisa cada seção que foi cortada
        for secao in secoes:
            # Corta a seção na primeira quebra de linha 
            # Assim a primeira linha é o nome da seção e o resto é o texto.
            linhas = secao.split('\n', 1)
            
            nome_da_secao = linhas[0].strip() # Pega o nome e tira espaços extras
            
            texto_da_secao = ""
            # Se houver mais de uma linha, significa que tem texto nessa seção
            if len(linhas) > 1:
                texto_da_secao = linhas[1].strip()
            
            # Só guarda o chunk se realmente tiver texto dentro da seção
            if texto_da_secao:
                novo_chunk = {
                    'doc_id': doc_id,
                    'titulo': titulo,
                    'secao': nome_da_secao,
                    'status': status,
                    'texto': texto_da_secao
                }
                lista_de_chunks.append(novo_chunk)
                
    # Transforma a lista de dicionários em um DataFrame do Pandas e devolve
    return pd.DataFrame(lista_de_chunks)


def gerar_saida_p1(df_chunks, caminho_saida):
    total_chunks = len(df_chunks)
    
    # Conta quantos chunks cada documento gerou e transforma em dicionário
    contagem_por_doc = df_chunks['doc_id'].value_counts().to_dict()
    
    # Pega o primeiro chunk da lista para mostrar como exemplo na evidência
    exemplo = df_chunks.iloc[0]
    
    # Começamos a montar o texto que vai para o arquivo
    texto = "## P1\n"
    texto += "### Chunking por seção\n\n"
    texto += f"**Número total de chunks:** {total_chunks}\n\n"
    
    texto += "**Número de chunks por documento:**\n"
    for doc, qtd in contagem_por_doc.items():
        texto += f"- {doc}: {qtd} chunks\n"
        
    texto += "\n**Exemplo de Chunk Completo:**\n"
    texto += f"- **doc_id:** {exemplo['doc_id']}\n"
    texto += f"- **titulo:** {exemplo['titulo']}\n"
    texto += f"- **secao:** {exemplo['secao']}\n"
    texto += f"- **status:** {exemplo['status']}\n"
    texto += f"- **texto:** {exemplo['texto']}\n"
    texto += "\n---\n\n"
    
    #  Usa append para adicionar no fim do arquivo sem apagar a P0
    with open(caminho_saida, 'a', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(texto)
        
    print("\n--- Validação P1 ---")
    print(f"Total de chunks gerados: {total_chunks}")
    print("Evidência da Parte 1 adicionada ao arquivo saidas.md")