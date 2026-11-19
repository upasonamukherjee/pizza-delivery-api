from typing import Optional, Literal
from pydantic import BaseModel, field_validator


class SignUpModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "username": "john",
                "email": "john@example.com",
                "password": "mypassword123",
                "is_staff": False,
                "is_active": True
            }
        }
    }


class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int] = None
    quantity: int
    order_status: Optional[str] = "PENDING"
    pizza_size: Literal["SMALL", "MEDIUM", "LARGE", "EXTRA-LARGE"] = "SMALL"
    user_id: Optional[int] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "quantity": 2,
                "pizza_size": "LARGE"
            }
        }
    }


class OrderStatusModel(BaseModel):
    order_status: Literal["PENDING", "IN-TRANSIT", "DELIVERED"] = "PENDING"

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "order_status": "IN-TRANSIT"
            }
        }
    }


class OrderResponse(BaseModel):
    id: int
    quantity: int
    order_status: str
    pizza_size: str
    user_id: Optional[int] = None

    @field_validator("order_status", "pizza_size", mode="before")
    @classmethod
    def choice_to_code(cls, value):
        return getattr(value, "code", value)

    model_config = {"from_attributes": True}