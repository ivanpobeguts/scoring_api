#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime
import logging
import hashlib
import uuid
from optparse import OptionParser
from http.server import HTTPServer, BaseHTTPRequestHandler

from exceptions import ValidationError
from utils import alt_name, check_pairs
from scoring import get_score, get_interests
from store import RedisStore
from constants import *
from fields import *


class RequestMeta(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        fields = []
        for name in dir(cls):
            attr = getattr(cls, name, None)
            if isinstance(attr, Field):
                fields.append(name)
        cls._fields = fields


class BasicRequest(metaclass=RequestMeta):
    def __init__(self, **kwargs):
        self._set_attributes(kwargs)

    def __get__(self, name):
        if name in self._fields:
            return getattr(self, alt_name(name))
        return getattr(self, name)

    def __set__(self, name, value):
        if name in self._fields:
            setattr(self, alt_name(name), value)
        else:
            setattr(self, name, value)

    def _set_attributes(self, kwargs):
        cls = type(self)
        for field in self._fields:
            value = kwargs.get(field)
            prop = getattr(cls, field)
            if not isinstance(prop, Field):
                raise TypeError(f'Cannot set non-property {field}')
            prop.validate(value)
            setattr(self, field, value)


class ClientsInterestsRequest(BasicRequest):
    client_ids = ClientIDsField(required=True)
    date = DateField(required=False, nullable=True)


class OnlineScoreRequest(BasicRequest):
    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    phone = PhoneField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)


class MethodRequest(BasicRequest):
    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=False)

    @property
    def is_admin(self):
        return self.login == ADMIN_LOGIN


def check_auth(request):
    if request.is_admin:
        digest = hashlib.sha512((datetime.datetime.now().strftime("%Y%m%d%H") + ADMIN_SALT).encode()).hexdigest()
    else:
        digest = hashlib.sha512((request.account + request.login + SALT).encode()).hexdigest()
    if digest == request.token:
        return True
    return False


def online_score_handler(method_request, ctx, store):
    try:
        user_info = OnlineScoreRequest(**method_request.arguments)
    except ValidationError as e:
        logging.error(str(e), ctx)
        return str(e), INVALID_REQUEST, ctx
    ctx.update({'has': list(method_request.arguments.keys())})
    if not check_pairs(user_info):
        error_msg = 'One of pairs (phone-email), (first_name-last_name), (gender-birthday) is missed'
        logging.error(str(error_msg), ctx)
        return error_msg, INVALID_REQUEST, ctx
    if method_request.is_admin:
        return {"score": 42}, OK, ctx
    score = get_score(
        store=store,
        phone=user_info.phone,
        email=user_info.email,
        birthday=user_info.birthday,
        gender=user_info.gender,
        first_name=user_info.first_name,
        last_name=user_info.last_name
    )
    return {"score": score}, OK, ctx


def clients_interests_handler(method_request, ctx, store):
    try:
        user_info = ClientsInterestsRequest(**method_request.arguments)
    except ValidationError as e:
        logging.error(str(e), ctx)
        return str(e), INVALID_REQUEST, ctx
    ctx.update({'nclients': len(user_info.client_ids)})
    interests = {cid: get_interests(store, cid) for cid in user_info.client_ids}
    return interests, OK, ctx


def method_handler(request, ctx, store):
    response, code = None, OK
    try:
        method_request = MethodRequest(**request['body'])
    except ValidationError as e:
        logging.error(str(e), ctx)
        return str(e), INVALID_REQUEST, ctx
    if not check_auth(method_request):
        logging.error('Unauthenticated', ctx)
        return response, FORBIDDEN, ctx

    if method_request.method == 'online_score':
        return online_score_handler(method_request, ctx, store)
    if method_request.method == 'clients_interests':
        return clients_interests_handler(method_request, ctx, store)
    else:
        logging.error('Service not found', ctx)
        return response, NOT_FOUND, ctx


class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "method": method_handler
    }
    store = RedisStore()

    def get_request_id(self, headers):
        return headers.get('HTTP_X_REQUEST_ID', uuid.uuid4().hex)

    def do_POST(self):
        response, code = {}, OK
        context = {"request_id": self.get_request_id(self.headers)}
        request = None
        try:
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            request = json.loads(data_string)
        except:
            code = BAD_REQUEST

        if request:
            path = self.path.strip("/")
            logging.info("%s: %s %s" % (self.path, data_string, context["request_id"]))
            if path in self.router:
                try:
                    response, code, context = self.router[path]({"body": request, "headers": self.headers}, context,
                                                                self.store)
                except Exception as e:
                    logging.exception("Unexpected error: %s" % e)
                    code = INTERNAL_ERROR
            else:
                code = NOT_FOUND

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if code not in ERRORS:
            r = {"response": response, "code": code}
        else:
            r = {"error": response or ERRORS.get(code, "Unknown Error"), "code": code}
        context.update(r)
        logging.info(context)
        self.wfile.write(json.dumps(r).encode())
        return


if __name__ == "__main__":
    op = OptionParser()
    op.add_option("-p", "--port", action="store", type=int, default=8080)
    op.add_option("-l", "--log", action="store", default=None)
    (opts, args) = op.parse_args()
    logging.basicConfig(filename=opts.log, level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    server = HTTPServer(("localhost", opts.port), MainHTTPHandler)
    logging.info("Starting server at %s" % opts.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
