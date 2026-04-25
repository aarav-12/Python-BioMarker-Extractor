"""
Pipeline: PDF -> extract -> return raw list.
No domain mapping, no validation, no normalization.
Node backend owns all of that.
"""

from __future__ import annotations

import logging

from pdfplumber import open as pdf_open

from extractor import extract_biomarkers
from age_extractor import extract_age

logger = logging.getLogger(__name__)


def extract_text(pdf_path):
    text = ""
    with pdf_open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def run_pipeline(pdf_path: str) -> dict:
    text = extract_text(pdf_path)
    chunks = [text]

    try:
        biomarkers = extract_biomarkers(chunks, pdf_path=pdf_path)
    except Exception as exc:
        logger.exception("Extraction failed")
        return {"error": f"Extraction failed: {exc}"}

    if not biomarkers:
        return {"error": "No biomarkers found in this report"}

    age_result = extract_age(pdf_path)

    return {
        "biomarkers": biomarkers,
        "count": len(biomarkers),
        **age_result,
    }
