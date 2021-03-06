import contextlib
import json
import os
import tempfile
import string
import pytest
from hypothesis import given
import hypothesis.strategies as st

from mxalias.alias import app
from mxalias.alias import sqldb
from mxalias import alias


ascii_alphanum = ''.join([ch for ch in string.ascii_letters+string.digits])

def set_up():
    db_fd, temp_file = tempfile.mkstemp(suffix='.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+temp_file
    app.config['TESTING'] = True
    app.testing = True
    client = app.test_client()

    with app.app_context():
        sqldb.create_all()

    return db_fd, temp_file, client

def tear_down(db_fd, temp_file, client):
    os.close(db_fd)
    os.unlink(temp_file)


@pytest.fixture
def client():
    with nfclient() as cl:
        yield cl


@contextlib.contextmanager
def nfclient():
    db_fd, temp_file, client = set_up()
    yield client
    tear_down(db_fd, temp_file, client)


def _get_list(byte_data):
    # convert byte data (json format) to python object
    data = byte_data.decode()
    return json.loads(data)


def test_empty_db(client):
    rv = client.get('/', follow_redirects=True)
    assert rv.data


def test_add_empty_alias(client):
    res = client.post('/v1/alias/new', data=dict(alias_addr='', email1=''))
    assert res.status_code == 400, 'Add empty alias: return code not 400 (Bad Request)'


def test_api_alias(client):
    obj = alias.Mxalias(alias='abc', forw_addr='abc1')
    sqldb.session.add(obj)
    sqldb.session.commit()
    res = client.get('/api/v1/alias/%s' %('abc'))
    assert res.status_code == 200
    ret_obj = _get_list(res.data)
    assert ret_obj == [{'alias': 'abc', 'forw_addr': 'abc1'}]


@given(alias_addr=st.text(min_size=1, alphabet=ascii_alphanum),
       forw_addr=st.text(min_size=1, alphabet=ascii_alphanum))
def test_add_alias(alias_addr, forw_addr):
    with nfclient() as client:
        res = client.post('/v1/alias/new',
                          data={'post_action': 'save_alias',
                                'alias': alias_addr,
                                'email1': forw_addr,
                                'forw_addr_cnt': '1'},
                          follow_redirects=True)
        assert res.status_code == 200, 'Add alias: return code not 200'
        res = client.get('/api/v1/alias/%s' % (alias_addr,))
        assert res.status_code == 200, 'Add alias: failed to get alias, return code not 200'

        ret_obj = _get_list(res.data)
        assert ret_obj == [{'alias': alias_addr, 'forw_addr': forw_addr}], 'Add alias: incorrect record'
