"""Quiz solver using headless browser and LLM."""
import asyncio
import base64
import logging
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright, Page, Browser
import requests

from config import Config
from llm_agent import LLMAgent

logger = logging.getLogger(__name__)


class QuizSolver:
    """Solves quiz questions using browser automation and LLM."""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.llm_agent = LLMAgent()
        self.start_time = None
    
    async def setup_browser(self):
        """Initialize Playwright and browser."""
        if not self.playwright:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            logger.info("Browser initialized")
    
    async def cleanup(self):
        """Clean up browser resources."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("Browser cleaned up")
    
    async def fetch_quiz_page(self, url: str) -> str:
        """
        Fetch and render the quiz page.
        
        Args:
            url: Quiz page URL
            
        Returns:
            Rendered HTML content
        """
        await self.setup_browser()
        
        page = await self.browser.new_page()
        try:
            logger.info(f"Navigating to quiz page: {url}")
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Wait for JavaScript to render
            await page.wait_for_timeout(2000)
            
            # Get the full HTML content
            content = await page.content()
            logger.info("Quiz page loaded successfully")
            
            return content
            
        finally:
            await page.close()
    
    def extract_question(self, html_content: str) -> Optional[str]:
        """
        Extract the question from the HTML content.
        
        The question is typically base64-encoded in a script tag.
        
        Args:
            html_content: HTML content of the quiz page
            
        Returns:
            Decoded question text or None
        """
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for script tags with base64 content
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'atob' in script.string:
                # Try to extract base64 content
                try:
                    # Look for base64 string in backticks or quotes
                    import re
                    b64_pattern = r'atob\([`"\']([A-Za-z0-9+/=\n]+)[`"\']'
                    match = re.search(b64_pattern, script.string, re.DOTALL)
                    
                    if match:
                        b64_content = match.group(1).replace('\n', '')
                        decoded = base64.b64decode(b64_content).decode('utf-8')
                        logger.info(f"Decoded question: {decoded[:200]}...")
                        return decoded
                except Exception as e:
                    logger.warning(f"Error decoding base64: {e}")
        
        # Fallback: return the visible text
        result_div = soup.find(id='result')
        if result_div:
            return result_div.get_text(strip=True)
        
        # Last resort: return full body text
        body = soup.find('body')
        if body:
            return body.get_text(strip=True)
        
        return html_content
    
    def extract_submit_url(self, question_text: str) -> Optional[str]:
        """
        Extract the submit URL from the question text.
        
        Args:
            question_text: The decoded question text
            
        Returns:
            Submit URL or None
        """
        import re
        
        # Look for URLs in the question
        url_pattern = r'https?://[^\s<>"\']+/submit'
        matches = re.findall(url_pattern, question_text)
        
        if matches:
            logger.info(f"Found submit URL: {matches[0]}")
            return matches[0]
        
        # Try to find any URL mentioned
        url_pattern = r'https?://[^\s<>"\']+'
        matches = re.findall(url_pattern, question_text)
        
        for url in matches:
            if 'submit' in url.lower():
                logger.info(f"Found submit URL: {url}")
                return url
        
        return None
    
    async def solve(self, quiz_url: str) -> Dict[str, Any]:
        """
        Solve a single quiz question.
        
        Args:
            quiz_url: URL of the quiz page
            
        Returns:
            Dict with result info including next_url if available
        """
        import time
        self.start_time = time.time()
        
        try:
            # Fetch the quiz page
            html_content = await self.fetch_quiz_page(quiz_url)
            
            # Extract question
            question_text = self.extract_question(html_content)
            if not question_text:
                logger.error("Failed to extract question from page")
                return {"success": False, "error": "Could not extract question"}
            
            logger.info(f"Question extracted, length: {len(question_text)}")
            
            # Extract submit URL
            submit_url = self.extract_submit_url(question_text)
            if not submit_url:
                logger.warning("Could not extract submit URL, will try to infer")
            
            # Use LLM to solve the question
            answer = await self.llm_agent.solve_question(question_text, quiz_url)
            
            if answer is None:
                logger.error("LLM failed to generate answer")
                return {"success": False, "error": "LLM failed to solve"}
            
            logger.info(f"Generated answer: {str(answer)[:200]}")
            
            # Submit the answer
            if submit_url:
                result = self.submit_answer(submit_url, quiz_url, answer)
                return result
            else:
                logger.error("No submit URL found")
                return {"success": False, "error": "No submit URL"}
                
        except Exception as e:
            logger.error(f"Error solving quiz: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
    
    def submit_answer(
        self,
        submit_url: str,
        quiz_url: str,
        answer: Any
    ) -> Dict[str, Any]:
        """
        Submit the answer to the quiz endpoint.
        
        Args:
            submit_url: URL to submit the answer
            quiz_url: Original quiz URL
            answer: The answer to submit
            
        Returns:
            Response from the server including next_url if available
        """
        payload = {
            "email": Config.STUDENT_EMAIL,
            "secret": Config.STUDENT_SECRET,
            "url": quiz_url,
            "answer": answer
        }
        
        try:
            logger.info(f"Submitting answer to {submit_url}")
            response = requests.post(
                submit_url,
                json=payload,
                timeout=30
            )
            
            logger.info(f"Submit response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Submit response: {result}")
                
                is_correct = result.get("correct", False)
                next_url = result.get("url")
                reason = result.get("reason")
                
                if is_correct:
                    logger.info("✓ Answer CORRECT!")
                else:
                    logger.warning(f"✗ Answer INCORRECT. Reason: {reason}")
                
                return {
                    "success": True,
                    "correct": is_correct,
                    "next_url": next_url,
                    "reason": reason,
                    "response": result
                }
            else:
                logger.error(f"Submit failed with status {response.status_code}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "response": response.text
                }
                
        except Exception as e:
            logger.error(f"Error submitting answer: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
