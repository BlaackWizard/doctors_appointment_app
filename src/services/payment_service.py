from dataclasses import dataclass

from src.exceptions.auth.user import NotFoundUserException
from src.exceptions.payment.payment import NotHaveEnoughMoneyException, NotFoundPaymentException, \
    ThisIsNotYourReceiptException
from src.exceptions.payment.service import NotFoundServiceException
from src.exceptions.payment.wallet import NotFoundWalletException
from src.repos.base import BaseRepo
from src.schemas.payment import SPaymentRequest, SPaymentResponse
from src.utils.generate_qr_code import generate_receipt
from fastapi.responses import StreamingResponse


@dataclass
class PaymentService:
    payment_repo: BaseRepo
    service_repo: BaseRepo
    user_repo: BaseRepo
    wallet_repo: BaseRepo

    async def payment_process(self, user_id: int, payment_data: SPaymentRequest):

        if payment_data.payment_method != 'Через карту':
            return 'Оплатите наличными и администратор поставит галочку что вы оплатили'

        patient = await self.user_repo.find_one(id=user_id, role='patient')
        service = await self.service_repo.find_one(id=payment_data.service_id)

        if not patient:
            raise NotFoundUserException().message

        if not service:
            raise NotFoundServiceException().message

        wallet = await self.wallet_repo.find_one(user_id=user_id)
        if not wallet:
            raise NotFoundWalletException().message

        if wallet.balance < service.cost:
            raise NotHaveEnoughMoneyException().message

        await self.wallet_repo.pay_service(wallet_id=wallet.id, service_cost=service.cost)

        await self.payment_repo.add(
            patient_id=user_id,
            service_id=payment_data.service_id,
            amount=service.cost,
            is_paid=True
        )
        payment = await self.payment_repo.find_one(
            patient_id=user_id,
            service_id=payment_data.service_id,
            amount=service.cost,
            is_paid=True
        )
        return await self.get_receipt(user_id=user_id, payment_id=payment.id)

    async def get_receipt(self, user_id: int, payment_id: int):
        payment = await self.payment_repo.find_by_id(payment_id)
        if not payment:
            raise NotFoundPaymentException().message

        patient = await self.user_repo.find_by_id(payment.patient_id)
        service = await self.service_repo.find_by_id(payment.service_id)

        if user_id != patient.id:
            raise ThisIsNotYourReceiptException().message

        receipt = generate_receipt(payment=payment, patient=patient, service=service, requisites=service.requisites)
        return StreamingResponse(receipt, media_type="image/png")
