from fastapi import FastAPI
from backend.app.routes import agent, settings

app = FastAPI()

app.include_router(agent.router)
app.include_router(settings.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Agentic Employment Infrastructure Backend"}
