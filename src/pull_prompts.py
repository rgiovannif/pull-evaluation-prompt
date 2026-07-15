"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """Faz o pull do prompt ruim do LangSmith e salva localmente."""
    prompt_name = "leonanluppi/bug_to_user_story_v1"
    file_path = "prompts/bug_to_user_story_v1.yml"
    
    print(f"⏳ Buscando o prompt '{prompt_name}' no LangSmith Hub...")
    
    try:
        # Faz o pull do objeto do prompt diretamente da nuvem
        prompt_obj = hub.pull(prompt_name)
        
        # Serialização nativa: converte o objeto complexo do LangChain para um dicionário
        prompt_data = prompt_obj.dict()
        
        # Salva utilizando a função utilitária do boilerplate
        save_yaml(prompt_data, file_path)
        
        print(f"✅ Prompt salvo com sucesso em: {file_path}")
    except Exception as e:
        print(f"❌ Erro ao puxar ou salvar o prompt: {e}")
        raise


def main():
    """Função principal"""
    print_section_header("Iniciando Fase 1: Pull de Prompts")
    
    # Valida se a chave da API do LangSmith está configurada
    check_env_vars(["LANGSMITH_API_KEY"])
    
    # Garante que a pasta 'prompts/' exista na raiz do projeto antes de tentar salvar
    Path("prompts").mkdir(parents=True, exist_ok=True)
    
    try:
        pull_prompts_from_langsmith()
        return 0
    except Exception as e:
        print(f"\nFalha na execução: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
