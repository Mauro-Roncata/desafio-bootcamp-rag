import pandas as pd
from core.search import buscar
from core.responder import responder

def avaliar_assistente(df_perguntas, df_chunks, vetorizador, matriz_tfidf, caminho_saida):
    resultados_tabela = []
    acertos_hit1 = 0
    acertos_hit3 = 0
    total_validas = 0
    p10_status_correto = False

    # Passa por todas as 10 perguntas do gabarito
    for _, linha in df_perguntas.iterrows():
        p_id = linha['pergunta_id']
        pergunta = linha['pergunta']
        doc_esperado = linha['doc_esperado']

        # Executa a busca para pegar o Top-3
        resultados_busca = buscar(pergunta, df_chunks, vetorizador, matriz_tfidf, k=3)
        
        # Executa o responder para pegar o status real do assistente
        texto_resposta = responder(pergunta, df_chunks, vetorizador, matriz_tfidf)
        status = "encontrado" if "STATUS: encontrado" in texto_resposta else "nao_encontrado"

        # Pega as informações do primeiro resultado (se houver)
        if resultados_busca:
            doc_retornado_1 = resultados_busca[0]['doc_id']
            score = resultados_busca[0]['score']
        else:
            doc_retornado_1 = "nenhum"
            score = 0.0

        # Avaliação de Acertos
        acerto = "Não"
        if doc_esperado != "nao_encontrado":
            total_validas += 1 # Conta apenas as 9 perguntas com resposta
            docs_retornados = [r['doc_id'] for r in resultados_busca]
            
            # Hit@1: O primeiro resultado é o documento esperado?
            if doc_retornado_1 == doc_esperado:
                acertos_hit1 += 1
                acerto = "Sim"
                
            # Hit@3: O documento esperado está entre os 3 primeiros?
            if doc_esperado in docs_retornados:
                acertos_hit3 += 1
                if acerto == "Não": # Se não acertou no top 1, mas estava no top 3
                    acerto = "Parcial (Hit@3)"
        else:
            # Tratamento especial para P10
            if status == "nao_encontrado":
                p10_status_correto = True
                acerto = "Sim (Correto ao barrar)"

        # Guarda os dados para a tabela final
        resultados_tabela.append({
            'pergunta_id': p_id,
            'doc_esperado': doc_esperado,
            'doc_retornado_1': doc_retornado_1,
            'score': f"{score:.2f}",
            'STATUS': status,
            'acerto': acerto
        })

    # Calcula as médias
    hit1_media = acertos_hit1 / total_validas if total_validas > 0 else 0
    hit3_media = acertos_hit3 / total_validas if total_validas > 0 else 0

    # Formata a saída em Markdown
    texto = "## P5\n"
    texto += "### Avaliação com o gabarito\n\n"
    
    # Montagem manual da tabela
    cabecalho = "| pergunta_id | doc_esperado | doc_retornado_1 | score | STATUS | acerto |\n|---|---|---|---|---|---|\n"
    linhas_md = ""
    for row in resultados_tabela:
        linhas_md += f"| {row['pergunta_id']} | {row['doc_esperado']} | {row['doc_retornado_1']} | {row['score']} | {row['STATUS']} | {row['acerto']} |\n"
    
    texto += cabecalho + linhas_md + "\n"
    
    texto += f"**Métricas (calculadas sobre as 9 perguntas válidas):**\n"
    texto += f"- **Hit@1:** {hit1_media:.2f} ({acertos_hit1}/{total_validas})\n"
    texto += f"- **Hit@3:** {hit3_media:.2f} ({acertos_hit3}/{total_validas})\n\n"
    
    p10_resultado = "ACERTOU" if p10_status_correto else "ERROU"
    texto += f"**Verificação P10:** O STATUS devolvido foi nao_encontrado? **{p10_resultado}**\n\n"
    
    # Análise de erro/proximidade técnica
    texto += "**Análise de erro ou proximidade:**\n"
    texto += "Alguns scores ficam perigosamente perto do threshold porque o algoritmo TF-IDF exige correspondência exata de palavras. Se o usuário utilizar sinônimos que não constam nas políticas, o score despenca. Para corrigir esse comportamento e melhorar o Hit@1, eu aplicaria a técnica de Lemmatization no pré-processamento ou substituiria o modelo TF-IDF por Embeddings densos, que conseguem compreender a similaridade semântica entre palavras diferentes.\n\n"
    texto += "---\n\n"

    # Salva no arquivo
    with open(caminho_saida, 'a', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(texto)

    print("\n--- Validação P5 ---")
    print(f"Avaliação concluída com sucesso! Hit@1: {hit1_media:.2f} | Hit@3: {hit3_media:.2f}")
    print("Evidência da Parte 5 adicionada ao arquivo saidas.md")