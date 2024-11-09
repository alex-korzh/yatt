from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Auth0Config(BaseModel):
    client_id: str = "L2lsodWxvh2O6nv0NrSM9yj7rQSQFBpQ"
    base_url: str = "https://dev-6q3ehaa3i7va2sxb.eu.auth0.com/oauth/"
    api_id: str = "http://api.local"
    
class OpenAIConfig(BaseModel):
    api_key: str | None = None
    prompt: str = (
        "Generate a creative and engaging text on a random topic. "
        "The text should be between 1500 and 2000 characters long and "
        "cover the topic in enough detail to be interesting and informative. "
        "Use a neutral tone, and avoid any controversial or sensitive topics. "
        "Make sure the content is suitable for all ages and can be used as a typing exercise."
    )

# env names are case-insensitive
class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="yatt_")
    env: Literal["dev", "release"] = "release"
    local_key: str | None = None # ONLY for local ssl testing
    chunk_size: int = 128
    line_limit: int = 45
    openai: OpenAIConfig = OpenAIConfig()
    auth0: Auth0Config = Auth0Config()


config = Config()
