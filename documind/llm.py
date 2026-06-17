from typing import Optional

from documind.config import Config


class LLMEngine:
    def __init__(self, provider: str = None):
        self.provider = (provider or Config.LLM_PROVIDER).lower()

    def ask(self, prompt: str, context: str = None) -> str:
        provider_map = {
            "openai": self._ask_openai,
            "ollama": self._ask_ollama,
            "demo": self._ask_demo,
        }
        handler = provider_map.get(self.provider)
        if not handler:
            return f"[Error] Unknown LLM provider: {self.provider}"
        return handler(prompt, context)

    def _ask_openai(self, prompt: str, context: str = None) -> str:
        import openai
        client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        messages = self._build_messages(prompt, context)
        try:
            resp = client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages,
                temperature=0.3,
                max_tokens=1024,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"[OpenAI Error] {e}"

    def _ask_ollama(self, prompt: str, context: str = None) -> str:
        import httpx
        messages = self._build_messages(prompt, context)
        try:
            resp = httpx.post(
                f"{Config.OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": Config.OLLAMA_MODEL,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0.3},
                },
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("message", {}).get("content", "").strip()
        except Exception as e:
            return f"[Ollama Error] {e}"

    def _ask_demo(self, prompt: str, context: str = None) -> str:
        if not context:
            return (
                "[Demo Mode] No relevant documents found in the knowledge base. "
                "Upload documents first and try again."
            )

        context_preview = context[:500].replace("\n", " ")
        n_chunks = context.count("[") if context.count("[") > 0 else 1

        return (
            f"[Demo Mode — Simulated Answer]\n\n"
            f"Based on the {n_chunks} retrieved document chunk(s), here is what I found:\n\n"
            f"{context_preview}...\n\n"
            f"💡 *To get real LLM-powered answers, set LLM_PROVIDER=openai or LLM_PROVIDER=ollama in .env*"
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
