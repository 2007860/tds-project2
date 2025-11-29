"""Main FastAPI application for LLM Quiz solver."""
import asyncio
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
import uvicorn

from config import Config
from quiz_solver import QuizSolver

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="LLM Quiz Solver API")

# Pydantic model for request validation
class QuizRequest(BaseModel):
    email: str
    secret: str
    url: str    

@app.post("/quiz")
async def handle_quiz(request: Request):
    """
    Handle incoming quiz requests.
    
    Expected JSON payload:
    {
        "email": "student email",
        "secret": "student secret",
        "url": "quiz URL"
    }
    
    Returns:
        200: Quiz processing started successfully
        400: Invalid JSON payload
        403: Invalid secret
    """
    try:
        # Parse JSON payload
        try:
            data = await request.json()
        except Exception:
            logger.error("Invalid JSON payload received")
            raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
        # Validate request structure
        try:
            quiz_request = QuizRequest(**data)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise HTTPException(status_code=400, detail="Invalid request structure")
        
        # Verify secret
        if quiz_request.secret != Config.STUDENT_SECRET:
            logger.warning(f"Invalid secret provided for email: {quiz_request.email}")
            raise HTTPException(status_code=403, detail="Invalid secret")
        
        # Verify email matches
        if quiz_request.email != Config.STUDENT_EMAIL:
            logger.warning(f"Email mismatch: {quiz_request.email} vs {Config.STUDENT_EMAIL}")
            raise HTTPException(status_code=403, detail="Email does not match")
        
        logger.info(f"Received valid quiz request for URL: {quiz_request.url}")
        
        # Start quiz solving in background (don't wait for completion)
        asyncio.create_task(solve_quiz_chain(quiz_request.url))
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "processing",
                "message": "Quiz solving started",
                "url": quiz_request.url
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


async def solve_quiz_chain(initial_url: str):
    """
    Solve a chain of quiz questions starting from the initial URL.
    
    Args:
        initial_url: The first quiz URL to solve
    """
    solver = QuizSolver()
    current_url = initial_url
    question_count = 0
    max_questions = 20  # Safety limit
    
    try:
        while current_url and question_count < max_questions:
            question_count += 1
            logger.info(f"Solving question {question_count}: {current_url}")
            
            # Solve the current quiz
            result = await solver.solve(current_url)
            
            if result.get("next_url"):
                current_url = result["next_url"]
                logger.info(f"Moving to next question: {current_url}")
            else:
                logger.info("Quiz chain completed!")
                break
                
    except Exception as e:
        logger.error(f"Error in quiz chain: {e}", exc_info=True)
    finally:
        await solver.cleanup()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "LLM Quiz Solver API is running",
        "email": Config.STUDENT_EMAIL
    }


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "config_valid": bool(Config.STUDENT_EMAIL and Config.STUDENT_SECRET and Config.OPENAI_API_KEY)
    }


if __name__ == "__main__":
    # Validate configuration
    try:
        Config.validate()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        exit(1)
    
    # Run the server
    logger.info(f"Starting server on {Config.HOST}:{Config.PORT}")
    uvicorn.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        log_level="info"
    )
