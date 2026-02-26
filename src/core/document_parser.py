import io

from pypdf import PdfReader

from src.utils.logger import get_logger

logger = get_logger(__name__)


def extract_text_from_pdf(file_stream: io.BytesIO) -> str:
    """
    Extracts text from a PDF file stream.

    Args:
        file_stream (io.BytesIO): The uploaded PDF file as a byte stream.

    Returns:
        str: The extracted text from all pages.
    """
    try:
        reader = PdfReader(file_stream)
        logger.info(f"PDF contains {len(reader.pages)} pages.")

        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

        logger.info(f"Extracted {len(text)} characters from PDF.")
        return text
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {e}")
        raise ValueError(f"Could not read PDF: {e}")
