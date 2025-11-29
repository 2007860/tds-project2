"""Data processing utilities for various file formats."""
import logging
from typing import Any, Optional
import io

logger = logging.getLogger(__name__)

# Optional imports - these are only needed for advanced data processing
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    logger.warning("pandas not available - data processing features limited")

try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("pdfplumber not available - PDF processing disabled")


class DataProcessor:
    """Process and clean data from various sources."""
    
    @staticmethod
    def process_csv(file_path: str) -> Optional[pd.DataFrame]:
        """
        Process a CSV file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            DataFrame or None
        """
        try:
            logger.info(f"Processing CSV: {file_path}")
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
            return df
        except Exception as e:
            logger.error(f"Error processing CSV: {e}")
            return None
    
    @staticmethod
    def process_excel(file_path: str, sheet_name: Any = 0) -> Optional[pd.DataFrame]:
        """
        Process an Excel file.
        
        Args:
            file_path: Path to Excel file
            sheet_name: Sheet name or index
            
        Returns:
            DataFrame or None
        """
        try:
            logger.info(f"Processing Excel: {file_path}")
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
            return df
        except Exception as e:
            logger.error(f"Error processing Excel: {e}")
            return None
    
    @staticmethod
    def process_pdf(file_path: str, page_num: Optional[int] = None) -> Optional[str]:
        """
        Extract text from PDF.
        
        Args:
            file_path: Path to PDF file
            page_num: Specific page number (0-indexed), or None for all pages
            
        Returns:
            Extracted text or None
        """
        try:
            logger.info(f"Processing PDF: {file_path}")
            with pdfplumber.open(file_path) as pdf:
                if page_num is not None:
                    # Extract specific page
                    if page_num < len(pdf.pages):
                        text = pdf.pages[page_num].extract_text()
                        logger.info(f"Extracted text from page {page_num}")
                        return text
                    else:
                        logger.error(f"Page {page_num} not found")
                        return None
                else:
                    # Extract all pages
                    texts = []
                    for i, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text:
                            texts.append(f"--- Page {i+1} ---\n{text}")
                    logger.info(f"Extracted text from {len(pdf.pages)} pages")
                    return "\n\n".join(texts)
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            return None
    
    @staticmethod
    def extract_tables_from_pdf(file_path: str, page_num: int) -> Optional[list]:
        """
        Extract tables from PDF page.
        
        Args:
            file_path: Path to PDF file
            page_num: Page number (0-indexed)
            
        Returns:
            List of tables (each as list of lists) or None
        """
        try:
            logger.info(f"Extracting tables from PDF page {page_num}")
            with pdfplumber.open(file_path) as pdf:
                if page_num < len(pdf.pages):
                    tables = pdf.pages[page_num].extract_tables()
                    logger.info(f"Found {len(tables)} tables on page {page_num}")
                    
                    # Convert tables to DataFrames
                    dfs = []
                    for table in tables:
                        if table and len(table) > 1:
                            df = pd.DataFrame(table[1:], columns=table[0])
                            dfs.append(df)
                    
                    return dfs
        except Exception as e:
            logger.error(f"Error extracting tables from PDF: {e}")
            return None
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        import re
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters (keep alphanumeric and basic punctuation)
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        return text.strip()
    
    @staticmethod
    def parse_json(text: str) -> Optional[Any]:
        """
        Parse JSON from text.
        
        Args:
            text: JSON string
            
        Returns:
            Parsed JSON or None
        """
        import json
        
        try:
            return json.loads(text)
        except Exception as e:
            logger.error(f"Error parsing JSON: {e}")
            return None
