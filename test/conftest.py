import pytest
import neo4j
import boltkit.controller
import boltkit.config
import os

# Note that this file MUST be called 'conftest.py' as this name is automatically
# looked for by the pytest driver.

home = "ext/neo4j-community-3.4.6"

bolt_port = 15734
bolt_address = ("localhost", bolt_port)
bolt_listen_address = "%s:%d" % bolt_address
bolt_uri = "bolt://%s" % bolt_listen_address

user = "neo4j"
password = "password"
auth_token = (user, password)

@pytest.fixture
def neo4j_driver():
    if os.path.exists(home):
        # We found a preinstalled boltkit neo4j.  We hope that it was fully
        # installed the first time around!
        realpath = home
    else:
        realpath = boltkit.controller._install(
            edition='community',
            version='3.4.6',
            path="ext"
        )

    controller = boltkit.controller.UnixController(home=realpath, verbosity=0)

    boltkit.config.update(
        realpath,
        {boltkit.config.BOLT_LISTEN_URI_SETTING: bolt_listen_address}
    )

    controller.create_user(user, password)
    controller.set_user_role(user, "admin")

    controller.start()
    boltkit.controller.wait_for_server("localhost", bolt_port, timeout=10)

    driver = neo4j.GraphDatabase.driver(bolt_uri, auth=auth_token)

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    yield driver
    controller.stop()
