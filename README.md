# Teacher English: Assistente de IA para Gramática e Vocabulário
Um serviço RESTful em Flask que integra um Large Language Model (LLM) local (via LM Studio) para auxiliar no ensino e aprendizado de inglês, oferecendo avaliação gramatical, tradução de palavras com exemplos contextuais e verificação de status do serviço LLM.

## Funcionalidades
O Teacher English oferece os seguintes endpoints de API:
|METODO |FUNCIONALIDADE | DESCRIÇÃO |
|------|---------------|-----------|
|/api/grammar/evaluate |Avaliação Gramatical| Envie uma frase em inglês e receba uma análise gramatical detalhada, incluindo correções, erros identificados e um percentual de assertividade.|
|/api/translate/word |Tradução e Contexto de Palavras| Forneça uma palavra em inglês e obtenha sua tradução para o português, tipo gramatical e frases de exemplo com tradução para demonstrar seu uso contextual.|
|/api/llm/status |Status do LLM| Verifique a disponibilidade e o status operacional do Large Language Model subjacente, garantindo que o serviço de IA esteja ativo.|

## Arquitetura do Projeto
O projeto segue os princípios da Arquitetura Limpa (Clean Architecture), dividindo o código em camadas concêntricas para garantir modularidade, testabilidade e separação de preocupações:

* `core/`: Contém a lógica de negócio principal (casos de uso) e as definições de entidades, independente de frameworks ou LLMs específicos.
* `adapters/`: Define interfaces (contratos) para serviços externos (como LLMs), permitindo que a camada core interaja com eles sem conhecer suas implementações concretas.
* `infrastructure/`: Fornece as implementações concretas dos adaptadores, como o cliente para a API do LM Studio.
* `web/`: Contém os controladores da API Flask, responsáveis por receber requisições HTTP, chamar os casos de uso apropriados e retornar as respostas.
* `main.py`: O ponto de entrada da aplicação Flask.
