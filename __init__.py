from flask import Flask,render_template,request
from flask_httpauth import HTTPDigestAuth
from api_db import *

app=Flask(__name__)
# digest auth stores data in Flask's session object
# hence 'SECRET_KEY' must be set
app.config["SECRET_KEY"] = "simple_api_poc"
auth = HTTPDigestAuth(use_ha1_pw=True)

@auth.get_password
def get_pw(username):
    return get_user_ha1_password(username)

@app.route("/")
def main_page():
    # display main page
    return render_template("index.html")

@app.route("/add/<secret>")
@auth.login_required
def add_secret(secret):
    if insert_secret(auth.username(), secret):
        return "ADD: Secret added!"
    return "ADD: There was an error adding a secret."

@app.route("/view/")
@auth.login_required
def view_secret():
    secrets = get_all_secrets(auth.username())
    if secrets is None or secrets == False or not any(secrets):
        return "VIEW: There are no secrets present."
    out = ""
    for key, value in secrets.iteritems():
        out += "%s: '%s'\n" % (key, value)
    return out

@app.route("/delete/<secret_id>")
@auth.login_required
def delete_secret_point(secret_id):
    if delete_secret(auth.username(), secret_id):
        return "DELETE: Secret deleted!"
    return "DELETE: The specified secret id does not exist!"

@app.route("/update/<secret_id>/<new_secret>")
@auth.login_required
def update_secret_point(secret_id, new_secret):
    if update_secret(auth.username(), secret_id, new_secret):
        return "DELETE: Secret '%s' updated!" % secret_id
    return "DELETE: Secret could not be updated."

if __name__ == "__main__":
    app.run()
