from fastapi import APIRouter, Body, Depends

from forms import UserLoginForm
from models import connect_db

router = APIRouter()


@router.post('/login', name='user:login')
def index(user_form: UserLoginForm = Body(..., embed=True), database=Depends(connect_db)):
    return {'status': 'OK'}
