# Server Deployment

I've only deployed this on linux so I'm not sure how this will work on other platforms. Python tends to be rather platform-independent so there shouldn't be too many issues.

## Python Setup
```
$ cd <the directory with the repository, same level as this file>
$ virtualenv venv
$ source venv/bin/activate
$ pip install flask-classy
```
Currently there isn't a configuration file but the port can be changed manually in the run.py script. If the IP address is set to 0.0.0.0 then external devices can access the server through the specified port. If it's set to 127.0.0.1, only your local machine can access the server.

## Configuration
The configuration file is a python file located in `./backend/static`. Comments there should explain sufficiently what is happening. You may need to create a folder called "instance" in the same directory as the run file if using the default configuration.

## Running the server
```
$ source venv/bin/activate
$ python3 run.py
```

## Additional information
Static files can be added to `./backend/static/` and will be available from the url http://localhost:5678/static/ followed by the filename.