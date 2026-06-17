from typing import Optional

from documind.config import Config


class LLMEngine:
    def __init__(self, provider: str = None):
        self.provider = (provider or Config.LLM_PROVIDER).lower()

    def ask(self, prompt: str, context: str = None, json_mode: bool = False) -> str:
        provider_map = {
            "openai": self._ask_openai,
            "ollama": self._ask_ollama,
            "demo": self._ask_demo,
        }
        handler = provider_map.get(self.provider)
        if not handler:
            return f"[Error] Unknown LLM provider: {self.provider}"
        return handler(prompt, context, json_mode=json_mode)

    def _ask_openai(self, prompt: str, context: str = None, json_mode: bool = False) -> str:
        import openai
        client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        messages = self._build_messages(prompt, context)
        kwargs = dict(
            model=Config.OPENAI_MODEL,
            messages=messages,
            temperature=0.3,
            max_tokens=2048,
        )
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        try:
            resp = client.chat.completions.create(**kwargs)
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"[OpenAI Error] {e}"

    def _ask_ollama(self, prompt: str, context: str = None, json_mode: bool = False) -> str:
        import httpx
        messages = self._build_messages(prompt, context)
        payload = dict(
            model=Config.OLLAMA_MODEL,
            messages=messages,
            stream=False,
            options={"temperature": 0.3},
        )
        if json_mode:
            payload["format"] = "json"
        try:
            resp = httpx.post(
                f"{Config.OLLAMA_BASE_URL}/api/chat",
                json=payload,
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("message", {}).get("content", "").strip()
        except Exception as e:
            return f"[Ollama Error] {e}"

    def _ask_demo(self, prompt: str, context: str = None, json_mode: bool = False) -> str:
        if json_mode:
            return self._ask_demo_json(prompt, context)
        if not context:
            return (
                "[Demo Mode] No relevant documents found in the knowledge base. "
                "Upload documents first and try again."
            )

        context_preview = context[:500].replace("\n", " ")
        n_chunks = context.count("---\n") + 1

        return (
            f"[Demo Mode — Simulated Answer]\n\n"
            f"Based on the {n_chunks} retrieved document chunk(s), here is what I found:\n\n"
            f"{context_preview}...\n\n"
            f"💡 *To get real LLM-powered answers, set LLM_PROVIDER=openai or LLM_PROVIDER=ollama in .env*"
        )

    def _ask_demo_json(self, prompt: str, context: str = None) -> str:
        import json
        sample = json.dumps([
            {"name": "Example Item", "value": 42, "status": "active"},
            {"name": "Sample Entry", "value": 100, "status": "pending"},
        ], indent=2)
        return (
            f"[Demo Mode — Structured Data]\n\n"
            f"Auto-detected schema from document. Extracted {2} records:\n\n"
            f"{sample}\n\n"
            f"💡 *To get real AI-powered extraction, set LLM_PROVIDER=openai or ollama in .env*"
        )

    @staticmethod
    def _build_messages(prompt: str, context: str = None) -> list:
        system_prompt = (
            "You are a precise document Q&A assistant. Answer questions based solely on the "
            "provided context. If the context doesn't contain the answer, say so clearly. "
            "Cite sources and page numbers when available."
        )
        messages = [{"role": "system", "content": system_prompt}]
        if context:
            messages.append({
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {prompt}",
            })
        else:
            messages.append({"role": "user", "content": prompt})
        return messages
