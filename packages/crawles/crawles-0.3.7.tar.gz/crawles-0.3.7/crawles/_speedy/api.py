from requests import sessions
from .Response import Response


def decorator(func):
    def inner(*args, **kwargs):
        response_ = func(*args, **kwargs)

        response = Response(response_)  # 创建新对象
        response.__dict__.update(response_.__dict__)  # 从原始数据更新到新对象
        return response

    return inner


def request(method, url, **kwargs):
    with sessions.Session() as session:
        return session.request(method=method, url=url, **kwargs)


@decorator
def get(url, params=None, **kwargs):
    return request("get", url, params=params, **kwargs)


@decorator
def options(url, **kwargs):
    return request("options", url, **kwargs)


@decorator
def head(url, **kwargs):
    kwargs.setdefault("allow_redirects", False)
    return request("head", url, **kwargs)


@decorator
def post(url, data=None, json=None, **kwargs):
    return request("post", url, data=data, json=json, **kwargs)


@decorator
def put(url, data=None, **kwargs):
    return request("put", url, data=data, **kwargs)


@decorator
def patch(url, data=None, **kwargs):
    return request("patch", url, data=data, **kwargs)


@decorator
def delete(url, **kwargs):
    return request("delete", url, **kwargs)
