from enum import Enum


class Role(str, Enum):
    ADMIN = "Admin"
    MEMBER = "Member"
