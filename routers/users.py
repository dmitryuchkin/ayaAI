from threading import settrace_all_threads
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db.models.users import User
from schemas.users import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create", response_model=UserResponse)
async def create_user(
    request: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user = User(
        username=request.username,
        email=request.email,
        password=request.password
    )
    db.add(user)
    await db.flush()
    print(user)
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found"
        )
    return user

@router.patch("/{user_id}", response_model=UserResponse)
async def edit_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found"
        )
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    
    return user

