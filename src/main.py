import os
from core.data_loader import carregar_corpus, validar_status, gerar_saida_p0
from core.chunking import criar_chunks, gerar_saida_p1

def main():
    # Configura os caminhos das pastas
    # Pega a pasta atual e volta uma pasta para achar a raiz do projeto
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_raiz = os.path.dirname(pasta_atual)
    
    # Monta os caminhos exatos dos arquivos
    caminho_csv = os.path.join(pasta_raiz, "metadados.csv")
    pasta_corpus = os.path.join(pasta_raiz, "corpus")
    caminho_saidas = os.path.join(pasta_raiz, "saidas.md")
    
    print("Iniciando a Parte 0: Setup e leitura do corpus...\n")
    # Executando as funções
    df = carregar_corpus(caminho_csv, pasta_corpus)
    validar_status(df)
    gerar_saida_p0(df, caminho_saidas)

    print("\nIniciando a Parte 1: Chunking por seção...")
    df_chunks = criar_chunks(df)
    gerar_saida_p1(df_chunks, caminho_saidas)



# Isso garante que o código só rode se executar este arquivo diretamente
if __name__ == "__main__":
    main()