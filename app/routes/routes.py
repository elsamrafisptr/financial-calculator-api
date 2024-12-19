from fastapi import APIRouter
from app.routes.endpoints.calculator import router as calculator_router

routers = APIRouter()
router_list = [calculator_router]

for router in router_list:
    routers.include_router(router)