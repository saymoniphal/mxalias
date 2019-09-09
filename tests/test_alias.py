import os
import tempfile
import pytest
from hypothesis import given
import hypothesis.strategies as st

from mxalias.alias import app
from mxalias.alias import sqldb
import mxalias.alias as alias

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.testing = True
    client = app.test_client()

    with app.app_context():
        sqldb.create_all()
    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_empty_db(client):
    rv = client.get('/', follow_redirects=True)
    assert rv.data


@given(alias=st.text(), forw_addr=st.text())
def test_add_alias(client, alias, forw_addr):
    res = client.post('/v1/alias/new', data=dict(alias_addr=alias, email1=forw_addr), follow_redirects=True)
    rv = client.get('/v1/alias/{}/json'.format(alias))
    print(rv)
    assert rv == [{'alias': alias, 'forw_addr': forw_addr}], 'Test add alias'
