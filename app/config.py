# Configuration constants for UN Digital Library Scraper

# =============================================================================
# Search Configuration
# =============================================================================

TARGET_URL: str = "https://digitallibrary.un.org/search?cc=Resolutions%20and%20Decisions&ln=en&p=china&f=&rm=&sf=latest%20first&so=d&rg=50&c=Resolutions%20and%20Decisions&c=&of=hb&fti=0&fti=0"

TEXT_SNIPPET_LENGTH: int = 500  # First 500 characters from PDF

# =============================================================================
# Network Configuration
# =============================================================================

REQUEST_TIMEOUT: int = 30  # Timeout for HTTP requests in seconds
PAGE_LOAD_TIMEOUT: int = 30  # Timeout for page loads in seconds

# =============================================================================
# Output Configuration
# =============================================================================

OUTPUT_FILENAME: str = "data/UN_Resolutions_Sample.csv"

# =============================================================================
# OCR Configuration
# =============================================================================

# Tesseract OCR configuration (Windows default path)
TESSDATA_PATH: str = r"C:\Program Files\Tesseract-OCR\tessdata"
