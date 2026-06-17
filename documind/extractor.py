import json
from typing import Any, Dict, List, Optional

from documind.document_loader import Document
from documind.llm import LLMEngine


class Extractor:
    def __init__(self, llm: LLMEngine = None):
        self.llm = llm or LLMEngine()

    def extract(self, documents: List[Document], schema: Dict[str, str] = None) -> List[Dict[str, Any]]:
        if not documents:
            return []

        full_text = "\n\n".join(d.content for d in documents if d.content.strip())
        if not full_text.strip():
            return []

        if schema:
            prompt = self._build_schema_prompt(full_text, schema)
        else:
            prompt = self._build_auto_prompt(full_text)

        raw = self.llm.ask(prompt, context=None)
        return self._parse_result(raw)

    def extract_from_text(self, text: str, schema: Dict[str, str] = None) -> List[Dict[str, Any]]:
        return self.extract([Document(content=text, metadata={})], schema=schema)

    @staticmethod
    def _build_auto_prompt(text: str) -> str:
        return (
            "Extract structured data from the following document. "
            "Identify all entities, fields, and relationships automatically. "
            "Return a JSON array of objects. "
            "Be thorough — extract names, dates, amounts, statuses, IDs, and any key information.\n\n"
            f"Document:\n{text[:6000]}"
        )

    @staticmethod
    def _build_schema_prompt(text: str, schema: Dict[str, str]) -> str:
        fields_desc = "\n".join(f'  "{k}": {v}' for k, v in schema.items())
        return (
            "Extract structured data from the following document using this schema:\n"
            f"{{\n{fields_desc}\n}}\n\n"
            "Return a JSON array of objects matching the schema above. "
            "If a field is not found, use null. Be thorough.\n\n"
            f"Document:\n{text[:6000]}"
        )

    @staticmethod
    def _parse_result(raw: str) -> List[Dict[str, Any]]:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[-1]
            cleaned = cleaned.rsplit("```", 1)[0]
        cleaned = cleaned.strip()

        json_start = cleaned.find("[")
        json_end = cleaned.rfind("]")
        if json_start != -1 and json_end != -1:
            cleaned = cleaned[json_start:json_end + 1]

        try:
            result = json.loads(cleaned)
            return result if isinstance(result, list) else [result]
        except json.JSONDecodeError:
            try:
                json_start = cleaned.find("{")
                json_end = cleaned.rfind("}")
                if json_start != -1 and json_end != -1:
                    result = json.loads(cleaned[json_start:json_end + 1])
                    return result if isinstance(result, list) else [result]
            except json.JSONDecodeError:
                pass
            return [{"raw": cleaned, "error": "Failed to parse JSON"}]
