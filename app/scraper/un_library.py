"""
UN Digital Library scraper implementation.
"""

from app.config import TARGET_URL, PAGE_LOAD_TIMEOUT
from app.models import Resolution
from app.pdf.extractor import PDFExtractor
from app.scraper.base import Scraper


class UNLibraryScraper(Scraper):
    """Scraper for UN Digital Library resolutions."""
    
    def __init__(self):
        super().__init__(url=TARGET_URL, headless=True, timeout=PAGE_LOAD_TIMEOUT)
        self.pdf_extractor = PDFExtractor()
    
    def scrape_resolutions(self) -> list[Resolution]:
        """
        Main scraping function that orchestrates the entire extraction process.
        
        Workflow:
        1. Wait for search results to load
        2. Extract metadata from each result row
        3. Navigate to record pages to get English PDFs
        4. Download and extract text from PDFs
        
        Returns:
            List of Resolution dataclass instances with extracted data
        """
        resolutions: list[Resolution] = []
        
        try:
            print("Waiting for search results to load...")
            result_rows = self._wait_find(
                "//div[contains(@class, 'result-row')]",
                find_all=True,
                timeout=PAGE_LOAD_TIMEOUT
            )
            print(f"Found {len(result_rows)} results.")
            
            # First pass: collect metadata and record URLs
            records_to_process: list[tuple[Resolution, str]] = []
            
            for i, row in enumerate(result_rows):
                resolution = Resolution()
                
                try:
                    # Extract title
                    title_element = self._wait_find(
                        ".//div[contains(@class, 'result-title')]//a",
                        element=row,
                        timeout=2
                    )
                    resolution.title = title_element.text.strip()
                    
                    # Extract document symbol and date
                    brief_options = self._wait_find(
                        ".//div[contains(@class, 'brief-options')]",
                        element=row,
                        timeout=2
                    )
                    resolution.document_symbol, resolution.date = self._parse_brief_options(
                        brief_options.text
                    )
                    
                    # Get record page URL
                    record_url = title_element.get_attribute("href") or ""
                    records_to_process.append((resolution, record_url))
                    
                except Exception as e:
                    print(f"  Warning: Error collecting metadata for row {i + 1}: {e}")
                    resolution.extracted_text_snippet = f"[Error: {str(e)[:50]}]"
                    resolutions.append(resolution)
            
            # Second pass: navigate to each record page to get English PDFs
            print(f"\nNavigating to record pages to find English PDFs...")
            
            for resolution, record_url in records_to_process:
                try:
                    print(f"Processing {resolution.document_symbol}...")
                    
                    # Navigate to record page to find English PDF
                    resolution.pdf_url = self._get_english_pdf_from_record_page(record_url)
                    
                    # Extract text from PDF
                    if resolution.pdf_url:
                        resolution.extracted_text_snippet = self.pdf_extractor.extract_text(
                            resolution.pdf_url
                        )
                    else:
                        resolution.extracted_text_snippet = "[No PDF available]"
                        
                except Exception as e:
                    print(f"  Warning: Error processing {resolution.document_symbol}: {e}")
                    resolution.extracted_text_snippet = f"[Error: {str(e)[:50]}]"
                
                resolutions.append(resolution)
                
        except Exception as e:
            print(f"Error during scraping: {e}")
            raise
        
        return resolutions
    
    def _parse_brief_options(self, brief_options_text: str) -> tuple[str, str]:
        """
        Parse the brief options text to extract document symbol and date.
        
        Format: "Symbol | Date | Collection"
        Example: "A/RES/2758(XXVI) | 1971-10-25 | Resolutions and Decisions"
        """
        parts = brief_options_text.split("|")
        document_symbol = parts[0].strip() if len(parts) > 0 else ""
        date = parts[1].strip() if len(parts) > 1 else ""
        return document_symbol, date
    
    def _get_english_pdf_from_record_page(self, record_url: str) -> str:
        """
        Navigate to a record page and find the English PDF URL.
        
        English PDFs have URLs ending in '-EN.pdf'.
        """
        if not record_url:
            return ""
        
        try:
            self.driver.get(record_url)
            
            # Find PDF links using XPath
            try:
                pdf_links = self._wait_find(
                    "//a[contains(@href, '.pdf')]",
                    find_all=True,
                    timeout=PAGE_LOAD_TIMEOUT
                )
            except Exception:
                return ""  # No PDF links found
            
            # Look for English version first
            for link in pdf_links:
                href = link.get_attribute("href") or ""
                if "-EN.pdf" in href:
                    return href
            
            # Fallback: avoid non-English versions
            non_english_suffixes = ["-AR.pdf", "-CH.pdf", "-ZH.pdf", "-FR.pdf", "-RU.pdf", "-ES.pdf"]
            for link in pdf_links:
                href = link.get_attribute("href") or ""
                if not any(suffix in href for suffix in non_english_suffixes):
                    return href
            
            # Return first available if only non-English
            if pdf_links:
                return pdf_links[0].get_attribute("href") or ""
                
        except Exception as e:
            print(f"  Warning: Error getting English PDF: {e}")
        
        return ""
