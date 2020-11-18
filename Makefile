install:
	pip3 install --upgrade pip && \
	pip3 install -r requirements.txt && \
	export APP_DIR=$(pwd)

lint:
	pylint --disable=R,C,E1120 collectorGenerator.py
	pylint --disable=R,C,E1120 configCollector.py
	pylint --disable=R,C,E1120 deviceCommander.py

all:
	install lint