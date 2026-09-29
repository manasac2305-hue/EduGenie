from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from qna import answer_question_with_gemini
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Educational Assistant",
    version="1.0.0"
)

# Enable CORS for flexible local & cross-origin communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    """
    Renders the EduGenie main web page interface.
    """
    return FileResponse("templates/index.html")

# 1. Q&A Module Endpoint
@app.get("/qa")
async def answer_question_get(question: str = Query(...)):
    answer = answer_question_with_gemini(question)
    return {"answer": answer}

@app.post("/qa")
async def answer_question_post(request: Request):
    data = await request.json()
    question = data.get("question", "")
    if not question:
        return JSONResponse(content={"error": "Please provide a question."}, status_code=400)
    answer = answer_question_with_gemini(question)
    return {"answer": answer}

# 2. Concept Explanation Module Endpoint
@app.post("/explain")
async def explain_api(request: Request):
    data = await request.json()
    topic = data.get("topic")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation}

@app.get("/explain")
async def explain_api_get(topic: str = Query(...)):
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation}

# 3. Summarization Module Endpoint
@app.post("/summarize")
async def summarize_api(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
    summary = summarize_text(text)
    return {"summary": summary}

# 4. Quiz Generation Module Endpoint
@app.post("/quiz")
async def quiz_api(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
    quiz = generate_quiz(text)
    return JSONResponse(content={"quiz": quiz})

# 5. Learning Recommendations Module Endpoint
@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str = Query(...)):
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
