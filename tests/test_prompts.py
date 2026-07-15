"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

# Define o caminho absoluto para o arquivo que será testado (v2)
PROMPT_V2_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Carrega os dados do YAML antes de cada teste."""
        assert PROMPT_V2_PATH.exists(), f"O arquivo {PROMPT_V2_PATH} ainda não foi criado."
        
        yaml_content = load_prompts(PROMPT_V2_PATH)
        assert "bug_to_user_story_v2" in yaml_content, "A chave raiz 'bug_to_user_story_v2' está ausente no YAML."
        
        self.prompt_data = yaml_content["bug_to_user_story_v2"]
        # Extrai o system_prompt todo em minúsculo para facilitar a busca de palavras-chave
        self.system_prompt = self.prompt_data.get("system_prompt", "").lower()

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in self.prompt_data, "Campo 'system_prompt' não encontrado."
        assert self.prompt_data["system_prompt"].strip() != "", "O 'system_prompt' está vazio."

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        role_keywords = ["você é", "atue como", "aja como", "product manager"]
        has_role = any(keyword in self.system_prompt for keyword in role_keywords)
        assert has_role, "Nenhuma definição clara de persona encontrada no system_prompt."

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        format_keywords = ["markdown", "user story", "formato", "critérios de aceite"]
        has_format = any(keyword in self.system_prompt for keyword in format_keywords)
        assert has_format, "O prompt não exige um formato específico de saída (ex: Markdown)."

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        few_shot_keywords = ["exemplo", "entrada", "saída", "input", "output"]
        # Exige que pelo menos 2 palavras de few-shot existam no texto
        matches = sum(1 for keyword in few_shot_keywords if keyword in self.system_prompt)
        assert matches >= 2, "Exemplos de few-shot claros (entrada/saída) não encontrados."

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        full_text = str(self.prompt_data).lower()
        assert "[todo]" not in full_text and "todo:" not in full_text, "Atenção: Existem marcações 'TODO' esquecidas no YAML."

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        assert "metadata" in self.prompt_data, "Campo 'metadata' não encontrado."
        metadata = self.prompt_data["metadata"]
        assert "techniques" in metadata, "Lista de 'techniques' não encontrada nos metadados."
        
        techniques = metadata["techniques"]
        assert isinstance(techniques, list) and len(techniques) >= 2, "É obrigatório listar pelo menos 2 técnicas (ex: ['Few-shot', 'Chain of Thought'])."

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])