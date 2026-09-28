from sklearn.feature_extraction.text import TfidfVectorizer

def criar_indice_tfidf(df_chunks):
    # Lista de stopwords em português e termos das perguntas que não agregam valor para a busca
    stopwords_pt = [
        'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'do', 'da', 'dos', 'das', 
        'em', 'no', 'na', 'nos', 'nas', 'para', 'com', 'por', 'qual', 'quais', 
        'quantos', 'quantas', 'posso', 'como', 'onde', 'quando', 'que', 'e', 'é', 'sao', 'ou'
    ]
    
    # Configura o "tradutor" de texto TF-IDF
    vetorizador = TfidfVectorizer(
        lowercase=True, 
        strip_accents='unicode',
        stop_words=stopwords_pt
    )
    
    # Transforma a coluna 'texto' dos chunks em uma matriz matemática
    matriz_tfidf = vetorizador.fit_transform(df_chunks['texto'])
    
    return vetorizador, matriz_tfidf

def gerar_saida_p2(matriz_tfidf, caminho_saida):
    # .shape devolve duas informações: número de linhas (chunks) e colunas (palavras únicas)
    linhas = matriz_tfidf.shape[0]
    colunas = matriz_tfidf.shape[1]
    
    # Frase explicando a decisão
    frase_decisao = (
        "Optei remover acentos (strip_accents='unicode') "
        "e excluir uma lista customizada de stopwords em português (incluindo termos como "
        "'qual', 'posso', 'quantos') para reduzir o ruído e focar nas palavras com maior "
        "peso, evitando falsos positivos na recuperação."
    )
    
    texto = "## P2\n"
    texto += "### Indexação com TF-IDF\n\n"
    texto += f"**Forma da matriz:** {linhas} linhas por {colunas} colunas.\n\n"
    texto += f"**Decisão de pré-processamento:** {frase_decisao}\n\n"
    texto += "---\n\n"
    
    # Usa append para adicionar no fim do arquivo sem apagar P0 e P1
    with open(caminho_saida, 'a', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(texto)
        
    print("\n--- Validação P2 ---")
    print(f"Matriz criada: {linhas} chunks x {colunas} palavras no vocabulário.")
    print("Evidência da Parte 2 adicionada ao arquivo saidas.md")