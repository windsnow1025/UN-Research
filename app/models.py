"""
Data models for UN Digital Library Scraper.
"""

from dataclasses import dataclass


@dataclass
class Resolution:
    """Data class representing a UN resolution with extracted metadata."""
    date: str = ""
    document_symbol: str = ""
    title: str = ""
    pdf_url: str = ""
    extracted_text_snippet: str = ""
