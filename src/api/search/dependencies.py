from src.repos.medical_card import VisitsRepo, MedicalCardRepo
from src.repos.user import UserRepo
from src.services.search import SearchService


def search_service():
    return SearchService(user_repo=UserRepo,
                         visits_repo=VisitsRepo,
                         medical_card_repo=MedicalCardRepo)
