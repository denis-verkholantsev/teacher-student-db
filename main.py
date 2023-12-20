from db.models import Base
from sqlalchemy import create_engine

URL = "postgresql://postgres:1313@localhost:8765/postgres"
engine = create_engine(URL, echo=True)
Base.metadata.create_all(bind=engine)


