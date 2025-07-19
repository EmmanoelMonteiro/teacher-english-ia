# Teacher English: Assistente de IA para Gramática e Vocabulário

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/flask-3.1.*+-red?style=for-the-badge&logo=flask&logoColor=white"  alt="Flask Version">
  <img src="https://img.shields.io/badge/LM_Studio-Compatible-informational?style=for-the-badge&logo=ai" alt="LM Studio Compatible">
</p>

Um serviço RESTful em Flask que integra um Large Language Model (LLM) local (via LM Studio) para auxiliar no ensino e aprendizado de inglês. Ele oferece avaliação gramatical, tradução de palavras com exemplos contextuais e a verificação do status do serviço LLM.

---

## 🎯 Objetivo do Projeto

O `Teacher English` visa **simplificar e agilizar o processo de avaliação de gramática e a consulta de vocabulário para estudantes e professores de inglês**. Ao integrar um LLM local, o projeto oferece uma solução autônoma e eficiente para feedback gramatical instantâneo e enriquecimento de vocabulário com exemplos práticos, tornando o aprendizado e o ensino mais interativos e acessíveis.

---

## ✨ Funcionalidades

O `Teacher English` expõe os seguintes endpoints de API:

* **Avaliação Gramatical (`/api/grammar/evaluate`):**
    * Envie uma frase em inglês via POST.
    * Receba uma análise gramatical detalhada, incluindo correções, erros identificados e um percentual de assertividade.
* **Tradução e Contexto de Palavras (`/api/translate/word`):**
    * Forneça uma palavra em inglês via POST.
    * Obtenha sua tradução para o português, tipo gramatical e frases de exemplo com tradução para demonstrar seu uso contextual.
* **Status do LLM (`/api/llm/status`):**
    * Verifique a disponibilidade e o status operacional do Large Language Model subjacente via GET.
    * Garanta que o serviço de IA esteja ativo e operante.

---

## 🚀 Como Rodar

Siga os passos abaixo para configurar e executar o `Teacher English` em sua máquina.

### Pré-requisitos

Certifique-se de ter o seguinte instalado:

