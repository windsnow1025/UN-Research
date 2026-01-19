"""
UN Digital Library Web Scraper

This script scrapes the United Nations Digital Library to extract metadata 
and text snippets from General Assembly resolutions.

Author: Interview Demo Script
Dependencies: selenium, pymupdf, pandas, webdriver-manager, requests
"""

from app.scraper.un_library import UNLibraryScraper
from app.output.csv_writer import save_to_csv


def main() -> None:
    """Main entry point for the scraper script."""
    print("=" * 60)
    print("UN Digital Library Web Scraper")
    print("=" * 60)
    print()
    
    # Use context manager for automatic cleanup
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
        print("Summary:")
        print(f"  Total resolutions extracted: {len(resolutions)}")
        text_count = sum(
            1 for r in resolutions 
            if r.extracted_text_snippet and not r.extracted_text_snippet.startswith('[')
        )
        print(f"  With PDF text: {text_count}")
        print("=" * 60)
    else:
        print("No resolutions were extracted.")


if __name__ == "__main__":
    main()
