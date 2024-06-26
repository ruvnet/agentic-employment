from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import agents, analytics, collaboration, governance, settings

app = FastAPI(
    title="AI Agent Management System API",
    description="API for managing AI agents, analytics, collaboration, governance, and system settings.",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(agents.router)
app.include_router(analytics.router)
app.include_router(collaboration.router)
app.include_router(governance.router)
app.include_router(settings.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the AI Agent Management System API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)