* **Python 3.9+:** Essencial para rodar a aplicação Flask.
* **LM Studio:** Software para baixar e rodar LLMs localmente. Baixe em [lmstudio.ai](https://lmstudio.ai/).
* **Um modelo LLM compatível:** Por exemplo, `bartowski/llama-3.2-1b-instruct` ou `phi-3-mini-4k-instruct-GGUF`. Você pode baixá-los diretamente pelo LM Studio.

### 1. Configuração do Ambiente

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/EmmanoelMonteiro/teacher-english-ia.git
    cd teacher_english
    ```

2.  **Crie e Ative o Ambiente Virtual:**
    ```bash
    python -m venv .venv
    # No Windows (PowerShell):
    .venv\Scripts\Activate.ps1
    # No Windows (CMD):
    .venv\Scripts\activate.bat
    # No macOS / Linux:
    source .venv/bin/activate
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install Flask python-dotenv pydantic openai
    ```
    Ou, se você já gerou um `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Crie o Arquivo de Variáveis de Ambiente (`.env`):**
    Na raiz do projeto (`teacher_english/`), crie um arquivo chamado `.env` com o seguinte conteúdo. **Ajuste o `LLM_MODEL_NAME` para o nome exato do modelo que você carregou no seu LM Studio.**

    ```dotenv
    # .env
    # Variáveis de Ambiente para a aplicação teacher_english

    # --- Configurações do LLM ---
    # URL base do servidor de inferência do LM Studio.
    # Geralmente é localhost na porta 1234.
    LLM_BASE_URL=http://localhost:1234/v1

    # Chave de API para o LM Studio. Para uso local, qualquer string serve.
    LLM_API_KEY=lm-studio_api_key_local

    # Nome do modelo LLM carregado no LM Studio.
    # AJUSTE ESTE VALOR para o nome EXATO do modelo que você carregou.
    # Ex: gemma-2-2b-it, lmstudio-community/bartowski/llama-3.2-1b-instruct, etc.
    # Você pode encontrar este nome na aba 'Local Inference Server' do LM Studio.
    LLM_MODEL_NAME=bartowski/llama-3.2-1b-instruct 
    ```

5.  **Crie os Arquivos `__init__.py`:**
    Certifique-se de que os arquivos `__init__.py` (que podem ser vazios) existam em cada subdiretório do `src/` para que o Python reconheça a estrutura como um pacote. A estrutura deve ser a seguinte:

    ```
    teacher_english/
    ├── .venv/
    ├── src/
    │   ├── __init__.py         <-- Adicione aqui
    │   ├── core/
    │   │   ├── __init__.py     <-- Adicione aqui
    │   │   ├── entities.py
    │   │   └── use_cases.py
    │   ├── adapters/
    │   │   ├── __init__.py     <-- Adicione aqui
    │   │   └── llm_adapter.py
    │   ├── infrastructure/
    │   │   ├── __init__.py     <-- Adicione aqui
    │   │   └── llm_api_client.py
    │   ├── web/
    │   │   ├── __init__.py     <-- Adicione aqui
    │   │   └── controllers.py
    │   └── main.py
    ├── .env
    ├── requirements.txt
    └── README.md
    ```
    Você pode criar esses arquivos vazios usando `touch __init__.py` (Linux/macOS) ou `type nul > __init__.py` (Windows CMD) em cada diretório correspondente.

### 2. Configuração do LLM no LM Studio

1.  **Abra o LM Studio.**
2.  **Baixe o Modelo Desejado:** Na aba "Search", procure e baixe um modelo compatível (ex: `bartowski/llama-3.2-1b-instruct`). Salve-o em um **SSD** para melhor desempenho.
3.  **Carregue o Modelo:** Na aba "My Models", selecione o modelo baixado para carregá-lo na memória.
4.  **Inicie o Servidor de Inferência Local:** Vá para a aba "Local Inference Server" e clique em "Start Server". Verifique se o servidor está rodando na porta `1234` (ou ajuste a variável `LLM_BASE_URL` no seu `.env` se for diferente).

### 3. Inicie a Aplicação Flask

Com seu ambiente virtual ativado e o LM Studio rodando o servidor de inferência local, execute a aplicação Flask a partir da **raiz do projeto**:

```bash
(.venv) python -m src.main
```

A aplicação estará acessível em `http://127.0.0.1:5000/`

## 💻 Endpoints da API

Todos os endpoints estão prefixados com `/api.`

1. Avaliar Gramática
* **Endpoint:** `POST /api/grammar/evaluate`
* **Descrição:** Avalia a gramática de uma frase em inglês e fornece feedback.
* **Corpo da Requisição (JSON):**

```JSON

{
    "phrase": "I has a new car and very happy."
}
```
* **Exemplo de Resposta (JSON):**

```JSON

{
    "comentarios": "A frase foi corrigida para garantir concordância verbal e uso correto do adjetivo. 'Has' foi corrigido para 'have' e 'very happy' para 'very happy'.",
    "erros_encontrados": [
        "Concordância verbal (has -> have)",
        "Uso incorreto de advérbio/adjetivo (very happy -> very happy)"
    ],
    "frase_corrigida": "I have a new car and I am very happy.",
    "frase_original": "I has a new car and very happy.",
    "percentual_assertividade": 75.0
}
```

2. Traduzir Palavra e Sugerir Contexto
* **Endpoint:** `POST /api/translate/word`
* **Descrição:** Traduz uma palavra do inglês para o português, indica seu tipo gramatical e oferece frases de exemplo com contexto.
* **Corpo da Requisição (JSON):**
```JSON
{
    "word": "apple"
}
```
* **Exemplo de Resposta (JSON):**
```JSON

{
    "palavra_original": "apple",
    "sugestoes_frases": [
        "She loves to eat an apple every morning. (Ela adora comer uma maçã todas as manhãs.)",
        "The new store sells only the best apples. (A nova loja vende apenas as melhores maçãs.)",
        "An apple a day keeps the doctor away. (Uma maçã por dia mantém o médico afastado.)"
    ],
    "tipo_gramatical": "substantivo",
    "traducao_pt": "maçã"
}
```

3. Status do LLM
* **Endpoint:** `GET /api/llm/status`
* **Descrição:** Verifica o status operacional do LLM no LM Studio.
* **Exemplo de Resposta (JSON - Ativo):**
```JSON

{
    "mensagem": "LLM está ativo e respondendo.",
    "modelo_carregado": "gemma-2-2b-it",
    "status": "ativo",
    "tempo_resposta_ms": 65.21
}
```
* **Exemplo de Resposta (JSON - Inativo):**
```JSON

{
    "mensagem": "Não foi possível conectar ao servidor do LLM. Detalhes: [Detalhes do erro de conexão]",
    "modelo_carregado": null,
    "status": "inativo",
    "tempo_resposta_ms": null
}
```
