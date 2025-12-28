"""Application entry point and composition root."""

from fastapi import FastAPI
from api.routes import router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    This is the composition root where all dependencies are wired together.
    """
    app = FastAPI(
        title="Airline Catalog API",
        description="A microservice for managing airline catalog data",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Register routers
    app.include_router(router)
    
    @app.get("/health")
    def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}
    
    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
