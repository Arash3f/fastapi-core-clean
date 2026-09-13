from dataclasses import dataclass
from uuid import UUID


@dataclass
class LoginDTO:
    username: str
    password: str
    device_id: str


@dataclass
class RegisterDTO:
    name: str
    username: str
    password: str
    device_id: str


@dataclass
class RefreshTokenDTO:
    refresh_token: str
    device_id: str


@dataclass
class LogoutDTO:
    user_id: UUID


@dataclass
class ChangeMyPasswordDTO:
    user_id: UUID
    current_password: str
    new_password: str


@dataclass
class ChangePasswordDTO:
    user_id: UUID
    new_password: str


@dataclass
class TokenResponseDTO:
    access_token: str
    refresh_token: str


@dataclass
class SuccessDTO:
    success: bool = True
