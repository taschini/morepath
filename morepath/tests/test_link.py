from morepath.link import path
from morepath.interfaces import IRoot, IPath
from morepath.request import Request
from werkzeug.test import EnvironBuilder
from morepath.app import global_app, root_path
from comparch import Lookup

def get_request(*args, **kw):
    return Request(EnvironBuilder(*args, **kw).get_environ())

class Root(IRoot):
    pass

def test_root_path():
    request = get_request()
    request.lookup = lookup = Lookup(global_app)
    root = Root()
    assert path(request, root) == ''
    assert IPath.component(request, root, lookup=lookup) is root_path
