#!/usr/bin/env python3

from xml.etree import ElementTree as ET
from urllib.parse import urljoin
from base64 import b64encode
import os
import posixpath
import sys
import hashlib
import requests
from tqdm import tqdm

xmldsig_algo = {
    'http://www.w3.org/2000/09/xmldsig#sha256': 'sha256',
    'http://www.w3.org/2000/09/xmldsig#sha1': 'sha1'
}

digest_impl = dict(sha1=hashlib.sha1, sha256=hashlib.sha256)

# xpath cheatsheet: https://devhints.io/xpath

class MissingArgumentError(ValueError):
    pass

def fetch_url(url):
    res = requests.get(url)
    return res.text

def fix_url_path(path_):
    return posixpath.join(*path_.split('\\'))

def fix_fs_path(path_):
    return os.path.join(*path_.split('\\'))

def fetch_dot_application(url):
    return fetch_url(url)

def extract_manifest_info(xml):
    tree = ET.fromstring(xml)
    dependency_el = tree.find('.//{urn:schemas-microsoft-com:asm.v2}dependency')
    assembly_el = dependency_el.find('.//{urn:schemas-microsoft-com:asm.v2}dependentAssembly')
    digest_method_el = assembly_el.find('.//{http://www.w3.org/2000/09/xmldsig#}DigestMethod')
    digest_el = assembly_el.find('.//{http://www.w3.org/2000/09/xmldsig#}DigestValue')
    return {'url_path': assembly_el.get('codebase'), 'digest': digest_el.text,
            'digest_algo': xmldsig_algo[ digest_method_el.get('Algorithm') ]
            }

def fetch_manifest(url):
    return fetch_url(url)

def assembly_elem_to_dict(elem):
    digest_method_elem = elem.find('.//{http://www.w3.org/2000/09/xmldsig#}DigestMethod')
    digest_elem = elem.find('.//{http://www.w3.org/2000/09/xmldsig#}DigestValue')
    return {'url_path': elem.get('codebase'), 'size': elem.get('size'), 'digest': digest_elem.text,
            'digest_algo': xmldsig_algo[ digest_method_elem.get('Algorithm') ]
            }

def file_element_to_dict(elem):
    digest_method_elem = elem.find('.//{http://www.w3.org/2000/09/xmldsig#}DigestMethod')
    digest_elem = elem.find('.//{http://www.w3.org/2000/09/xmldsig#}DigestValue')
    return {'url_path': elem.get('name'), 'size': elem.get('size'), 'digest': digest_elem.text,
            'digest_algo': xmldsig_algo[ digest_method_elem.get('Algorithm') ]
            }

def extract_files(xml):
    tree = ET.fromstring(xml)
    assembly_el = tree.find(".//{urn:schemas-microsoft-com:asm.v2}dependentAssembly[@dependencyType='install']")
    assembly_dict = assembly_elem_to_dict(assembly_el)
    file_els = tree.findall('.//{urn:schemas-microsoft-com:asm.v2}file')
    return [assembly_dict] + [file_element_to_dict(f) for f in file_els]

def check_dir(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

def download_file(download_path, manifest_url, url_path, size, digest, digest_algo):
    url = '{0}.deploy'.format(urljoin(manifest_url, fix_url_path(url_path)))

    file_path = os.path.join(download_path, fix_fs_path(url_path))

    check_dir(file_path)

    hash = digest_impl[digest_algo]()

    with open(file_path, "wb") as handle:
        res = requests.get(url, stream=True)
        file_size = int(size)
        with tqdm(desc=file_path, total=file_size, unit='B', unit_scale=True, unit_divisor=1024, dynamic_ncols=True) as pbar:
            for data in res.iter_content():
                handle.write(data)
                hash.update(data)
                pbar.update(len(data))
    downloaded_digest = b64encode(hash.digest()).decode()
    if downloaded_digest != digest:
        raise Exception("Error validating {0} (downloaded digest {1} doesn't match expected digest {2})".format(file_path, downloaded_digest, digest))

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    url, download_path = args[0:2]

    if not url:
        raise MissingArgumentError('url (arg1) is missing')

    if not download_path:
        raise MissingArgumentError('download_path (arg2) is missing')

    dot_app_xml = fetch_dot_application(url)
    manifest_info = extract_manifest_info(dot_app_xml)

    manifest_url = urljoin(url, fix_url_path(manifest_info.get('url_path')))
    manifest_xml = fetch_manifest(manifest_url)

    files = extract_files(manifest_xml)

    for file in files:
        download_file(download_path, manifest_url, **file)

if __name__ == '__main__':
    main()
