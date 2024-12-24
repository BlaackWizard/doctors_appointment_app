from sqlalchemy import extract, func, select

from src.db.connect import async_session_maker
from src.models.payment import Payment
from src.repos.sqlalchemy import SQLAlchemyRepo


class PaymentRepo(SQLAlchemyRepo):
    model = Payment

    @classmethod
    async def get_monthly_financial_report(cls, year: int):
        async with async_session_maker() as session:
            query = (
                select(
                    extract('month', cls.model.date).label("month"),
                    func.sum(cls.model.amount).label("monthly_income"),
                )
                .filter(extract('year', cls.model.date) == year)
                .group_by(extract('month', cls.model.date))
                .order_by(extract('month', cls.model.date))
            )

            result = await session.execute(query)
            data = [{"month": row[0], "monthly_income": row[1]} for row in result.fetchall()]
            return data
