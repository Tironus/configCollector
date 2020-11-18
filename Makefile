install:
	pip3 install --upgrade pip && \
	pip3 install -r requirements.txt && \
	export APP_DIR=$(pwd)

lint:
	pylint --disable=C,R,E1120,E0401 collectorGenerator.py
	pylint --disable=C,R,E1120,E0401 configCollector.py
	pylint --disable=C,R,E1120,E0401,W0612 deviceCommander.py

all:
	install lint