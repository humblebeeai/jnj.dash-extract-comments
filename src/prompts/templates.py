"""
Templates for OpenAI Prompts.
"""

COLUMN_NAME_EXTRACTION_PROMPT = """You are a data architect helping build a dashboard. The input is a “description document” (PDF text) that describes what data should be captured for a case/procedure/workflow.

IMPORTANT:
The dashboard already has a fixed list of column names provided by the user.
You MUST NOT invent new fields.
You MUST output definitions ONLY for the provided fields, in the SAME ORDER as given.

Task:
For each provided column name, find its definition in the document text and fill the schema.

Output:
Return ONLY valid JSON with this structure:

{
  "document_title": "<string or null>",
  "fields": [
    {
      "name": "<EXACT column name from the provided list>",
      "label": "<human readable label>",
      "type": "<one of: string, number, integer, boolean, date, datetime, enum, array, object>",
      "required": <true/false/null>,
      "allowed_values": ["..."] or null,
      "unit": "<unit>" or null,
      "scale": "<e.g., 1-5>" or null,
      "how_to_fill": "<short instruction from doc>" or null,
      "source_hint": "<short quote or keyword from the doc, max 12 words>"
    }
  ]
}

Rules:
- Do NOT include any text outside JSON.
- Use EXACT column names as provided. Do NOT rename them.
- If the document does not define a field, set how_to_fill=null and source_hint="not specified in document".
- YES/NO/NA fields -> type=enum and allowed_values=["YES","NO","NA",""] if empty allowed.
- 1-5 rating fields -> type=integer and scale="1-5".
- Sizes like cm2 -> type=number and unit="cm2".
- If a field can contain multiple values -> use type=array.

--------------------------------------------------
COLUMN_NAMES
--------------------------------------------------
{COLUMN_NAMES}

--------------------------------------------------
TEXT
--------------------------------------------------
{pdf_text}
"""

DATA_EXTRACTION_PROMPT = """You are a structured data extraction engine.

Your task is to extract values from ONE row of text and populate ONLY the requested dashboard columns.

--------------------------------------------------
OUTPUT RULES
--------------------------------------------------

- Return ONLY a valid JSON object
- Keys MUST be EXACTLY the column names in TARGET_COLUMNS
- Do NOT output extra fields
- If value not found -> return null
- Follow COLUMN DEFINITIONS strictly:
  - integer/number -> numeric output
  - enum -> must match allowed_values
  - string -> text
- Respect units and scale if defined
- If multiple values exist:
  - If column type is string -> comma-separated
  - Otherwise -> most relevant single value
- Do NOT invent values

--------------------------------------------------
TARGET_COLUMNS
--------------------------------------------------
{TARGET_COLUMNS}

--------------------------------------------------
COLUMN_DEFINITIONS
--------------------------------------------------
{COLUMN_DEFINITIONS}

--------------------------------------------------
ROW_TEXT
--------------------------------------------------
\"\"\"{ROW_TEXT}\"\"\"
"""
