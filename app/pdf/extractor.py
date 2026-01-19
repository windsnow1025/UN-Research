"""
PDF download and text extraction with OCR support.
"""

import re

import fitz  # PyMuPDF
import requests

from app.config import REQUEST_TIMEOUT, TEXT_SNIPPET_LENGTH, TESSDATA_PATH


class PDFExtractor:
    """Handles PDF download and text extraction with OCR fallback."""
    
    def __init__(self, max_chars: int = TEXT_SNIPPET_LENGTH):
        self.max_chars = max_chars
    
    def extract_text(self, pdf_url: str) -> str:
        """
        Download a PDF and extract text content.
        
        Falls back to OCR if no text layer is found.
        
        Args:
            pdf_url: URL of the PDF to process
            
        Returns:
            Extracted text snippet or error message
        """
        pdf_bytes = self._download_pdf(pdf_url)
        if not pdf_bytes:
            return "[PDF download failed]"
        
        return self._extract_text_from_bytes(pdf_bytes)
    
    def _download_pdf(self, pdf_url: str) -> bytes | None:
        """Download a PDF file into memory."""
        try:
            response = requests.get(
                pdf_url,
                timeout=REQUEST_TIMEOUT,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
                }
            )
            response.raise_for_status()
            return response.content
            
        except requests.RequestException as e:
            print(f"  Warning: Failed to download PDF: {e}")
            return None
    
    def _extract_text_from_bytes(self, pdf_bytes: bytes) -> str:
        """
        Extract text from PDF bytes.
        
        Uses PyMuPDF for text extraction with Tesseract OCR fallback.
        """
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            extracted_text = ""
            used_ocr = False
            
            # First pass: try to extract existing text layer
            for page in doc:
                page_text = page.get_text() or ""
                extracted_text += page_text
                
                if len(extracted_text) >= self.max_chars:
                    break
            
            # Clean up whitespace
            extracted_text = re.sub(r'\s+', ' ', extracted_text).strip()
            
            # If no text found, try OCR on the first page
            if not extracted_text:
                print("    No text layer found, attempting OCR...")
                try:
                    doc.close()
                    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                    
                    first_page = doc[0]
                    tp = first_page.get_textpage_ocr(
                        language="eng",
                        tessdata=TESSDATA_PATH,
                        full=True
                    )
                    extracted_text = first_page.get_text(textpage=tp) or ""
                    extracted_text = re.sub(r'\s+', ' ', extracted_text).strip()
                    used_ocr = True
                    
                    if extracted_text:
                        print("    OCR successful!")
                    else:
                        print("    OCR returned no text")
                        
                except Exception as ocr_error:
                    print(f"    OCR failed: {ocr_error}")
                    return "[OCR failed - check Tesseract installation]"
            
            doc.close()
            
            if not extracted_text:
                return "[No text could be extracted]"
            
            # Add OCR indicator if used
            result = extracted_text[:self.max_chars]
            if used_ocr:
                result = "[OCR] " + result
                
            return result
                
        except Exception as e:
            print(f"  Warning: Failed to extract text from PDF: {e}")
            return f"[Error: {str(e)[:50]}]"
