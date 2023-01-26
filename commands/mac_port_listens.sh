# mac command to see what processes are listening on which ports
# takes a few minutes

sudo lsof -i -P | grep LISTEN | grep :$PORT

