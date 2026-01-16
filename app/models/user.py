from pydantic import BaseModel, Field

class UserCreate(BaseModel):
  name: str = Field(..., title="User Name", description="The full name of the user")

class UserRead(BaseModel):
  id: int = Field(..., title="User ID", description="The unique identifier of the user")
  name: str = Field(..., title="User Name", description="The full name of the user")
