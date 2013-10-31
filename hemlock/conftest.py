import pytest

def pytest_addoption(parser):
    parser.addoption("--server-mysql", action="store", default="localhost",
        help="MySQL Server")
    parser.addoption("--database", action="store", default="hemlock_test",
        help="MySQL DB")
    parser.addoption("--mysql-username", action="store", default="travis",
        help="MySQL Username")
    parser.addoption("--mysql-password", action="store", default="password",
        help="MySQL Password")
    parser.addoption("--couchbase-server", action="store", default="localhost",
        help="Couchbase Server")
    parser.addoption("--couchbase-bucket", action="store", default="hemlock_test",
        help="Couchbase Bucket")
    parser.addoption("--couchbase-username", action="store", default="travis",
        help="Couchbase Username")
    parser.addoption("--couchbase-password", action="store", default="password",
        help="Couchbase Password")
    parser.addoption("--elasticsearch-endpoint", action="store", default="localhost",
        help="ElasticSearch Endpoint")
    parser.addoption("--hemlock-debug", action="store_false", default=None,
        help="Debugging Mode")
    parser.addoption("--no-couchbase", action="store_false", default=None,
        help="Don't use Couchbase")
    parser.addoption("--hemlock-version", action="store_true", default=None,
        help="Version")

@pytest.fixture
def server_mysql(request):
    return request.config.getoption("--server-mysql")

@pytest.fixture
def database(request):
    return request.config.getoption("--database")

@pytest.fixture
def mysql_username(request):
    return request.config.getoption("--mysql-username")

@pytest.fixture
def mysql_password(request):
    return request.config.getoption("--mysql-password")

@pytest.fixture
def couchbase_server(request):
    return request.config.getoption("--couchbase-server")

@pytest.fixture
def couchbase_bucket(request):
    return request.config.getoption("--couchbase-bucket")

@pytest.fixture
def couchbase_username(request):
    return request.config.getoption("--couchbase-username")

@pytest.fixture
def couchbase_password(request):
    return request.config.getoption("--couchbase-password")

@pytest.fixture
def elasticsearch_endpoint(request):
    return request.config.getoption("--elasticsearch-endpoint")

@pytest.fixture
def hemlock_debug(request):
    return request.config.getoption("--hemlock-debug")

@pytest.fixture
def no_couchbase(request):
    return request.config.getoption("--no-couchbase")

@pytest.fixture
def hemlock_version(request):
    return request.config.getoption("--hemlock-version")
