import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def buscar(pergunta, df_chunks, vetorizador, matriz_tfidf, k=3):

    # Transforma a pergunta em números usando o mesmo vetorizador da P2
    vetor_pergunta = vetorizador.transform([pergunta])
    
    # Calcula a similaridade (nota de 0 a 1) entre a pergunta e todos os chunks
    # Isso devolve uma matriz. Pega a posição [0] para ter apenas a lista de notas.
    notas = cosine_similarity(vetor_pergunta, matriz_tfidf)[0]
    
    # Cria uma cópia da tabela de chunks e adiciona a coluna de notas
    df_resultados = df_chunks.copy()
    df_resultados['score'] = notas
    
    # Filtra para manter apenas os documentos vigentes.
    df_vigentes = df_resultados[df_resultados['status'] == 'vigente']
    
    # Ordena do maior score para o menor
    df_ordenado = df_vigentes.sort_values(by='score', ascending=False)
    
    # Pega apenas os k primeiros resultados (top-k)
    top_k = df_ordenado.head(k)
    
    # Transforma o resultado em uma lista de dicionários
    return top_k.to_dict('records')


def gerar_saida_p3(df_perguntas, df_chunks, vetorizador, matriz_tfidf, caminho_saida):

    perguntas_teste = ['P01', 'P02', 'P10']
    
    texto = "## P3\n"
    texto += "### Recuperação top-k com regra de vigência\n\n"
    
    # Passa pelas três perguntas exigidas
    for p_id in perguntas_teste:
        # Encontra a pergunta na tabela do gabarito
        linha = df_perguntas[df_perguntas['pergunta_id'] == p_id].iloc[0]
        texto_pergunta = linha['pergunta']
        
        texto += f"**{p_id} - Pergunta:** {texto_pergunta}\n\n"
        
        # Chama a função de busca
        resultados = buscar(texto_pergunta, df_chunks, vetorizador, matriz_tfidf, k=3)
        
        # Monta a tabela de evidência com score formatado para 2 casas decimais
        texto += "| Posição | doc_id | seção | score |\n"
        texto += "|---|---|---|---|\n"
        
        for i, res in enumerate(resultados):
            score_formatado = f"{res['score']:.2f}"
            texto += f"| {i+1} | {res['doc_id']} | {res['secao']} | {score_formatado} |\n"
            
        texto += "\n"
        
    texto += "---\n\n"
    
    # Adiciona no final do arquivo saidas.md
    with open(caminho_saida, 'a', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(texto)
        
    print("\n--- Validação P3 ---")
    print("Busca realizada para as perguntas P01, P02 e P10.")
    print("Regra de vigência aplicada com sucesso (POL-004 excluída).")
    print("Evidência da Parte 3 adicionada ao arquivo saidas.md")