# Click Once Downloader

Downloads files referenced from a click once .application file

## Instructions

Follow these instructions to install the command in your main/global python3 installation.

### Install
* `git clone git@github.com:jmurphyau/clickonce_download.git` (or `git clone https://github.com/jmurphyau/clickonce_download.git`)
* `cd clickonce_download`
* `python3 setup.py install`

### Run
* `clickonce_download.py [CLICKONCE-URL] [DOWNLOAD-PATH]`

## Instructions for Virtual Environment

Follow these instructions to install the command in a python3 virtual environment.

### Install
* `git clone git@github.com:jmurphyau/clickonce_download.git` (or `git clone https://github.com/jmurphyau/clickonce_download.git`)
* `cd clickonce_download`
* `python3 -m venv .`
* `bin/pip3 install --upgrade pip setuptools`
* `bin/python3 setup.py install`

### Run
* `bin/clickonce_download.py [CLICKONCE-URL] [DOWNLOAD-PATH]`
