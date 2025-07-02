# src/adapters/llm_adapter.py

from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMAdapter(ABC):
    """
    Interface abstrata para o adaptador do LLM.
    Define o contrato para qualquer implementação de LLM.
    """

    @abstractmethod
    def generate_completion(self, messages: list[Dict[str, str]], **kwargs) -> str:
        """Gera uma conclusão de texto com base nas mensagens fornecidas."""
        pass

    @abstractmethod
    def get_llm_status(self) -> Dict[str, Any]:
        """Obtém o status operacional do LLM."""
        pass