import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app="src.core.server:app",
        reload=True,
        workers=1,
        host="0.0.0.0",
    )
