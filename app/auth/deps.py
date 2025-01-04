from typing import Annotated

from fastapi import Depends

from app.auth.service import get_current_user

user_dependecy = Annotated[dict, Depends(get_current_user)]
