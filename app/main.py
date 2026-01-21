"""
UN Digital Library Web Scraper

This script scrapes the United Nations Digital Library to extract metadata 
and text snippets from General Assembly resolutions and UPR reports.

Author: Interview Demo Script
Dependencies: selenium, pymupdf, pandas, webdriver-manager, requests
"""

from app.config import SCRAPE_MODE, ScrapeMode
from app.scraper.un_library import UNLibraryScraper
from app.output.csv_writer import save_to_csv


def main() -> None:
    """Main entry point for the scraper script."""
    mode_name = "UPR Reports" if SCRAPE_MODE == ScrapeMode.UPR else "Resolutions"
    
    print("=" * 60)
    print(f"UN Digital Library Web Scraper - {mode_name}")
    print("=" * 60)
    print()
    
    print("Initializing browser...")
    print("Navigating to UN Digital Library...")
    
    with UNLibraryScraper() as scraper:
        resolutions = scraper.scrape_resolutions()
    
    print("Browser closed.")
    
    # Save results to CSV
    if resolutions:
        save_to_csv(resolutions)
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"Summary ({mode_name}):")
        print(f"  Total extracted: {len(resolutions)}")
        text_count = sum(
            1 for r in resolutions 
            if r.extracted_text_snippet and not r.extracted_text_snippet.startswith('[')
        )
        print(f"  With PDF text: {text_count}")
        print("=" * 60)
    else:
        print("No documents were extracted.")


if __name__ == "__main__":
    main()

