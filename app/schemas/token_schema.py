from pydantic import BaseModel

# 定义 AccessToken 模型
class AccessToken(BaseModel):
    access_token: str  # JWT 令牌
    token_type: str  # 令牌类型，例如 "bearer"