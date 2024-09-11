from fastapi import APIRouter
from schemas import SytemStatusResponse
from typing import Dict

router = APIRouter()


@router.get(
    "/status",
    tags=["Manage"],
    operation_id="status",
    summary="接口状态、版本及系统健康状况",
    response_model=SytemStatusResponse,
)
async def api_health_check():
    """用于描述接口状态、版本及系统健康状况"""
    status = "SUCCESS"
    health_info: Dict[str, str] = {}

    # todo：增加对数据库的检查
    try:
        health_info["database"] = "SUCCESS"
        health_info["cache"] = "SUCCESS"
    except Exception as e:
        status = "ERROR"
        health_info["error"] = str(e)

    return SytemStatusResponse(status=status, health=health_info)
