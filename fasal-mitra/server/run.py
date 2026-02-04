"""
Startup script to run the FastAPI server
"""

if __name__ == "__main__":
    import uvicorn
    from app.config import settings
    
    print(f"""
    🌾 FasalMitra API Server
    ========================
    
    Starting server...
    - Environment: {settings.ENVIRONMENT}
    - Host: {settings.HOST}
    - Port: {settings.PORT}
    - Debug: {settings.DEBUG}
    
    API Documentation:
    - Swagger UI: http://{settings.HOST}:{settings.PORT}/docs
    - ReDoc: http://{settings.HOST}:{settings.PORT}/redoc
    
    Press CTRL+C to stop the server
    """)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
