from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.db.connect import async_session_maker
from src.models.wallet import Wallet
from src.repos.sqlalchemy import SQLAlchemyRepo


class WalletRepo(SQLAlchemyRepo):
    model = Wallet

    @classmethod
    async def pay_service(cls, wallet_id: int, service_cost: float):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=wallet_id)
            result = await session.execute(query)
            wallet = result.scalar_one_or_none()

            wallet.balance -= service_cost
            session.add(wallet)

            await session.commit()
            return wallet.balance

    @classmethod
    async def top_balance(cls, wallet, amount):
        async with async_session_maker() as session:
            wallet.balance += amount
            session.add(wallet)

            await session.commit()
            return wallet.balance
