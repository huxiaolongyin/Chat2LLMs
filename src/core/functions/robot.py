def go_to_place(place: str) -> str:
    return f"收到命令，我带你去 {place}"


tools = [
    {
        "type": "function",
        "function": {
            "name": "go_to_place",
            "description": "只有当用户明确要求去某个室内或室外场景位置时才使用。驱动机器人到指定地点。",
            "parameters": {
                "type": "object",
                "properties": {
                    "place": {
                        "type": "string",
                        "description": "必须是用户提到的室内或室外的地点",
                    },
                },
                "required": ["place"],
            },
        },
    }
]
