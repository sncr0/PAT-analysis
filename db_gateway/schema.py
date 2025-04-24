from typing import Optional
from db_gateway.models import Base
from db_gateway.engine import engine


def init_db(drop_existing: Optional[bool] = False) -> None:
    if drop_existing:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
