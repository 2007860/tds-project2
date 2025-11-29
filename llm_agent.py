"""LLM agent for solving quiz questions."""
import asyncio
import logging
import json
from typing import Any, Optional
from openai import AsyncOpenAI

from config import Config
from tools.scraper import WebScraper
from tools.data_processor import DataProcessor
from tools.analyzer import DataAnalyzer
from tools.visualizer import Visualizer

logger = logging.getLogger(__name__)


class LLMAgent:
    """Uses LLM to understand and solve quiz questions."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
        self.scraper = WebScraper()
        self.processor = DataProcessor()
        self.analyzer = DataAnalyzer()
        self.visualizer = Visualizer()
    
    async def solve_question(self, question_text: str, quiz_url: str) -> Optional[Any]:
        """
        Solve a quiz question using LLM and available tools.
        
        Args:
            question_text: The question to solve
            quiz_url: Original quiz URL for context
            
        Returns:
            The answer (can be bool, int, float, str, dict, or base64 string)
        """
        try:
            # Use GPT-4 to analyze and solve the question
            system_prompt = """You are a data analysis expert solving quiz questions.

You have access to these capabilities:
- Web scraping (with JavaScript support)
- API data fetching
- Data processing (CSV, Excel, PDF, text)
- Data analysis (filtering, sorting, aggregating, statistics)
- Visualization (charts, graphs)

Given a question, determine what data you need, how to get it, how to process it, and what the answer is.

Return your response as a JSON object with this structure:
{
    "steps": ["step 1", "step 2", ...],
    "data_needed": "description of data needed",
    "processing": "how to process the data",
    "answer": <the final answer>,
    "answer_type": "boolean|number|string|base64|json"
}

The answer field should contain the actual answer value.
If the answer is a file/image, use base64 encoding and set answer_type to "base64".
"""
            
            user_prompt = f"""Question:
{question_text}

Quiz URL: {quiz_url}

Analyze this question and solve it step by step. Return the answer in the specified JSON format."""
            
            logger.info("Calling GPT-4 to analyze question...")
            
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            logger.info(f"LLM response: {result_text[:500]}")
            
            result = json.loads(result_text)
            
            # Execute the plan
            answer = await self.execute_plan(result, question_text, quiz_url)
            
            return answer
            
        except Exception as e:
            logger.error(f"Error in solve_question: {e}", exc_info=True)
            return None
    
    async def execute_plan(self, plan: dict, question_text: str, quiz_url: str) -> Any:
        """
        Execute the LLM's plan to solve the question.
        
        Args:
            plan: The plan from LLM
            question_text: Original question
            quiz_url: Quiz URL
            
        Returns:
            The final answer
        """
        try:
            # Check if the answer is already in the plan
            if "answer" in plan:
                answer = plan["answer"]
                answer_type = plan.get("answer_type", "string")
                
                logger.info(f"Answer from LLM: {answer} (type: {answer_type})")
                
                # Convert answer to appropriate type
                if answer_type == "number":
                    if isinstance(answer, (int, float)):
                        return answer
                    return float(answer) if '.' in str(answer) else int(answer)
                elif answer_type == "boolean":
                    if isinstance(answer, bool):
                        return answer
                    return str(answer).lower() in ('true', 'yes', '1')
                elif answer_type == "json":
                    if isinstance(answer, dict):
                        return answer
                    return json.loads(answer) if isinstance(answer, str) else answer
                else:
                    return answer
            
            # If no direct answer, try to execute steps
            steps = plan.get("steps", [])
            logger.info(f"Executing {len(steps)} steps...")
            
            # For now, return a simple answer
            # In a full implementation, we would execute each step using the tools
            return None
            
        except Exception as e:
            logger.error(f"Error executing plan: {e}", exc_info=True)
            return None
    
    async def download_and_process_file(self, url: str) -> Any:
        """
        Download and process a file from a URL.
        
        Args:
            url: URL of the file to download
            
        Returns:
            Processed data
        """
        try:
            import requests
            import tempfile
            import os
            
            logger.info(f"Downloading file from {url}")
            response = requests.get(url, timeout=30)
            
            # Determine file type from URL or content-type
            content_type = response.headers.get('content-type', '')
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.tmp') as f:
                f.write(response.content)
                temp_path = f.name
            
            try:
                # Process based on file type
                if 'pdf' in url.lower() or 'pdf' in content_type:
                    data = self.processor.process_pdf(temp_path)
                elif 'csv' in url.lower() or 'csv' in content_type:
                    data = self.processor.process_csv(temp_path)
                elif 'excel' in url.lower() or 'xls' in url.lower():
                    data = self.processor.process_excel(temp_path)
                else:
                    # Try as text
                    data = response.text
                
                return data
            finally:
                # Clean up temp file
                os.unlink(temp_path)
                
        except Exception as e:
            logger.error(f"Error downloading/processing file: {e}", exc_info=True)
            return None
