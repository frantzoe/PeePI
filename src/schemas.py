from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
	id: Optional[int]
	last_name: str = Field(min_length=1)
	first_name: str = Field(min_length=1)
	email_address: str = Field(min_length=5)
	birth_date: str = Field(min_length=10, max_length=10)
	
	"""
	@validator("email_address")
	def check_email_address(cls, val):
		if not re.compile(r"^[a-z0-9]+(?:[._][a-z0-9]+)*@(?:\w+\.)+\w{2,3}$", val):
			raise ValueError('Email address is not valid.')
		return val
	"""

	class Config:
		orm_mode = True # Configure Model To Support ORM Object
