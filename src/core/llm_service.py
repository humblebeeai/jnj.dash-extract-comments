import json
from typing import Any, Dict, List

from openai import OpenAI

from src.config.settings import MODEL_NAME, OPENAI_API_KEY
from src.prompts.templates import (COLUMN_NAME_EXTRACTION_PROMPT,
                                   DATA_EXTRACTION_PROMPT)
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LLMService:
    def __init__(self):
        if not OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model_name = MODEL_NAME

    def extract_column_schema(
        self, pdf_text: str, column_names: List[str]
    ) -> Dict[str, Any]:
        """
        Uses LLM to extract column definitions from PDF text based on user-provided column names.
        """
        prompt = COLUMN_NAME_EXTRACTION_PROMPT.replace(
            "{COLUMN_NAMES}", json.dumps(column_names, indent=2, ensure_ascii=False)
        ).replace("{pdf_text}", pdf_text)

        logger.info(f"Calling OpenAI ({self.model_name}) for schema extraction.")
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You extract structured dashboard schemas from documents.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                response_format={"type": "json_object"},
            )
            raw_output = response.choices[0].message.content or "{}"
            return json.loads(raw_output)
        except Exception as e:
            logger.error(f"Error during schema extraction: {e}")
            raise

    def extract_row_data(
        self, row_text: str, schema: Dict[str, Any], target_columns: List[str]
    ) -> Dict[str, Any]:
        """
        Uses LLM to extract structured data for a single row of text based on the schema.
        """
        if not row_text.strip():
            return {}

        defs_by_name = {f["name"]: f for f in schema.get("fields", [])}
        filtered_fields = [defs_by_name[c] for c in target_columns if c in defs_by_name]

        prompt = (
            DATA_EXTRACTION_PROMPT.replace(
                "{TARGET_COLUMNS}",
                json.dumps(target_columns, indent=2, ensure_ascii=False),
            )
            .replace(
                "{COLUMN_DEFINITIONS}",
                json.dumps({"fields": filtered_fields}, indent=2, ensure_ascii=False),
            )
            .replace("{ROW_TEXT}", row_text)
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                response_format={"type": "json_object"},
            )
            raw_output = response.choices[0].message.content or "{}"
            return json.loads(raw_output)
        except Exception as e:
            logger.error(f"Error during row extraction: {e}")
            return {}
