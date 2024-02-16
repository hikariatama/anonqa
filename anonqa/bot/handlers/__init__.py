from aiogram import Router


def get_router() -> Router:
    from .admin import get_admin_router
    from .user import get_user_router

    router = Router()

    router.include_router(get_user_router())
    router.include_router(get_admin_router())

    return router
