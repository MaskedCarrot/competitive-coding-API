
from codeforces import CodeforcesUserData
from scrape_codechef import CodechefUserData
from flask import request
from flask import Flask , render_template
from flask_restful import Api
from flask_cors import CORS
from contests import get_contests
from constants import *
from scrape_codechef import get_friends_details_basic
from codeforces import get_problems_by_tags


app = Flask(__name__)
CORS(app)
api = Api(app)

@app.errorhandler(404)
def invalid_route(e):
    return render_template('error_404.html')


@app.route('/contests')
def contests():
    try:
        return get_contests()
    except:
        result = {'status': STATE_CLIST_EXCEPTION}
        return result


@app.route('/codeforces/basic_details')
def codeforces_basic_details():
    username = request.args.get('handle')
    codeforces = CodeforcesUserData(username)
    return codeforces.get_basic_details()


@app.route('/codeforces/personal_details')
def codeforces_personal_details():
    username = request.args.get('handle')
    codeforces = CodeforcesUserData(username)
    return codeforces.get_personal_details()


@app.route('/codeforces/past_submissions')
def codeforces_past_submission():
    username = request.args.get('handle')
    codeforces = CodeforcesUserData(username)
    return codeforces.get_past_submissions()


@app.route('/codeforces/contest_details')
def codeforces_contest_details():
    username = request.args.get('handle')
    codeforces = CodeforcesUserData(username)
    return codeforces.get_contest_details()


@app.route('/codeforces/problems_by_tags')
def codeforces_problems_by_tag():
    tags = request.args.get('tags')
    return get_problems_by_tags(tags)


@app.route('/codeforces/friend_details')
def codeforces_friend_details():
    username_list = request.args.get('handles')
    codeforces = CodeforcesUserData(username_list)
    return codeforces.get_friend_details()


@app.route('/codechef/basic_details')
def codechef_basic_details():
    username = request.args.get('handle')
    codechef = CodechefUserData(username)
    return codechef.get_basic_details()


@app.route('/codechef/personal_details')
def codechef_personal_details():
    username = request.args.get('handle')
    codechef = CodechefUserData(username)
    return codechef.get_personal_details()


@app.route('/codechef/contest_details')
def codechef_contest_details():
    username = request.args.get('handle')
    codechef = CodechefUserData(username)
    return codechef.get_contests_details()


@app.route('/codechef/friend_details')
def codechef_friends_details():
    username_list = request.args.get('handles').split(';')
    return get_friends_details_basic(username_list)


@app.route('/')
def welcome():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
