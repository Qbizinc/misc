# Note: docker and docker compose must be installed to run the quickstart command

python3 -m pip install --upgrade pip wheel setuptools
python3 -m pip install --upgrade acryl-datahub
datahub version # to confirm the installation

# To launch the service

datahub docker quickstart # this may take awhile

# datahub will be running on http://<ip or localhost>:9002

