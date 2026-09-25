import pandas as pd
import os

def carregar_corpus(caminho_metadados, pasta_corpus):

    # Lê os metadados usando pandas
    df = pd.read_csv(caminho_metadados, encoding='utf-8')
    
    # Listas vazias para guardar os textos e a quantidade de palavras
    textos = []
    num_palavras = []
    
    # Passa por cada linha do dataframe
    for indice, linha in df.iterrows():
        
        # Pega o nome do arquivo que está na coluna 'arquivo' do CSV
        nome_arquivo = linha['arquivo']
        
        # Junta o caminho da pasta com o nome do arquivo (ex: corpus/POL-001_onboarding.md)
        caminho_arquivo = os.path.join(pasta_corpus, nome_arquivo)
        
        # Abre e lê o arquivo de texto
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            texto = arquivo.read()
            
            # Guarda o texto na lista "texto"
            textos.append(texto)
            
            # Conta as palavras e guarda na lista
            quantidade = len(texto.split())
            num_palavras.append(quantidade)
            
    # Cria duas novas colunas no nosso dataframe com as informações que coletamos
    df['texto'] = textos
    df['num_palavras'] = num_palavras
    
    return df


def validar_status(df):
    # Conta quantos documentos existem de cada status na coluna 'status'
    contagem = df['status'].value_counts()
    
    # Pega o valor exato de 'vigente' e 'revogado'
    vigentes = contagem.get('vigente', 0)
    revogados = contagem.get('revogada', 0)
    
    print("\n--- Validação P0 ---")
    print(f"Documentos vigentes: {vigentes} (Esperado: 11)")
    print(f"Documentos revogados: {revogados} (Esperado: 1)")


def gerar_saida_p0(df, caminho_saida):
   # Filtra apenas as colunas para a evidência
    df_tabela = df[['doc_id', 'status', 'num_palavras']]
    
    # Constrói a tabela Markdown
    cabecalho = "| doc_id | status | num_palavras |\n|---|---|---|\n"
    linhas = ""
    for _, linha in df_tabela.iterrows():
        linhas += f"| {linha['doc_id']} | {linha['status']} | {linha['num_palavras']} |\n"
    
    tabela_markdown = cabecalho + linhas
    
    # Monta o texto que vai ser escrito no arquivo final
    texto_evidencia = "## P0\n"
    texto_evidencia += "### Setup e leitura do corpus\n\n"
    texto_evidencia += "**Evidência da Parte 0:** Tabela com doc_id, status e número de palavras de cada documento.\n\n"
    texto_evidencia += tabela_markdown + "\n---\n\n"
    
    # Abre o arquivo saidas.md no modo de escrita ('w') e salva o texto
    with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(texto_evidencia)
        
    print(f"\nEvidência criada com sucesso no arquivo: saidas.md")