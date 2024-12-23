from dataclasses import dataclass

from src.exceptions.payment.wallet import (NotFoundWalletException,
                                           WalletAlreadyExistsException)
from src.repos.base import BaseRepo
from src.schemas.wallet import SWalletRequest, SWalletResponse


@dataclass
class WalletService:
    wallet_repo: BaseRepo
    user_repo: BaseRepo

    async def top_balance(self, user_id: int, user_data: SWalletRequest):
        wallet = await self.wallet_repo.find_one(user_id=user_id)
        if not wallet:
            raise NotFoundWalletException().message

        balance = await self.wallet_repo.top_balance(amount=user_data.amount, wallet=wallet)

        return SWalletResponse(
            message='Ваш баланс пополнился!',
            balance=balance,
        )

    async def create_wallet(self, user_id: int):
        exists = await self.wallet_repo.find_one(user_id=user_id)

        if exists:
            raise WalletAlreadyExistsException().message

        await self.wallet_repo.add(
            user_id=user_id,
            balance=0.00,
        )
        return 'Создан новый кошелек'

    async def check_balance(self, user_id: int):
        wallet = await self.wallet_repo.find_one(user_id=user_id)
        if not wallet:
            raise NotFoundWalletException().message

        return SWalletResponse(
            message='Ваш баланс:',
            balance=wallet.balance,
        )
