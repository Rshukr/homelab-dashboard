from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.get("/server_metrics")
async def get_metrics():
    return {"msg": "Bonjour"}


@router.get("/container_status")
async def get_container_info():
    return {"msg": "Bonjour-ein"}
