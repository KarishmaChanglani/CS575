from backend.command import *

# Location of the database. Default "instance/blobs.db"
DATABASE = "instance/blobs.db"

# Port for hosting the server. Default 5678
PORT = 5678

# Routes for the various command objects. This should be a one-to-one relation so each command has a single route, and
# each route is only assigned one command. The "route" is the url path so "/foo/bar/" resolves to a url like
# "http://example.com/foo/bar/"
COMMAND_ROUTES = {
    GetUserCommand: "/user/",
    GetUserDataCommand: "/user/data/",
    GetMachineCommand: "/machine/",
    GetMachineDataCommand: "/machine/data",
    SaveAuthCommand: "/save/auth/",
    SaveRecordCommand: "/save/data/"
}
