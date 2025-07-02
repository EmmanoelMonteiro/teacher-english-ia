# src/web/controllers.py

from flask import request, jsonify, Blueprint
import json # Importar aqui para o jsonify

from core.use_cases import AvaliarGramaticaUseCase, TraduzirPalavraUseCase, LLMStatusUseCase
from infrastructure.llm_api_client import LMStudioLLMClient
from core.entities import AvaliacaoGramatical, Traducao, LLMStatus # Importar as entidades

# Injeção de dependências - instancie os adaptadores e casos de uso aqui
llm_client = LMStudioLLMClient()
avaliar_gramatica_use_case = AvaliarGramaticaUseCase(llm_client)
traduzir_palavra_use_case = TraduzirPalavraUseCase(llm_client)
llm_status_use_case = LLMStatusUseCase(llm_client)

api_bp = Blueprint('api', __name__)

@api_bp.route('/grammar/evaluate', methods=['POST'])
def evaluate_grammar():
    """
    Endpoint para avaliar a gramática de uma frase em inglês.
    Espera JSON: {"phrase": "your English phrase here"}
    """
    data = request.get_json()
    if not data or 'phrase' not in data:
        return jsonify({"error": "Missing 'phrase' in request body."}), 400

    phrase = data['phrase']
    try:
        # Chama o caso de uso
        avaliacao: AvaliacaoGramatical = avaliar_gramatica_use_case.execute(phrase)
        return avaliacao, 200 # Usa .dict() para serializar Pydantic
    except ConnectionError as e:
        return jsonify({"error": str(e), "status_llm": "inativo"}), 503
    except ValueError as e:
        return jsonify({"error": f"Erro de processamento: {e}"}), 400
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado: {e}"}), 500

@api_bp.route('/translate/word', methods=['POST'])
def translate_word():
    """
    Endpoint para traduzir uma palavra e obter exemplos de frases.
    Espera JSON: {"word": "your English word here"}
    """
    data = request.get_json()
    if not data or 'word' not in data:
        return jsonify({"error": "Missing 'word' in request body."}), 400

    word = data['word']
    try:
        # Chama o caso de uso
        traducao = traduzir_palavra_use_case.execute(word)
        # return jsonify(traducao.dict()), 200
        return traducao, 200
    except ConnectionError as e:
        return jsonify({"error": str(e), "status_llm": "inativo"}), 503
    except ValueError as e:
        return jsonify({"error": f"Erro de processamento: {e}"}), 400
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado: {e}"}), 500

@api_bp.route('/llm/status', methods=['GET'])
def get_llm_status():
    """
    Endpoint para verificar o status do serviço LLM.
    """
    try:
        # Chama o caso de uso
        status: LLMStatus = llm_status_use_case.execute()
        return jsonify(status.dict()), 200
    except Exception as e:
        # Embora o use case já trate erros, é bom ter um fallback aqui
        return jsonify({"status": "erro", "mensagem": f"Erro ao obter status do LLM: {e}"}), 500