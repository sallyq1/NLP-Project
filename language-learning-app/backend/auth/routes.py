from fastapi import APIRouter, HTTPException
from database import supabase
from pydantic import BaseModel
# from models import Profile

router = APIRouter()

# @router.post("/signup")
# async def signup(user: Profile):
#     try:
#         response = supabase.auth.sign_up({
#                 "email": user.email,
#     })
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# @router.post("/login")
# async def login(user: Profile):
#     try:
#         response = supabase.auth.sign_in_with_password({
#             "email": user.email,
#         })
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
