"""
CSV export functionality for resolution data.
"""

import pandas as pd

from app.config import OUTPUT_FILENAME
from app.models import Resolution


def save_to_csv(
    resolutions: list[Resolution], 
    filename: str = OUTPUT_FILENAME
) -> None:
    """
    Save extracted resolutions to a CSV file.
    
    Args:
        resolutions: List of Resolution objects to save
        filename: Output filename for the CSV
    """
    data = [
        {
            "Date": r.date,
            "Document_Symbol": r.document_symbol,
            "Title": r.title,
            "PDF_URL": r.pdf_url,
            "Extracted_Text_Snippet": r.extracted_text_snippet
        }
        for r in resolutions
    ]
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8")
    
    print(f"\nSuccessfully saved {len(resolutions)} resolutions to '{filename}'")
