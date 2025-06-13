import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from chatbot import get_response, RESUME_PATH

app = FastAPI(title="Chatbot API")

# ← INSERT HEALTH CHECK HERE
@app.get("/health")
async def health():
    return {"status": "ok"}

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    user_msg = req.message.strip()
    if not user_msg:
        raise HTTPException(400, detail="Empty message")
    bot_reply = get_response(user_msg)
    return ChatResponse(reply=bot_reply)

@app.get("/resume")
async def resume_endpoint():
    if not os.path.isfile(RESUME_PATH):
        raise HTTPException(404, detail="Resume not found")
    return FileResponse(
        path=RESUME_PATH,
        media_type="application/pdf",
        filename="Prajwal_M_D_RESUME.pdf"
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
