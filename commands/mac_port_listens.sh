# mac command to see what processes are listening on which ports
# takes a few minutes

# see https://stackoverflow.com/a/4421674 for more explanatory details

sudo lsof -i -P | grep LISTEN | grep :$PORT

