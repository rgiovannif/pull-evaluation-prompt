"""
Script para fazer push de prompts otimizados para o LangSmith Prompt Hub.
"""
import os
import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import check_env_vars, print_section_header

load_dotenv()

def push_prompts_to_langsmith():
    """Lê o prompt v2 do YAML e faz o push para o LangSmith Hub."""
    file_path = "prompts/bug_to_user_story_v2.yml"
    
    print("⏳ Carregando arquivo YAML local...")
    with open(file_path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)
        
    prompt_data = yaml_data["bug_to_user_story_v2"]
    system_prompt = prompt_data["system_prompt"]
    user_prompt = prompt_data["user_prompt"]
    
    # Converte os textos do YAML para um objeto oficial de Prompt do LangChain
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt)
    ])
    
    # Recupera o seu usuário configurado no .env
    #username = os.getenv("USERNAME_LANGSMITH_HUB")
    repo_name = "bug_to_user_story_v2"
    
    print(f"🚀 Fazendo push do prompt para o Hub: {repo_name}")
    
    # Envia para o LangSmith
    hub.push(repo_name, prompt_template)
    
    print("✅ Push realizado com sucesso!")

def main():
    """Função principal"""
    print_section_header("Iniciando Fase 4: Push de Prompts")
    
    # Valida as chaves e variáveis necessárias
    check_env_vars(["LANGSMITH_API_KEY"])
    
    # Garante que o arquivo v2 existe antes de tentar enviar
    if not Path("prompts/bug_to_user_story_v2.yml").exists():
        print("❌ Erro: O arquivo bug_to_user_story_v2.yml não foi encontrado.")
        return 1
        
    try:
        push_prompts_to_langsmith()
        return 0
    except Exception as e:
        print(f"\n❌ Falha na execução: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())