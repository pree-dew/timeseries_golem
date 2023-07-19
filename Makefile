build:
	export CPPFLAGS="-I/usr/local/opt/zlib/include:$CPPFLAGS"
	pip3 install python-snappy
	pip3 install wheel
	python3 setup.py bdist_wheel --universal

install: build
	pip3 install dist/*.whl --force-reinstall
	rm -rf dist/
	rm -rf build/

clean: 
	pip3 uninstall ts-golem 

env: 
	python3 -m venv ~/local_golem
	source ~/local_golem/bin/activate
	pip3 install wheel

setup: env install

build-linux:
	export CPPFLAGS="-I/usr/local/opt/zlib/include:$CPPFLAGS"
	apt-get install libsnappy-dev
	pip3 install python-snappy
	pip3 install wheel
	python3 setup.py bdist_wheel --universal