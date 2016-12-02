from backend.command import *

# Location of the database. Default "instance/blobs.db". If this deployment is only for testing, set this value to
# "tests/test.db"
DATABASE = "instance/blobs.db"

# Port for hosting the server. Default 5678
PORT = 5678

# Routes for the various command objects. The "route" is the url path so "/foo/bar/" resolves to a url like
# "http://example.com/foo/bar/". Each route should correspond to a single command, but each command may have multiple
# routes.
COMMAND_ROUTES = {
    "/user/": GetUserCommand,
    "/user/data/": GetUserDataCommand,
    "/user/data/split/": GetUserDataSplitCommand,
    "/machine/": GetMachineCommand,
    "/machine/data/": GetMachineDataCommand,
    "/save/auth/": SaveAuthCommand,
    "/save/data/": SaveRecordCommand
}
