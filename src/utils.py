from fastapi import HTTPException
from . import models


##### Utility Functions #####

def get_all_users(db, skip, limit):
	return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(id, db):
	user_query = db.query(models.User).filter(models.User.id == id)
	return check_if_user_exists(user_query)


def get_user_by_email(email, db):
	user_query = db.query(models.User).filter(models.User.email_address == email)
	return check_if_user_exists(user_query)


def create_new_user(db, user):
	db_user = models.User(
		last_name = user.last_name.capitalize(),
		first_name = user.first_name.capitalize(),
		email_address = user.email_address,
		birth_date = user.birth_date
	)

	return commit_to_database(db, db_user)


def update_existing_user(id, db, user):
	db_user = get_user_by_id(id, db).first()

	db_user.last_name = user.last_name.capitalize()
	db_user.first_name = user.first_name.capitalize()
	db_user.email_address = user.email_address
	db_user.birth_date = user.birth_date

	return commit_to_database(db, db_user)


def check_if_user_exists(query):
	if query.first() is None:
		raise HTTPException(status_code=404, detail="User not found in database.")
	
	return query


def commit_to_database(db, obj):
	db.add(obj)
	db.commit()
	db.refresh(obj)

	return obj
