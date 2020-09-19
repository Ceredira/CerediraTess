import base64

import flask_login as login

from cerediratess.models.user import User


def init_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @login_manager.request_loader
    def load_user_from_request(request):
        # first, try to login using the api_key url arg
        api_key = request.args.get('api_key')
        if api_key:
            user = User.query.filter_by(api_key=api_key).first()
            if user:
                return user

        # next, try to login using Basic Auth
        auth = request.headers.get('Authorization')

        if auth is None:
            # self.make_error(400, 'CT-401',
            #                 'Authorization header expected. Authorization must be base64(username:password).')
            return None

        auth = auth.replace('Basic ', '', 1)
        decoded_auth = base64.b64decode(auth).decode()
        if ':' not in decoded_auth:
            # self.make_error(400, 'CT-401', message=str(
            #     'Error in Authorization header (expected :). Authorization must be base64(username:password).'))
            return None

        username, password = decoded_auth.split(':', maxsplit=1)
        user = User.query.filter_by(username=username).first()

        if not user:
            # self.make_error(400, 'CT-403', f'User {username} does not exists in service.')
            return None
        if not user.check_password(password):
            # self.make_error(400, 'CT-401', f'Wrong password used. Authorization failed.')
            return None

        return user
