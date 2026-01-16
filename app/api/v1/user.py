from fastapi import APIRouter, Depends, HTTPException, Path

from app.db.schema import SessionLocal
from app.models.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(tags=["Users"])

def get_user_service() -> UserService:
  return UserService(session=SessionLocal())

@router.get(
  "/users",
  response_model=list[UserRead], 
  summary="List all users",
  description="Retrieve a list of all users currently stored in the database.",
  responses={
    200: {"description": "List of users successfully retrieved"}
  }
)
def get_users(service: UserService = Depends(get_user_service)):
  return service.list_users()

@router.post(
  "/users", 
  response_model=UserRead,
  status_code=201,
  summary="Create a new user",
  description="Create a new user in the database with the given name.",
  responses={
    201: {"description": "User successfully created"},
  }
)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
  try:
    created_user = service.create_user(user.name)
    return created_user
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))

@router.get(
  "/users/{user_id}", 
  response_model=UserRead,
  summary="Retrieve a user by ID",
  description="Get detailed information about a specific user by their unique ID.",
  responses={
    200: {"description": "User successfully retrieved"},
    404: {"description": "User not found"}
  }
)
def get_user(
  user_id: int = Path(..., title="User ID", description="The unique identifier of the user"),
  service: UserService = Depends(get_user_service)
):
  user = service.get_user(user_id)
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  return user

@router.put(
  "/users/{user_id}", 
  response_model=UserRead,
  summary="Update a user by ID",
  description="Update the name of an existing user identified by their unique ID.",
  responses={
    200: {"description": "User successfully updated"},
    404: {"description": "User not found"}
  }
)
def update_user(
  user_id: int = Path(..., title="User ID", description="The unique identifier of the user"), 
  user: UserCreate = ...,
  service: UserService = Depends(get_user_service)
):
  updated = service.update_user(user_id, user.name)
  if not updated:
    raise HTTPException(status_code=404, detail="User not found")
  return updated

@router.delete(
  "/users/{user_id}",
  summary="Delete a user by ID",
  description="Delete an existing user identified by their unique ID.",
  responses={
    200: {"description": "User successfully deleted"},
    404: {"description": "User not found"}
  }
)
def delete_user(
  user_id: int = Path(..., title="User ID", description="The unique identifier of the user"), 
  service: UserService = Depends(get_user_service)
):
  success = service.delete_user(user_id)
  if not success:
    raise HTTPException(status_code=404, detail="User not found")
  return {success: True}
