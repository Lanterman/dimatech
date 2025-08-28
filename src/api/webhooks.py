from fastapi import APIRouter, status

from services import webhoosk as webhooks_service
from schemas import webhooks as webhooks_schema, users as users_schema


router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/payments", 
            # response_model=users_schema.UserPaymentSchema, 
            status_code=status.HTTP_200_OK,
            responses={400: {"description": "A user with this email address already exists!"}})
async def payments(form_data: webhooks_schema.ReceivePayment):
    """Create user - endpoint"""

    _process_class = webhooks_service.ProcessPayment()
    payment = await _process_class.process_payment(form_data)
    return payment
