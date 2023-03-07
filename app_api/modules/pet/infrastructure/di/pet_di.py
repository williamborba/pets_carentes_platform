from kink import di

from app_api.modules.pet.infrastructure.repositorys.pet_repository import PetRepository


def pet_di() -> None:
    di[PetRepository] = PetRepository()
