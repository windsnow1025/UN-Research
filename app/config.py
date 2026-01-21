# Configuration constants for UN Digital Library Scraper
from enum import Enum


class ScrapeMode(Enum):
    """Available scraping modes."""
    RESOLUTION = "resolution"
    UPR = "upr"


# =============================================================================
# Scrape Mode Configuration (Change this to switch between modes)
# =============================================================================

SCRAPE_MODE: ScrapeMode = ScrapeMode.RESOLUTION

# =============================================================================
# URL Configuration
# =============================================================================

RESOLUTION_URL: str = "https://digitallibrary.un.org/search?cc=Resolutions%20and%20Decisions&ln=en&as=1&rm=&sf=latest%20first&so=d&rg=100&c=Resolutions%20and%20Decisions&c=&of=hb&fti=0&fti=0&as_query=JTdCJTIyZGF0ZV9zZWxlY3RvciUyMiUzQSU3QiUyMmRhdGVUeXBlJTIyJTNBJTIyY3JlYXRpb25fZGF0ZSUyMiUyQyUyMmRhdGVQZXJpb2QlMjIlM0ElMjJhbGx5ZWFycyUyMiUyQyUyMmRhdGVGcm9tJTIyJTNBJTIyJTIyJTJDJTIyZGF0ZVRvJTIyJTNBJTIyJTIyJTdEJTJDJTIyY2xhdXNlcyUyMiUzQSU1QiU3QiUyMnNlYXJjaEluJTIyJTNBJTIydGl0bGUlMjIlMkMlMjJjb250YWluJTIyJTNBJTIyYWxsLXdvcmRzJTIyJTJDJTIydGVybSUyMiUzQSUyMiUyMiUyQyUyMm9wZXJhdG9yJTIyJTNBJTIyQU5EJTIyJTdEJTVEJTdE"

UPR_URL: str = "https://digitallibrary.un.org/search?cc=Resolutions%20and%20Decisions&ln=en&as=1&rm=&sf=latest%20first&so=d&rg=100&c=Human%20Rights%20Council&c=&of=hb&fti=0&fti=0&as_query=JTdCJTIyZGF0ZV9zZWxlY3RvciUyMiUzQSU3QiUyMmRhdGVUeXBlJTIyJTNBJTIyY3JlYXRpb25fZGF0ZSUyMiUyQyUyMmRhdGVQZXJpb2QlMjIlM0ElMjJhbGx5ZWFycyUyMiUyQyUyMmRhdGVGcm9tJTIyJTNBJTIyJTIyJTJDJTIyZGF0ZVRvJTIyJTNBJTIyJTIyJTdEJTJDJTIyY2xhdXNlcyUyMiUzQSU1QiU3QiUyMnNlYXJjaEluJTIyJTNBJTIydGl0bGUlMjIlMkMlMjJjb250YWluJTIyJTNBJTIyYWxsLXdvcmRzJTIyJTJDJTIydGVybSUyMiUzQSUyMlJlcG9ydCUyMG9mJTIwdGhlJTIwV29ya2luZyUyMEdyb3VwJTIwb24lMjB0aGUlMjBVbml2ZXJzYWwlMjBQZXJpb2RpYyUyMFJldmlldyUyMiUyQyUyMm9wZXJhdG9yJTIyJTNBJTIyQU5EJTIyJTdEJTVEJTdE"

# =============================================================================
# Output Configuration
# =============================================================================

RESOLUTION_OUTPUT_FILE: str = "data/UN_Resolutions.csv"
UPR_OUTPUT_FILE: str = "data/UN_UPR_Reports.csv"

# =============================================================================
# Derived Configuration (based on SCRAPE_MODE)
# =============================================================================

SCRAPE_URL: str = UPR_URL if SCRAPE_MODE == ScrapeMode.UPR else RESOLUTION_URL
OUTPUT_FILE: str = UPR_OUTPUT_FILE if SCRAPE_MODE == ScrapeMode.UPR else RESOLUTION_OUTPUT_FILE

# =============================================================================
# PDF Configuration
# =============================================================================

TEXT_SNIPPET_LENGTH: int = 500  # First 500 characters from PDF

# =============================================================================
# Network Configuration
# =============================================================================

REQUEST_TIMEOUT: int = 10  # Timeout for HTTP requests in seconds
PAGE_LOAD_TIMEOUT: int = 10  # Timeout for page loads in seconds

# =============================================================================
# OCR Configuration
# =============================================================================

# Tesseract OCR configuration (Windows default path)
TESSDATA_PATH: str = r"C:\Program Files\Tesseract-OCR\tessdata"

