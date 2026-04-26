import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .routes import speech

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Simple token verification - in production, implement proper token validation
    """
    token = credentials.credentials
    if not token:
        logger.warning(f"Invalid authentication attempt: empty token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.debug(f"Token verified: {token[:10]}...")
    return token

app = FastAPI(
    title="IndexTTS API",
    description="REST API for IndexTTS2 speech synthesis with emotion control",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    speech.router, 
    prefix="/v1/audio", 
    tags=["audio"],
    dependencies=[Depends(verify_token)]
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "model": "IndexTTS2"}

@app.on_event("startup")
async def startup_event():
    logger.info("Starting IndexTTS2 API server")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down IndexTTS2 API server")
