from sqlalchemy import Column, Integer, String
from .database import Base


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	last_name = Column(String)
	first_name = Column(String)
	email_address = Column(String, index=True)
	birth_date = Column(String)
