all: clean setup dist build

setup:
	python3 -m venv .
	bin/pip3 install --upgrade pip setuptools wheel

build:
	bin/python3 setup.py build
	# bin/python3 setup.py build_scripts

install:
	bin/python3 setup.py install
	# bin/python3 setup.py install_lib --skip-build --no-compile
	# bin/python3 setup.py install_scripts --skip-build

dist:
	bin/pip3 wheel -w dist/wheels .
	# bin/python3 setup.py bdist
	# bin/python3 setup.py bdist_egg --exclude-source-files --skip-build
	# bin/python3 setup.py bdist_wheel --skip-build

develop: develop-install develop-req

clean:
	rm -rf {lib,bin,include,build,dist}/
	rm -rf clickonce_download.egg-info/
