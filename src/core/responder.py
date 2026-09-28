import pandas as pd
from core.search import buscar

# threshold escolhido com base na observação da P3.
THRESHOLD_ESCOLHIDO = 0.30

def responder(pergunta, df_chunks, vetorizador, matriz_tfidf):
  
    # Usa a função buscar da P3 para pegar o melhor resultado (k=1)
    resultados = buscar(pergunta, df_chunks, vetorizador, matriz_tfidf, k=1)
    
    # Se a busca não retornar nada (lista vazia por algum erro), trata como não encontrado
    if not resultados:
        return montar_saida_acessivel(pergunta, None, 0.0)
        
    melhor_resultado = resultados[0]
    score = melhor_resultado['score']
    
    # Verifica se o score atingiu a nota de corte (threshold)
    if score >= THRESHOLD_ESCOLHIDO:
        return montar_saida_acessivel(pergunta, melhor_resultado, score)
    else:
        return montar_saida_acessivel(pergunta, None, score)

def montar_saida_acessivel(pergunta, chunk, score):
 
    texto_saida = f"PERGUNTA: {pergunta}\n"
    
    if chunk is not None:
        texto_saida += f"RESPOSTA: {chunk['texto']}\n"
        texto_saida += f"FONTE: {chunk['doc_id']} | {chunk['titulo']} | Seção: {chunk['secao']}\n"
        texto_saida += f"SCORE: {score:.2f}\n"
        texto_saida += "STATUS: encontrado\n"
    else:
        texto_saida += "RESPOSTA: Não encontrei essa informação nas políticas vigentes. Procure a área de Pessoas e Cultura.\n"
        texto_saida += "FONTE: nenhuma\n"
        texto_saida += f"SCORE: {score:.2f}\n"
        texto_saida += "STATUS: nao_encontrado\n"
        
    return texto_saida

def gerar_saida_p4(df_perguntas, df_chunks, vetorizador, matriz_tfidf, caminho_saida):

    texto = "## P4\n"
    texto += "### Resposta extrativa e regra de não encontrado\n\n"
    
    # Justificativa exigida
    texto += f"**Threshold escolhido:** {THRESHOLD_ESCOLHIDO}\n"
    texto += "**Justificativa:** Ao analisar os resultados da P3, observei que perguntas válidas retornaram scores acima de 0.40, enquanto a pergunta P10 (sem resposta no corpus) teve o seu maior score em 0.21. Escolhi 0.30 como ponto de corte seguro para evitar falsos positivos sem prejudicar respostas corretas.\n\n"
    
    # saídas completas da P02 e P10
    perguntas_teste = ['P02', 'P10']
    
    for p_id in perguntas_teste:
        linha = df_perguntas[df_perguntas['pergunta_id'] == p_id].iloc[0]
        texto_pergunta = linha['pergunta']
        
        # Gera a resposta formatada
        resposta_formatada = responder(texto_pergunta, df_chunks, vetorizador, matriz_tfidf)
        
        texto += f"**Teste com {p_id}:**\n"
        texto += "```text\n"
        texto += resposta_formatada
        texto += "```\n\n"
        
    texto += "---\n\n"
    
    with open(caminho_saida, 'a', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(texto)
        
    print("\n--- Validação P4 ---")
    print(f"Threshold de {THRESHOLD_ESCOLHIDO} aplicado com sucesso.")
    print("Respostas extrativas geradas e formatadas.")
    print("Evidência da Parte 4 adicionada ao ficheiro saidas.md")