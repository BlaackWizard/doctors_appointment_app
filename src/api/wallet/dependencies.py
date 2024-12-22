from src.repos.payment import PaymentRepo
from src.repos.services import ServiceRepo
from src.repos.user import UserRepo
from src.repos.wallet import WalletRepo
from src.services.payment_service import PaymentService
from src.services.service_service import ServicesService
from src.services.wallet_service import WalletService


def wallet_services():
    return WalletService(user_repo=UserRepo, wallet_repo=WalletRepo)


def payment_services():
    return PaymentService(
        user_repo=UserRepo,
        wallet_repo=WalletRepo,
        payment_repo=PaymentRepo,
        service_repo=ServiceRepo
    )
