import pymongo
from datetime import datetime
from hashlib import md5
from config import DB_PASS, DB_USER

CON = pymongo.Connection()
db = CON["digest_http_api"]
db.authenticate(DB_USER, DB_PASS)


def _generate_user_ha1_pw(username, realm, password):
	'''
	Generates password for a user to be stored in database. The
	particular way in which this password is structured and hashed is 
	specific for HTTP Digest authentication. This is an internat function
	used for creating new users.

	Args:
		username: username of user
		realm: realm used in HTTP Digest auth, by default the realm is 
			   'Authentication Required'
		password: plain-text user password

	Returns:
		Hashed 'password' combination to be stored in the database
	'''
	a1 = username + ":" + realm + ":" + password
	return md5(a1.encode("utf-8")).hexdigest()


def _insert_user(username, password):
	'''
	Inserts the specified user into database. Meant to be an internal function
	only to create users during setup.

	Args:
		username: username of user 
		password: plain-text password of user 
	'''
	ha1 = _generate_user_ha1_pw(username, "Authentication Required", password)
	db.users.insert({"username": username, "ha1": ha1, "secrets": {} })


def get_user_ha1_password(username):
	'''
	Retrieves hash password combination stored for the particular user. Used 
	to authenticate via Flask_HTTPAuth library.

	Args:
		username: username of user 

	Returns:
		Hashed password combination if one exists for specified user.
	'''
	trans = db.users.find_one({"username": username})
	if trans:
		return trans["ha1"]
	return None


def update_secret(username, secret_id, new_content):
	'''
	Updates a specified secret for a user.

	Args:
		username: username of user 
		secret_id: id to be updated
		new_content: new text of secret 

	Returns:
		Returns true on success, false otherwise.
	'''
	secrets = get_all_secrets(username)
	secret_id = str(secret_id)
	if not secrets or secret_id not in secrets:
		return False
	secrets[secret_id] = new_content
	db.users.update({"username": username}, {"$set": {"secrets": secrets}})
	return True


def delete_secret(username, secret_id):
	'''
	Deletes specified secret for a user.

	Args:
		username: username of user 
		secret_id: id of secret to be deleted 

	Returns:
		Returns true on success, false otherwise.
	'''
	secrets = get_all_secrets(username)
	secret_id = str(secret_id)
	if not secrets or secret_id not in secrets:
		return False
	del secrets[secret_id]
	db.users.update({"username": username}, {"$set": {"secrets": secrets}})
	return True

def insert_secret(username, secret):
	'''
	Inserts a new secret for specified user.

	Args:
		username: username of user 
		secret: string secret to be added 

	Returns:
		Returns true on success, false otherwise.
	'''
	secrets = get_all_secrets(username)
	if secrets == False:
		return False
	if not secrets:
		secrets = {"0": secret}
	else:
		max_id = 0
		for key, val in secrets.iteritems():
			if int(key) > max_id:
				max_id = int(key)
		max_id += 1
		max_id = str(max_id)
		secrets[max_id] = secret

	db.users.update({"username": username}, {"$set": {"secrets": secrets}})
	return True

def get_all_secrets(username):
	'''
	Retrieves all secrets for specified user.

	Args:
		username: username of user 

	Returns:
		A dictionary with all secrets, or false if user does not exist.
	'''
	trans = db.users.find_one({"username": username})
	if trans:
		return trans["secrets"]
	return False



_insert_user('test-user', 'pa$$w0rd')
# user = get_user_ha1_password("pawel")
# #print get_user_secret("pawel",1)
# #insert_secret('pawel', 'hahahah3454')
# print get_all_secrets('pawel')
# print update_secret('pawel', 1, 'czesc')
# print update_secret('pawel', 123123123123, 'asdfasdf')
# print delete_secret('pawel',1)
# print delete_secret('pawel',4)
# print get_all_secrets('pawel')