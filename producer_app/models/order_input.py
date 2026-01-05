from pydantic import BaseModel, Field, field_validator


class CreateOrderInput(BaseModel):
    orderId: str = Field(min_length=1)
    itemCount: int = Field(gt=0, le=9999, description="Number of items to generate")

    @field_validator("orderId")
    @classmethod
    def order_id_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("orderId cannot be empty or whitespace")
        return v
