# src/core/entities.py

from typing import List, Optional
from pydantic import BaseModel, Field

class AvaliacaoGramatical(BaseModel):
    """Entidade para a avaliação gramatical de uma frase."""
    frase_original: str = Field(..., description="A frase em inglês original submetida.")
    frase_corrigida: str = Field(..., description="A frase com correções gramaticais sugeridas.")
    erros_encontrados: List[str] = Field(default_factory=list, description="Lista de erros gramaticais específicos encontrados.")
    percentual_assertividade: float = Field(..., ge=0, le=100, description="Percentual de assertividade gramatical (0-100%).")
    comentarios: str = Field(..., description="Comentários adicionais sobre a gramática.")

class Traducao(BaseModel):
    """Entidade para a tradução de uma palavra com exemplos de aplicação."""
    palavra_original: str = Field(..., description="A palavra em inglês original.")
    traducao_pt: str = Field(..., description="A tradução da palavra para o português.")
    sugestoes_frases: List[str] = Field(default_factory=list, description="Lista de frases de exemplo com a palavra em contexto.")
    tipo_gramatical: Optional[str] = Field(None, description="Tipo gramatical da palavra (ex: substantivo, verbo).")

class LLMStatus(BaseModel):
    """Entidade para o status do serviço LLM."""
    status: str = Field(..., description="Status do LLM (ativo, inativo, erro).")
    mensagem: str = Field(..., description="Mensagem descritiva sobre o status.")
    modelo_carregado: Optional[str] = Field(None, description="Nome do modelo LLM carregado, se aplicável.")
    tempo_resposta_ms: Optional[float] = Field(None, description="Tempo de resposta do LLM em milissegundos.")