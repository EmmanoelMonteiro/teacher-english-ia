# src/core/use_cases.py

import re
import json
from core.entities import AvaliacaoGramatical, Traducao, LLMStatus
from adapters.llm_adapter import LLMAdapter

class AvaliarGramaticaUseCase:
    def __init__(self, llm_adapter: LLMAdapter):
        self.llm = llm_adapter

    def execute(self, frase_ingles: str) -> AvaliacaoGramatical:
        prompt = f"""
        Você é um avaliador de gramática para frases em inglês.
        Analise a frase: "{frase_ingles}" e forneça:
        1. A frase original.
        2. A frase corrigida (se houver erros).
        3. Uma lista dos erros gramaticais específicos encontrados (ex: "erro de concordância verbal", "uso incorreto de preposição"). Se não houver erros, a lista deve ser vazia.
        4. O percentual de assertividade gramatical (100% se não houver erros).

        Exemplo de formato JSON **COMPLETO E VÁLIDO**:
        ```json
        {{
            "frase_original": "...",
            "frase_corrigida": "...",
            "erros_encontrados": [],
            "percentual_assertividade": float
        }}
        ```
        """

        try:
            # Pedimos para o LLM gerar um JSON diretamente
            llm_response_text = self.llm.generate_completion(
                messages=[
                    {"role": "system", "content": "Você é um expert em gramática inglesa e fornece feedback preciso no formato JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2, # Mais determinístico para gramática
                max_tokens=800
            )

            # Tenta analisar a resposta como JSON
            ## data = json.loads(llm_response_text)
            json_match = llm_response_text.replace("```json","")
            json_match = json_match.replace("```","")

            data = json.loads(json_match)

            print("Aqui 03 ##################")
            print(data)
            print("--------------------------")
            
            # Valida e retorna a entidade
            return data

        except Exception as e:
            # Fallback se o LLM não retornar JSON ou falhar
            print(f"Erro ao processar JSON do LLM, tentando fallback textual: {e}")
            fallback_prompt = f"""
            Você é um avaliador de gramática para frases em inglês.
            Analise a frase: "{frase_ingles}" e forneça:
            - A frase corrigida (se houver).
            - Uma breve descrição dos erros.
            - Um percentual de assertividade.

            Exemplo:
            Original: I has a cat.
            Corrigida: I have a cat.
            Erros: Erro de concordância verbal (has -> have).
            Assertividade: 70%
            """
            fallback_response = self.llm.generate_completion(
                messages=[
                    {"role": "system", "content": "Você é um expert em gramática inglesa e fornece feedback preciso."},
                    {"role": "user", "content": fallback_prompt}
                ],
                temperature=0.5,
                max_tokens=600
            )
            
             # Tentar extrair informações do texto (pode ser impreciso)
            
            corrigida_match = re.search(r"Corrigida:\s*(.*)", fallback_response)
            erros_match = re.search(r"Erros:\s*(.*)", fallback_response)
            assertividade_match = re.search(r"Assertividade:\s*(\d+\.?\d*)%", fallback_response)

            frase_corrigida = corrigida_match.group(1).strip() if corrigida_match else frase_ingles
            erros_encontrados = [e.strip() for e in erros_match.group(1).split(',')] if erros_match else []
            percentual_assertividade = float(assertividade_match.group(1)) if assertividade_match else 0.0
            comentarios = fallback_response

            return AvaliacaoGramatical(
                frase_original=frase_ingles,
                frase_corrigida=frase_corrigida,
                erros_encontrados=erros_encontrados,
                percentual_assertividade=percentual_assertividade,
                comentarios=comentarios
            )
            

class TraduzirPalavraUseCase:
    def __init__(self, llm_adapter: LLMAdapter):
        self.llm = llm_adapter

    def execute(self, palavra_ingles: str) -> Traducao:
        prompt = f"""
        Você é um tradutor especialista. Traduza a palavra em inglês "{palavra_ingles}" para o português.
        Forneça também o tipo gramatical da palavra.
        Em seguida, liste três frases de exemplo em inglês onde a palavra é usada em contexto.

        Sua resposta **DEVE** ser formatada como um objeto JSON válido, cercado por ```json e ```.
        O JSON **DEVE** conter as seguintes chaves:
        - "palavra_original": A palavra em inglês original.
        - "traducao_pt": A tradução para o português.
        - "tipo_gramatical": O tipo gramatical da palavra (ex: "substantivo", "verbo", "adjetivo").
        - "sugestoes_frases": Uma lista de strings, onde cada string é uma frase de exemplo em inglês, seguida da sua tradução para o português entre parênteses.

        Exemplo de formato JSON **COMPLETO E VÁLIDO**:
        ```json
        {{
            "palavra_original": "house",
            "traducao_pt": "casa",
            "tipo_gramatical": "substantivo",
            "sugestoes_frases": [
                "I live in a big house. (Eu moro em uma casa grande.)",
                "They are building a new house. (Eles estão construindo uma casa nova.)",
                "My dream house has a garden. (Minha casa dos sonhos tem um jardim.)"
            ]
        }}
        ```

        Agora, forneça a tradução e os detalhes para a palavra: "{palavra_ingles}"
        """
        try:
            print("AQUI 01  #####################")
            llm_response_text = self.llm.generate_completion(
                messages=[
                    {"role": "system", "content": "Você é um tradutor especialista e fornece traduções e exemplos no formato JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7, # Um pouco mais criativo para exemplos
                max_tokens=800
            )
            
            # json_match = re.search(r"```json\s*(\{.*\})\s*```", llm_response_text, re.DOTALL)

            json_match = llm_response_text.replace("```json","")
            json_match = json_match.replace("```","")
            
            dados = json.loads(json_match)
            print("Aqui 03 ##################")
            print(dados)
            print("--------------------------")
            return dados

        except Exception as e:
            print(f"Erro ao processar JSON do LLM para tradução, tentando fallback textual: {e}")
            fallback_prompt = f"""
            Traduza a palavra em inglês "{palavra_ingles}" para o português.
            Diga se é um substantivo, verbo, etc.
            Dê três exemplos de frases com essa palavra em inglês e a tradução de cada frase.

            Exemplo:
            Palavra: cat
            Tradução: gato (substantivo)
            Frases:
            - The cat is sleeping. (O gato está dormindo.)
            - She has a black cat. (Ela tem um gato preto.)
            - My cat loves to play. (Meu gato adora brincar.)
            """
            fallback_response = self.llm.generate_completion(
                messages=[
                    {"role": "system", "content": "Você é um tradutor especialista e fornece traduções e exemplos."},
                    {"role": "user", "content": fallback_prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            # Tentar extrair informações do texto (pode ser impreciso)
            traducao_match = re.search(r"Tradução:\s*(.*?)\s*\((\w+)\)", fallback_response)
            frases_match = re.findall(r"-\s*(.*?)\s*\((.*?)\)", fallback_response)

            traducao_pt = traducao_match.group(1).strip() if traducao_match else "Não disponível"
            tipo_gramatical = traducao_match.group(2).strip() if traducao_match else None
            sugestoes_frases = [f"{ing.strip()} ({pt.strip()})" for ing, pt in frases_match] if frases_match else [fallback_response]

            return Traducao(
                palavra_original=palavra_ingles,
                traducao_pt=traducao_pt,
                tipo_gramatical=tipo_gramatical,
                sugestoes_frases=sugestoes_frases
            )

class LLMStatusUseCase:
    def __init__(self, llm_adapter: LLMAdapter):
        self.llm = llm_adapter

    def execute(self) -> LLMStatus:
        status_data = self.llm.get_llm_status()
        return LLMStatus(**status_data)