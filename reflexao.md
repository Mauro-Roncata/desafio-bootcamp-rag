## Reflexão - Assistente de Políticas Internas

**1. A importância de citar a FONTE e os riscos reais:**
Citar a fonte é o principal mecanismo de confiança do sistema. Em uma empresa real, se o assistente fornecer uma informação incorreta sobre benefícios ou regras de trabalho sem citar a origem, o colaborador pode tomar decisões baseadas em alucinações da IA. Isso geraria problemas internos até passivos trabalhistas. A fonte permite o usuáro validar a regra e que a área de Pessoas e Cultura identifique e remova os documentos obsoletos.

**2. A decisão mais difícil: O Threshold (Limiar):**
A decisão mais complexa foi definir o threshold exato de 0.30. Um valor muito alto (ex: 0.50) causaria falsos negativos, atrapalhando o usuário ao afirmar que regras existentes não foram encontradas. Um valor muito baixo causaria respostas incorretas, forçando o pareamento de perguntas sem resposta no corpus. A decisão foi tomada de forma empírica ao isolar a pergunta P10 (estacionamento), cujo score máximo foi 0.21. Utilizei esse teto como limite inferior, garantindo o corte seguro de ruídos sem prejudicar as perguntas válidas.

**3. Mudanças e novos riscos com o uso de um LLM:**
Com um modelo local na Parte 4, o sistema deixaria de fornecer uma cópia bruta (extrativa) do chunk. O LLM receberia os trechos recuperados no prompt e sintetizaria uma resposta em formato conversacional. O novo risco introduzido seria a alucinação generativa: o LLM poderia misturar a regra vigente com conhecimentos externos (pré-treino) ou flexibilizar o tom das políticas (ex: afirmar que o home office é "negociável" quando a regra é estrita).