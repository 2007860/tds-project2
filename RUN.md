# How to Run the Application

## Prerequisites
- Python 3.9+ installed
- Virtual environment already created (done ✅)

## Steps to Run

### 1. Activate Virtual Environment
```bash
source venv/Scripts/activate
```

### 2. Install Dependencies (if not already installed)
```bash
./venv/Scripts/python -m pip install fastapi uvicorn playwright openai requests beautifulsoup4 python-dotenv pydantic aiohttp lxml python-multipart
./venv/Scripts/python -m playwright install chromium
```

### 3. Configure Environment
Edit `.env` file and update:
```
STUDENT_EMAIL=24f20078@ds.study.iitm.ac.in
STUDENT_SECRET=your_secret_here
OPENAI_API_KEY=sk-your-actual-api-key
```

### 4. Start the Server
```bash
./venv/Scripts/python app.py
```

Server will start on: `http://localhost:8000`

### 5. Test the Server (in a new terminal)
```bash
# Health check
curl http://localhost:8000/health

# API info
curl http://localhost:8000/    
   
# Test quiz endpoint
curl -X POST http://localhost:8000/quiz \
  -H "Content-Type: application/json" \
  -d '{"email":"24f20078","secret":"your_secret","url":"https://tds-llm-analysis.s-anand.net/demo"}'
```

## Quick Commands

```bash
# Run everything at once:
source venv/Scripts/activate && ./venv/Scripts/python app.py
```

## Stop the Server
Press `Ctrl + C` in the terminal running the app

## Troubleshooting

**ModuleNotFoundError**: Run step 2 again to install dependencies

**Configuration error**: Update `.env` file with your actual credentials

**Port already in use**: Change `PORT=8000` in `.env` to another port like `8001`
