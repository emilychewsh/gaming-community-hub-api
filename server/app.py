from flask import make_response
from config import app, api
from models import User, Game, Favourite, Review, ReviewLike
from controllers.user_controller import UserSignup, UserLogin, UserLogout, CheckSession



@app.route('/')
def index():
    return make_response({"message": "Welcome to the Gaming Community Hub!"}, 200 )

api.add_resource(UserSignup, '/user/signup')
api.add_resource(UserLogin, '/user/login')
api.add_resource(UserLogout, '/user/logout')
api.add_resource(CheckSession, '/user/checksession')

if __name__ == "__main__":
    app.run(port=4000, debug=True)