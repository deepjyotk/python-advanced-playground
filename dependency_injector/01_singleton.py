"""
Simple Dependency Injection Example with FastAPI

This demonstrates the core concept of dependency injection:
- A FastAPI endpoint depends on a payment service
- The payment service is injected via dependency_injector
- Clean separation of concerns
"""

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from datetime import datetime
import uuid
import asyncio
import random

# Simple Pydantic models
class PaymentRequest(BaseModel):
    amount: float
    description: str

class PaymentResponse(BaseModel):
    payment_id: str
    amount: float
    status: str
    timestamp: datetime

# The service that our endpoint depends on
class PaymentService:
    """Simple payment service - this is what gets injected."""
    
    def __init__(self, api_key: str = "test_key"):
        self.api_key = api_key
        print(f"PaymentService initialized with API key: {api_key}")
    
    async def process_payment(self, amount: float, description: str) -> dict:
        """Mock payment processing with fake network call."""
        payment_id = str(uuid.uuid4())
        
        # Simulate network call to payment processor
        print(f"Making network call to payment processor for {description}...")
        await asyncio.sleep(random.uniform(0.5, 2.0))  # Simulate network latency
        
        # Simulate potential network failure
        if random.random() < 0.1:  # 10% chance of network failure
            raise Exception("Network timeout - payment processor unavailable")
        
        # Simple mock logic
        if amount > 1000:
            status = "failed"
            message = "Amount too high"
        else:
            status = "success"
            message = "Payment processed"
        
        print(f"Payment processed: {amount} for {description} -> {status}")
        
        return {
            "payment_id": payment_id,
            "amount": amount,
            "status": status,
            "timestamp": datetime.now(),
            "message": message
        }

# Dependency Injection Container
class Container(containers.DeclarativeContainer):
    """Container that manages our dependencies."""
    
    # Configure the payment service as a singleton
    payment_service = providers.Singleton(
        PaymentService,
        api_key="sk_test_123456789"
    )

# Create FastAPI app
app = FastAPI(title="Dependency Injection Demo")

# Create and wire the container
container = Container()
container.wire(modules=[__name__])

# Dependency function for FastAPI
def get_payment_service() -> PaymentService:
    """Dependency function that returns the payment service instance."""
    return container.payment_service()

# The endpoint that depends on PaymentService
@app.post("/make_payment", response_model=PaymentResponse)
async def make_payment(
    payment_request: PaymentRequest,
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    This endpoint demonstrates dependency injection:
    - It depends on PaymentService
    - PaymentService is automatically injected by dependency_injector
    - We don't create PaymentService manually in the endpoint
    """
    
    # Use the injected service
    result = await payment_service.process_payment(
        amount=payment_request.amount,
        description=payment_request.description
    )
    
    return PaymentResponse(
        payment_id=result["payment_id"],
        amount=result["amount"],
        status=result["status"],
        timestamp=result["timestamp"]
    )

@app.get("/health")
async def health_check():
    """Simple health check."""
    return {"status": "healthy", "message": "Dependency injection working!"}

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server with dependency injection...")
    print("Visit http://localhost:8000/docs to see the API documentation")
    uvicorn.run(app, host="0.0.0.0", port=8000) 