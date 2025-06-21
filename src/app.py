from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
from src.routes.instances import router as instances_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Crear la aplicación FastAPI
app = FastAPI(
    title="EC2 Manager API",
    description="""
    API REST para gestión simulada de instancias EC2 usando boto3.
    
    Esta API simula operaciones básicas de gestión de instancias EC2:
    - Listar todas las instancias
    - Obtener información de una instancia específica  
    - Detener instancias
    
    Utiliza datos mock y simula las respuestas de AWS EC2.
    """,
    
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(instances_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador global de excepciones"""
    logger.error(f"Global exception handler caught: {type(exc).__name__}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status_code": 500
        }
    )


@app.get("/", tags=["health"])
async def root():
    """Endpoint de salud de la aplicación"""
    return {
        "message": "EC2 Manager API",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Endpoint detallado de verificación de salud"""
    return {
        "status": "healthy",
        "service": "EC2 Manager API",
        "version": "1.0.0",
        "checks": {
            "api": "ok",
            "mock_data": "ok"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting EC2 Manager API...")
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
