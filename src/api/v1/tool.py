from fastapi import APIRouter
from schemas.base import BaseDataResponse, ErrorResponse
from core.functions.weather import get_current_weather

router = APIRouter()


@router.get(
    "/weather",
    tags=["Tool"],
    operation_id="get_current_weather",
    summary="获取当前天气信息",
    response_model=BaseDataResponse,
)
async def get_current_weather_api(city_name: str = None):
    """获取当前天气信息"""
    res = get_current_weather(city_name)
    if res == "获取天气信息失败":
        return ErrorResponse(detail=res)
    return BaseDataResponse(data=res)
