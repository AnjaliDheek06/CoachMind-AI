from app.database.database import Base, engine
from app.upload_book.model import UploadedBook
from app.lesson.model import Lesson
from app.scenario.model import Scenario
from app.response.model import Response
from app.evaluation.model import Evaluation


def create_tables():
    
    Base.metadata.create_all(bind=engine)