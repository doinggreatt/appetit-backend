from fastapi import APIRouter

from config import SessionDep

router = APIRouter(prefix="/food")

@router.post("")
