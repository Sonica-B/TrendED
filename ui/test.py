import base64
from dataclasses import dataclass
from typing import override
from uuid import uuid4
import webauthn
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie

from webauthn.helpers import options_to_json, parse_attestation_object, parse_authentication_credential_json, parse_registration_credential_json
from webauthn.helpers.structs import AttestationConveyancePreference, PublicKeyCredentialDescriptor

@dataclass
class User:
    id: str
    name: str
    username: str
    sessions: list[str]
    # for webauthn
    crediential_id: str
    public_key: str
    sign_in_count: int


rp_id = "localhost"

class Database:
    def __init__(self, path: str):
        self.users: list[User] = []
        self.users_by_id: dict[str, User] = {}
        self.users_by_username: dict[str, User] = {}
        self.path = path
        self.active_sessions: dict[str, User] = {}
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
                for user in data['users']:
                    self.add_user(User(**user))
        except Exception:
            pass

    def save(self):
        with open(self.path, 'w') as f:
            json.dump({
                'users': [user.__dict__ for user in self.users]
            }, f)

    def add_user(self, user: User):
        self.users.append(user)
        self.users_by_id[user.id] = user
        self.users_by_username[user.username] = user
        for session in user.sessions:
            self.active_sessions[session] = user

    def remove_user(self, user: User):
        self.users.remove(user)
        del self.users_by_id[user.id]
        del self.users_by_username[user.username]
        for session in user.sessions:
            del self.active_sessions[session]

    def add_user_session(self, user: User, user_session: str):
        if user_session in user.sessions:
            return
        user.sessions.append(user_session)
        self.active_sessions[user_session] = user

    def invalidate_session(self, user_session: str):
        user = self.active_sessions.get(user_session)
        if user is None:
            return
        user.sessions.remove(user_session)
        del self.active_sessions[user_session]

    def get_user_by_id(self, id: str) -> User | None:
        return self.users_by_id.get(id)

    def get_user_by_username(self, username: str) -> User | None:
        return self.users_by_username.get(username)

    def get_user_by_session(self, session: str) -> User | None:
        return self.active_sessions.get(session)



database = Database('database.json')
registration_to_challenge: dict[str, bytes] = {}
authentication_to_challenge: dict[str, bytes] = {}

class Serv(BaseHTTPRequestHandler):
    @override
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:5173')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        BaseHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/user':
            # authenticate cookie
            cookies = SimpleCookie(self.headers.get('Cookie'))
            session = cookies.get('session')
            if session is None:
                self.send_response(401)
                self.end_headers()
                return
            session = session.value
            user = database.get_user_by_session(session)
            if user is None:
                self.send_response(401)
                self.end_headers()
                return
            # return data
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            _ = self.wfile.write(json.dumps({
                "id": user.id,
                "name": user.name,
                "username": user.username,
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/register':
            # read arguments
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            registration_args: dict[str, str] = json.loads(body)

            user = database.get_user_by_username(registration_args['username'])
            if user is not None and len(user.public_key) > 0:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                _ = self.wfile.write(json.dumps({'error': 'User already exists'}).encode())
                return
            new_user: User = user if user is not None else User(
                id=str(uuid4()),
                name=registration_args['name'],
                username=registration_args['username'],
                sessions=[],
                sign_in_count=0,
                crediential_id = "",
                public_key= "",
            )
            database.add_user(new_user)
            database.save()
            # create credential
            options = webauthn.generate_registration_options(
                rp_id=rp_id,
                rp_name="Test",
                user_display_name=new_user.name,
                user_name= new_user.username,
            )
            registration_to_challenge[new_user.id] = options.challenge
            # return credential
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            _ = self.wfile.write(json.dumps({
                "id": new_user.id,
                "options": json.loads(options_to_json(options))
            }).encode())

        elif self.path == '/register/verify':
            # read arguments
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            json_obj = json.loads(body)
            id: str = json_obj["id"]
            challenge = registration_to_challenge.get(id)
            user = database.get_user_by_id(id)
            if challenge is None or user is None:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                _ = self.wfile.write(json.dumps({'error': 'Invalid session'}).encode())
                return
            # verify credential
            try:
                resp = webauthn.verify_registration_response(
                    credential=json_obj["resp"],
                    expected_rp_id=rp_id,
                    expected_challenge=challenge,
                    expected_origin="http://localhost:5173",
                )
                user.crediential_id = base64.b64encode(resp.credential_id).decode()
                user.public_key = base64.b64encode(resp.credential_public_key).decode()
                session = str(uuid4())
                database.add_user_session(user, session)
                database.save()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                _ = self.wfile.write(json.dumps({
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "username": user.username,
                     },
                    "session": session
                }).encode())
            except Exception as e:
                # return failure
                self.send_response(400)
                self.headers['Content-type'] = 'application/json'
                self.end_headers()
                _ = self.wfile.write(json.dumps({'error': str(e)}).encode())
        elif self.path == '/authenticate':
            # read arguments
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            auth_args: dict[str, str] = json.loads(body)

            user = database.get_user_by_username(auth_args['username'])
            if user is None:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                _ = self.wfile.write(json.dumps({'error': 'User not found'}).encode())
                return
            options = webauthn.generate_authentication_options(
                rp_id=rp_id,
                allow_credentials = [PublicKeyCredentialDescriptor(base64.b64decode(user.crediential_id))]
            )
            authentication_to_challenge[user.id] = options.challenge
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            _ = self.wfile.write(json.dumps({
                "id": user.id,
                "options": json.loads(options_to_json(options))
            }).encode())

        elif self.path == '/authenticate/verify':
            # read arguments
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            json_obj = json.loads(body)
            id: str = json_obj["id"]
            challenge = authentication_to_challenge.get(id)
            user = database.get_user_by_id(id)
            if challenge is None or user is None:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                _ = self.wfile.write(json.dumps({'error': 'Invalid session'}).encode())
                return
            # verify credential
            try:
                resp = webauthn.verify_authentication_response(
                    credential=json_obj["resp"],
                    expected_challenge=challenge,
                    expected_rp_id=rp_id,
                    expected_origin="http://localhost:5173",
                    credential_public_key=base64.b64decode(user.public_key),
                    credential_current_sign_count=user.sign_in_count,
                )
                session = str(uuid4())
                user.sign_in_count = resp.new_sign_count
                database.add_user_session(user, session)
                database.save()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                _ = self.wfile.write(json.dumps({
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "username": user.username,
                     },
                    "session": session
                }).encode())
            except Exception as e:
                # return failure
                self.send_response(400)
                self.headers['Content-type'] = 'application/json'
                self.end_headers()
                _ = self.wfile.write(json.dumps({'error': str(e)}).encode())

        elif self.path == "/logout":
            # authenticate cookie
            cookies = SimpleCookie(self.headers.get('Cookie'))
            session = cookies.get('session')
            if session is None:
                self.send_response(401)
                self.end_headers()
                return
            session = session.value
            user = database.get_user_by_session(session)
            if user is None:
                self.send_response(401)
                self.end_headers()
                return
            database.invalidate_session(session)
            database.save()

        else:
            self.send_response(404)
            self.end_headers()


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), Serv)
    print('Starting server')
    server.serve_forever()


