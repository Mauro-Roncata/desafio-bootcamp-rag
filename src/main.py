import os
import pandas as pd
from core.data_loader import carregar_corpus, validar_status, gerar_saida_p0
from core.chunking import criar_chunks, gerar_saida_p1
from core.indexing import criar_indice_tfidf, gerar_saida_p2
from core.search import buscar, gerar_saida_p3

def main():
    # Configura os caminhos das pastas
    # Pega a pasta atual e volta uma pasta para achar a raiz do projeto
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_raiz = os.path.dirname(pasta_atual)
    
    # Monta os caminhos exatos dos arquivos
    caminho_csv = os.path.join(pasta_raiz, "metadados.csv")
    pasta_corpus = os.path.join(pasta_raiz, "corpus")
    caminho_saidas = os.path.join(pasta_raiz, "saidas.md")
    caminho_csv_perguntas = os.path.join(pasta_raiz, "perguntas_gabarito.csv")
    
    print("Iniciando a Parte 0: Setup e leitura do corpus...\n")
    # Executando as funções
    df = carregar_corpus(caminho_csv, pasta_corpus)
    validar_status(df)
    gerar_saida_p0(df, caminho_saidas)

    print("\nIniciando a Parte 1: Chunking por seção...")
    df_chunks = criar_chunks(df)
    gerar_saida_p1(df_chunks, caminho_saidas)

    print("\nIniciando a Parte 2: Indexação com TF-IDF...")
    # Passando os chunks gerados na P1 para o indexador
    vetorizador, matriz_tfidf = criar_indice_tfidf(df_chunks)
    gerar_saida_p2(matriz_tfidf, caminho_saidas)

    print("\nIniciando a Parte 3: Recuperação top-k com regra de vigência...")
    # Le as perguntas do gabarito
    df_perguntas = pd.read_csv(caminho_csv_perguntas, encoding='utf-8')
    # Executa as buscas de teste e gera a evidência
    gerar_saida_p3(df_perguntas, df_chunks, vetorizador, matriz_tfidf, caminho_saidas)



# Isso garante que o código só rode se executar este arquivo diretamente
if __name__ == "__main__":
    main()