import os
import uvicorn

from fastapi import FastAPI, status

from db.db import TESTING
from config.utils import LockedError

from models.users import Base
from api.users import router as users_router


Base.metadata.create_all

app = FastAPI()

app.include_router(users_router)


if __name__ == "__main__":
    if TESTING:
        raise LockedError(
            status_code=status.HTTP_423_LOCKED,
            detail="To run the project, you need to set the TESTING variable to False"
        )

    uvicorn.run(
        app="main:app", reload=True, host=os.environ.get("DOC_HOST", os.environ["HOST"]),
        port=int(os.environ.get("DOC_PORT", os.environ["PORT"]))
    )
