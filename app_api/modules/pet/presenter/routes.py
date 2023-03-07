from starlette.routing import Route

from app_api.modules.pet.presenter.pet_create_presenter import create_or_update, photo_create
from app_api.modules.pet.presenter.pet_timeline_presenter import timeline

routes = [
    Route(path='/pet', endpoint=create_or_update, methods=['POST', 'PATCH', ], ),
    Route(path='/pet/photo', endpoint=photo_create, methods=['POST', ], ),
    Route(path='/pet/timeline', endpoint=timeline, methods=['GET', ], ),
]
