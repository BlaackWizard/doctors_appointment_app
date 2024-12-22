from typing import Annotated

from fastapi import APIRouter, Depends

from src.services.auth_service import get_current_user
from src.services.wallet_service import WalletService
from .dependencies import wallet_services, payment_services
from ...schemas.payment import SPaymentRequest
from ...schemas.wallet import SWalletRequest
from ...services.payment_service import PaymentService

router = APIRouter(prefix='/wallet', tags=['Кошелек'])


@router.post('/create-wallet')
async def create_wallet_endpoint(
    wallet_services: Annotated[WalletService, Depends(wallet_services)],
    user: str = Depends(get_current_user),
):
    return await wallet_services.create_wallet(user_id=user.id)


@router.post("/top-balance")
async def top_balance_endpoint(
    user_data: SWalletRequest,
    wallet_services: Annotated[WalletService, Depends(wallet_services)],
    user: str = Depends(get_current_user),
):
    return await wallet_services.top_balance(user.id, user_data)


@router.post('/check-balance')
async def check_balance_endpoint(
    wallet_services: Annotated[WalletService, Depends(wallet_services)],
    user: str = Depends(get_current_user),
):
    return await wallet_services.check_balance(user.id)


@router.post('/pay-service')
async def pay_service_endpoint(
    payment_services: Annotated[PaymentService, Depends(payment_services)],
    user_data: SPaymentRequest,
    user: str = Depends(get_current_user),
):
    return await payment_services.payment_process(user_id=user.id, payment_data=user_data)


@router.post('/get-receipt')
async def get_receipt_endpoint(
    payment_services: Annotated[PaymentService, Depends(payment_services)],
    payment_id: int,
    user: str = Depends(get_current_user),
):
    return await payment_services.get_receipt(user_id=user.id, payment_id=payment_id)
