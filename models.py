from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from database import Base
from sqlalchemy.orm import relationship

class questions(Base):
	__tablename__ = "question_store"
	q_id = Column(Integer, primary_key = True, index = True)
	question = Column(String, index = True)
	subject = Column(String, index = True)
	topic = Column(String, index = True)
	difficulty = Column(String, index = True)
	marks = Column(Integer, index = True)