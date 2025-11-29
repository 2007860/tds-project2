"""Simple test to verify app can import without running server."""
import sys

print("Testing imports...")

try:
    from config import Config
    print("✓ config.py imported")
except Exception as e:
    print(f"✗ config.py failed: {e}")
    sys.exit(1)

try:
    # Check if pandas is available (it's not required for basic operation)
    try:
        import pandas
        print("✓ pandas available")
    except ImportError:
        print("⚠ pandas not available (optional - only needed for advanced data processing)")
    
    from llm_agent import LLMAgent
    print("✓ llm_agent.py imported")
except Exception as e:
    print(f"✗llm_agent.py failed: {e}")
    sys.exit(1)

try:
    from quiz_solver import QuizSolver
    print("✓ quiz_solver.py imported")
except Exception as e:
    print(f"✗ quiz_solver.py failed: {e}")
    sys.exit(1)

try:
    from app import app
    print("✓ app.py imported")
except Exception as e:
    print(f"✗ app.py failed: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("All core imports successful!")
print("="*50)

# Check configuration
try:
    print(f"\nStudent Email: {Config.STUDENT_EMAIL}")
    print(f"OpenAI API Key: {'Set' if Config.OPENAI_API_KEY and Config.OPENAI_API_KEY != 'sk-your-openai-api-key' else 'NOT SET - UPDATE .env!'}")
    print(f"Secret: {'Set' if Config.STUDENT_SECRET and Config.STUDENT_SECRET != 'your_secret_string' else 'NOT SET - UPDATE .env!'}")
except Exception as e:
    print(f"\n⚠ Configuration warning: {e}")

print("\n✓ Ready to run: python app.py")
