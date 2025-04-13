from app.endpoints.ping import api_router as application_health_router
from app.endpoints.group import api_router as group_router
from app.endpoints.student import api_router as student_router

list_of_routes = [
    application_health_router,
    group_router,
    student_router,
]


__all__ = [
    "list_of_routes",
]
