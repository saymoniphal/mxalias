import os
import tempfile
import pytest
from mxalias import alias


@pytest.fixture
def client():
    db_fd, alias.app.config['DATABASE'] = tempfile.mkstemp()
    alias.app.config['TESTING'] = True
    client = alias.app.test_client()

    with alias.app.app_context():
        alias.init_db()
    yield client

    os.close(db_fd)
    os.unlink(alias.app.config['DATABASE'])
