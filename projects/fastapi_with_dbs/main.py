
"""
Simple script to run the FastAPI application
"""
import uvicorn

def main():
    """Main entry point for the application."""
    uvicorn.run("app:create_app", host="0.0.0.0", port=8000, reload=True, factory=True)

if __name__ == "__main__":
    main()