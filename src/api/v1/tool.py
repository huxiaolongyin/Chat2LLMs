from fastapi import APIRouter, Body
from schemas.base import BaseDataResponse, ErrorResponse
from core.functions.common import get_current_weather
from core.functions.robot import go_to_place

router = APIRouter()


@router.post(
    "/weather",
    tags=["Tool"],
    operation_id="get_current_weather",
    summary="获取当前天气信息",
    response_model=BaseDataResponse,
)
async def get_current_weather_api(city_name: str = Body(..., embed=True)):
    """获取当前天气信息"""
    res = get_current_weather(city_name)
    if res == "获取天气信息失败":
        return ErrorResponse(detail=res)
    return BaseDataResponse(data=res)


@router.post(
    "/go_to_place",
    tags=["Tool"],
    operation_id="go_to_place",
    summary="前往某个地方",
    response_model=BaseDataResponse,
)
async def go_to_place_api(place: str = Body(..., embed=True)):
    res = go_to_place(place)
    if not place:
        return ErrorResponse(detail="抱歉，没有识别到地点，请再说一下")
    return BaseDataResponse(data=res)
