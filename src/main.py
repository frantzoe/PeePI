from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, SessionLocal
from .utils import *

app = FastAPI()

# Create Database If It Doesn't Exist Already
models.Base.metadata.create_all(bind=engine)


# Dependency Function: Open / Close Database Connection
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


"""
# Placeholder Function
@app.get('/')
def read_root():
	return {"Hello": "World"}
"""


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	return get_all_users(db, skip, limit)


@app.get("/users/{id}", response_model=schemas.User)
def read_user(id: int, db: Session = Depends(get_db)):
	return get_user_by_id(id, db).first()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):

	"""
	Before proceding, we should make sure that:

	[]	The user's email address isn't already assigned to another user in the database.
	[]	The string representation of the birth date is in the right format (YYYY/MM/DD).

	**	It's possible to use unique constraints and regex patterns to deal with these two.
	"""

	return create_new_user(db, user)


@app.put("/users/{id}", response_model=schemas.User)
def update_user(id: int, user: schemas.User, db: Session = Depends(get_db)):

	"""
	** Comment in POST operation method above also applies here.
	"""
	
	return update_existing_user(id, db, user)


"""
@app.patch("/users/", response_model=schemas.User)
def modify_user(id: int, user: schemas.User, db: Session = Depends(get_db)):
	pass

	**	Since I already implemented a PUT operation to update a user, I didn't bother implementing this.
"""


@app.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
	get_user_by_id(id, db).delete()
	db.commit()
