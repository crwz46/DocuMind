from documind.config import Config
from documind.llm import LLMEngine


class TestLLMEngine:
    def test_demo_mode_with_context(self):
        engine = LLMEngine(provider="demo")
        answer = engine.ask("What is DocuMind?", context="DocuMind is a RAG engine")
        assert "Demo Mode" in answer

    def test_demo_mode_without_context(self):
        engine = LLMEngine(provider="demo")
        answer = engine.ask("What is DocuMind?")
        assert "no relevant documents" in answer.lower()

    def test_invalid_provider(self):
        engine = LLMEngine(provider="invalid")
        answer = engine.ask("Hello")
        assert "Error" in answer

    def test_demo_provider_from_config(self):
        Config.LLM_PROVIDER = "demo"
        engine = LLMEngine()
        assert engine.provider == "demo"

    def test_build_messages_with_context(self):
        messages = LLMEngine._build_messages("Test question", "Some context")
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["content"] == "Context:\nSome context\n\nQuestion: Test question"

    def test_build_messages_without_context(self):
        messages = LLMEngine._build_messages("Test question")
        assert len(messages) == 2
        assert messages[1]["content"] == "Test question"
