install:
	pip3 install --upgrade pip && \
	pip3 install -r requirements.txt && \
	export APP_DIR=$(pwd)

lint:
	pylint --disable=R,C,E1120,E0401 collectorGenerator.py
	pylint --disable=R,C,E1120,E0401 configCollector.py
	pylint --disable=R,C,E1120,E0401 deviceCommander.py

all:
	install lint