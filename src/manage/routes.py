from fastapi import APIRouter
from config import CONFIG
from models.base import BaseEmptyResponse, BaseDataResponse

router = APIRouter()


@router.get(
    "/health_check",
    tags=["Manage"],
    operation_id="health_check",
    summary="Health check",
    response_model=BaseEmptyResponse,
)
async def api_health_check():
    return {"status": "OK"}


@router.get(
    "/version",
    tags=["Manage"],
    operation_id="get_version",
    summary="Get application version",
    response_model=BaseDataResponse,
)
async def api_version():
    return BaseDataResponse(data={"version": CONFIG.VERSION})
