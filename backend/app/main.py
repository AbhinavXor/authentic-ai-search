"""
=========================================================
MODULE: FastAPI Application Entry Point

Project:
Authentic AI Search

Engine:
VRA (Verified Resource Algorithm)

Purpose:
This file starts the FastAPI backend server.

Responsibilities:
- Create FastAPI app
- Register API routers
- Add health check route
- Add VRA test route
- Add CORS middleware for frontend

Author:
Abhinav

Version:
0.3.0
=========================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.db.models import initialize_database

from backend.app.core.config import config
from backend.app.vra.pipeline import VRAPipeline
from backend.app.vra.types import UserQuery
from backend.app.api.chat import router as chat_router
from backend.app.api.feedback import (
    router as feedback_router
)


app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.PROJECT_VERSION,
    description="Verified AI Search backend powered by VRA."
)
initialize_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)
app.include_router(feedback_router)


@app.get("/")
def root() -> dict:
    """
    Root health route.
    """

    return {
        "project": config.PROJECT_NAME,
        "version": config.PROJECT_VERSION,
        "engine": config.VRA_ENGINE_NAME,
        "status": "running"
    }


@app.get("/health")
def health_check() -> dict:
    """
    Health check route.
    """

    return {
        "status": "healthy",
        "message": "Backend is working"
    }


@app.get("/vra/test")
def vra_test() -> dict:
    """
    Temporary VRA test route.
    """

    pipeline = VRAPipeline()

    query = UserQuery(
        query_text="What is the population of India?"
    )

    result = pipeline.process_query(query)

    return {
        "answer": result.answer,
        "trust_score": result.trust_score,
        "sources": [
            {
                "title": source.title,
                "url": source.url,
                "domain": source.domain,
                "source_type": source.source_type,
                "authority_score": source.authority_score,
                "freshness_score": source.freshness_score
            }
            for source in result.sources
        ],
        "evidence_records": result.evidence_records,
        "warning_message": result.warning_message
    }