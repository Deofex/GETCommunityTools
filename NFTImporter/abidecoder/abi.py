import requests
import json
from Crypto.Hash import keccak

def get_url(url, headers=None):
    '''Retrieve content from an URL'''
    response = requests.get(url, headers=headers)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url, headers=None):
    '''Retrieve a JSON file from an URL'''
    content = get_url(url, headers)
    js = json.loads(content)
    return js

def get_keccakhash(s):
    '''Create Keccakhash from ETH functions'''
    #t = get_keccakhash('Transfer(address,address,uint256)')
    k = keccak.new(digest_bits=256)
    b = str.encode(s)
    k.update(b)
    h = k.hexdigest()
    h = '0x{}'.format(h)
    return h

def decode_abi(abi):
    '''Decode the ABI'''
    functions = {}
    for a in abi:
        if 'name' not in a:
            continue
        if len(a['inputs']) == 0:
            continue
        s = a['name'] + '('
        for i in a['inputs']:
            s = s + i['type'] + ','
        s = s[:-1]
        s = s + ')'
        h = get_keccakhash(s)
        functions[h] = a['name']
    return functions

def decode_abi_from_url(abiurl):
    '''Retrieve the ABI from an url and decode it'''
    abi = get_json_from_url(abiurl)
    functions = decode_abi(abi)
    return functions

