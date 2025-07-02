# src/infrastructure/llm_api_client.py

import os
import time
from openai import OpenAI, APIConnectionError, OpenAIError
from dotenv import load_dotenv
from typing import Dict, Any

from adapters.llm_adapter import LLMAdapter

load_dotenv() # Carrega as variáveis do .env

class LMStudioLLMClient(LLMAdapter):
    """
    Implementação concreta do LLMAdapter para interagir com o LM Studio
    (compatível com a API da OpenAI).
    """
    def __init__(self):
        self.base_url = os.getenv("LLM_BASE_URL", "http://localhost:1234/v1")
        self.api_key = os.getenv("LLM_API_KEY", "lm-studio")
        self.model_name = os.getenv("LLM_MODEL_NAME", "bartowski/llama-3.2-1b-instruct") # Nome do modelo no LM Studio

        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)

    def generate_completion(self, messages: list[Dict[str, str]], **kwargs) -> str:
        """
        Gera uma conclusão de texto usando o LLM no LM Studio.
        """
        try:
            print("generate_completion #### "+ self.model_name)
            # Inclui o modelo nos kwargs, permitindo que seja sobrescrito se necessário
            # mas usando o padrão definido no .env
            model_to_use = kwargs.pop('model', self.model_name)
            print("Model: "+ model_to_use)
            print("Mensagem: ")
            print(messages)            
            print("kwargs: ")
            print(kwargs)
            completion = self.client.chat.completions.create(
                model=model_to_use,
                messages=messages,
                **kwargs
            )
            print("AQUI 02 #####################")
            print(completion.choices[0].message.content)
            print("-----------------------------")
            return completion.choices[0].message.content
        except APIConnectionError as e:
            raise ConnectionError(f"Não foi possível conectar ao servidor do LLM: {e}. Verifique se o LM Studio está rodando.") from e
        except OpenAIError as e:
            raise ValueError(f"Erro na API do LLM: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Erro inesperado ao gerar conclusão do LLM: {e}") from e

    def get_llm_status(self) -> Dict[str, Any]:
        """
        Verifica o status do LLM tentando fazer uma requisição simples.
        """
        start_time = time.time()
        try:
            # Tenta uma requisição de modelo simples (como listar modelos, se suportado)
            # ou uma pequena inferência.
            # O LM Studio não tem um endpoint /models robusto como o da OpenAI,
            # então uma pequena inferência é uma forma mais confiável de testar.
            test_response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "olá"}],
                max_tokens=5,
                temperature=0.0
            )
            end_time = time.time()
            response_time_ms = (end_time - start_time) * 1000

            return {
                "status": "ativo",
                "mensagem": "LLM está ativo e respondendo.",
                "modelo_carregado": self.model_name,
                "tempo_resposta_ms": round(response_time_ms, 2)
            }
        except APIConnectionError as e:
            return {
                "status": "inativo",
                "mensagem": f"Não foi possível conectar ao servidor do LLM. Detalhes: {e}",
                "modelo_carregado": None,
                "tempo_resposta_ms": None
            }
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": f"Erro ao verificar o status do LLM. Detalhes: {e}",
                "modelo_carregado": None,
                "tempo_resposta_ms": None
            }