import base64
import json
from typing import Any
from uuid import uuid4

import webauthn
from fastapi import APIRouter, Cookie
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from webauthn.helpers.structs import PublicKeyCredentialDescriptor


class UserResponse(BaseModel):
    id: str
    name: str
    username: str


class User(UserResponse):
    sessions: list[str]
    # for webauthn
    crediential_id: str
    public_key: str
    sign_in_count: int


rp_id = "localhost"
expected_origin = "http://localhost:5173"


class Database:
    def __init__(self, path: str):
        self.users: list[User] = []
        self.users_by_id: dict[str, User] = {}
        self.users_by_username: dict[str, User] = {}
        self.path = path
        self.active_sessions: dict[str, User] = {}
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
                for user in data["users"]:
                    self.add_user(User(**user))
        except Exception:
            pass

    def save(self):
        with open(self.path, "w") as f:
            json.dump({"users": [user.__dict__ for user in self.users]}, f)

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


database = Database("database.json")
registration_to_challenge: dict[str, bytes] = {}
authentication_to_challenge: dict[str, bytes] = {}


router = APIRouter()


# check session cookie
@router.get("/user")
async def get_user(session: str = Cookie(None)):
    user = database.get_user_by_session(session)
    if user is None:
        return JSONResponse(
            content=jsonable_encoder({"error": "Invalid session"}), status_code=401
        )
    return JSONResponse(content=jsonable_encoder(UserResponse(**user.__dict__)))


class RegisterArgs(BaseModel):
    name: str
    username: str


@router.post("/register")
async def register(userargs: RegisterArgs):
    print(userargs)
    user = database.get_user_by_username(userargs.username)
    if user is not None and len(user.public_key) > 0:
        return JSONResponse(
            content=jsonable_encoder({"error": "User already exists"}), status_code=400
        )
    if user is not None:
        new_user = user
    else:
        new_user = User(
            id=str(uuid4()),
            name=userargs.name,
            username=userargs.username,
            sessions=[],
            sign_in_count=0,
            crediential_id="",
            public_key="",
        )
        database.add_user(new_user)
        database.save()
    options = webauthn.generate_registration_options(
        rp_id=rp_id,
        rp_name="Test",
        user_display_name=new_user.name,
        user_name=new_user.username,
    )
    registration_to_challenge[new_user.id] = options.challenge
    return JSONResponse(
        content=jsonable_encoder(
            {
                "id": new_user.id,
                "options": json.loads(webauthn.options_to_json(options)),
            }
        )
    )


class VerifyArgs(BaseModel):
    id: str
    resp: dict[Any, Any]


@router.post("/register_verify")
async def register_verify(verifyargs: VerifyArgs):
    challenge = registration_to_challenge.get(verifyargs.id)
    user = database.get_user_by_id(verifyargs.id)
    if challenge is None or user is None:
        return JSONResponse(
            content=jsonable_encoder({"error": "Invalid session"}), status_code=400
        )
    try:
        resp = webauthn.verify_registration_response(
            credential=verifyargs.resp,
            expected_rp_id=rp_id,
            expected_challenge=challenge,
            expected_origin=expected_origin,
        )
        user.crediential_id = base64.b64encode(resp.credential_id).decode()
        user.public_key = base64.b64encode(resp.credential_public_key).decode()
        session = str(uuid4())
        database.add_user_session(user, session)
        database.save()
        return JSONResponse(
            content=jsonable_encoder(
                {
                    "user": UserResponse(**user.__dict__),
                    "session": session,
                }
            )
        )
    except Exception as e:
        return JSONResponse(
            content=jsonable_encoder({"error": str(e)}), status_code=400
        )


class AuthenticateArgs(BaseModel):
    username: str


@router.post("/login")
async def login(authargs: AuthenticateArgs):
    user = database.get_user_by_username(authargs.username)
    if user is None:
        return JSONResponse(
            content=jsonable_encoder({"error": "User not found"}), status_code=400
        )
    options = webauthn.generate_authentication_options(
        rp_id=rp_id,
        allow_credentials=[
            PublicKeyCredentialDescriptor(base64.b64decode(user.crediential_id))
        ],
    )
    authentication_to_challenge[user.id] = options.challenge
    return JSONResponse(
        content=jsonable_encoder(
            {"id": user.id, "options": json.loads(webauthn.options_to_json(options))}
        )
    )


class AuthenticateVerifyArgs(BaseModel):
    id: str
    resp: dict[Any, Any]


@router.post("/login_verify")
async def login_verify(authverifyargs: AuthenticateVerifyArgs):
    challenge = authentication_to_challenge.get(authverifyargs.id)
    user = database.get_user_by_id(authverifyargs.id)
    if challenge is None or user is None:
        return JSONResponse(content={"error": "Invalid session"}, status_code=400)
    try:
        resp = webauthn.verify_authentication_response(
            credential=authverifyargs.resp,
            expected_challenge=challenge,
            expected_rp_id=rp_id,
            expected_origin=expected_origin,
            credential_public_key=base64.b64decode(user.public_key),
            credential_current_sign_count=user.sign_in_count,
        )
        session = str(uuid4())
        user.sign_in_count = resp.new_sign_count
        database.add_user_session(user, session)
        database.save()
        return JSONResponse(
            content=jsonable_encoder(
                {
                    "user": jsonable_encoder(UserResponse(**user.__dict__)),
                    "session": session,
                }
            )
        )
    except Exception as e:
        return JSONResponse(
            content=jsonable_encoder({"error": str(e)}), status_code=400
        )
