"""Web scraping utilities with JavaScript support."""
import logging
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)


class WebScraper:
    """Web scraping with JavaScript rendering support."""
    
    @staticmethod
    def scrape_static(url: str, headers: Optional[Dict[str, str]] = None) -> str:
        """
        Scrape a static webpage (no JavaScript).
        
        Args:
            url: URL to scrape
            headers: Optional HTTP headers
            
        Returns:
            HTML content
        """
        try:
            logger.info(f"Scraping static page: {url}")
            response = requests.get(url, headers=headers or {}, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return ""
    
    @staticmethod
    async def scrape_dynamic(url: str) -> str:
        """
        Scrape a page with JavaScript rendering.
        
        Args:
            url: URL to scrape
            
        Returns:
            Rendered HTML content
        """
        try:
            logger.info(f"Scraping dynamic page: {url}")
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, wait_until="networkidle")
                content = await page.content()
                await browser.close()
                return content
        except Exception as e:
            logger.error(f"Error scraping dynamic page {url}: {e}")
            return ""
    
    @staticmethod
    def extract_text(html: str) -> str:
        """
        Extract text from HTML.
        
        Args:
            html: HTML content
            
        Returns:
            Extracted text
        """
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(strip=True, separator=' ')
    
    @staticmethod
    def fetch_api(
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Fetch data from an API.
        
        Args:
            url: API endpoint URL
            method: HTTP method
            headers: HTTP headers
            data: Request data
            
        Returns:
            API response (parsed JSON or text)
        """
        try:
            logger.info(f"Fetching API: {method} {url}")
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=data, timeout=30)
            else:
                response = requests.post(url, headers=headers, json=data, timeout=30)
            
            response.raise_for_status()
            
            # Try to parse as JSON
            try:
                return response.json()
            except:
                return response.text
                
        except Exception as e:
            logger.error(f"Error fetching API {url}: {e}")
            return None
