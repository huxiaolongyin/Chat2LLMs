from fastapi import APIRouter
from config import CONFIG
from models.base import BaseEmptyResponse, BaseDataResponse

router = APIRouter()


@router.get(
    "/status",
    tags=["Manage"],
    operation_id="status",
    summary="Status",
    response_model=BaseDataResponse,
)
async def api_health_check():
    return BaseDataResponse(data={"version": CONFIG.VERSION})


# @router.get(
#     "/version",
#     tags=["Manage"],
#     operation_id="get_version",
#     summary="Get application version",
#     response_model=BaseDataResponse,
# )
# async def api_version():
#     return BaseDataResponse()
