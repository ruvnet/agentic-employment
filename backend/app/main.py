from fastapi import FastAPI
from backend.app.routes import agent, settings, users  # Import the users router

app = FastAPI()

app.include_router(agent.router)
app.include_router(settings.router)
app.include_router(users.router)  # Include the users router

@app.get("/")
async def root():
    return {"message": "Welcome to the Agentic Employment Infrastructure Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
