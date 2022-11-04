import json
import pdb
import base64
import requests

from cabinet_lib.constants import ROOT_URL
import cabinet_lib.fns as f


def upload(metadata:dict, file_path:str) -> dict:
    """
    Add a new entry to the Cabinet System. Entry includes a blob in base64_str form and a dict of associated metadata
    """
    # NOTE: may need to move inside a nother fn so post and post_args aren't accessible to user
    blob = f.encode_blob(file_path)
    data = {'metadata':metadata, 'blob_b64s': blob}
    api_resp = requests.post(ROOT_URL+'/blob', json=data).json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    return api_resp['body']

def search(blob_type:str, parameters:dict) ->dict:
    """
    Returns metadata for all entries matching submitted search parameters
    """
    url = f.make_url(blob_type, parameters)
    api_resp = requests.get(ROOT_URL+url).json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    return api_resp['body']
      

def update(blob_type:str, entry_id:int, update_data:dict):
    """
    Creates a soft update of the metadata associated with a stored blob
    """
    data = {'blob_type':blob_type, 'entry_id':entry_id, 'update_data':update_data}
    api_resp = requests.post(ROOT_URL+'/blob/update', json=data).json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    return api_resp['body']

# OTHER 

def feilds(blob_type:str)-> dict: 
    """
    Returns a dict where keys are the metadata fields for specified blob_type. Values are None.  
    """
    fields:list = requests.get(ROOT_URL+f'/blob/feilds?blob_type={blob_type}').json()
    fields_dict = dict.fromkeys(fields)
    return fields_dict


def blob_types():
    """
    Lists all blob_types stored in Cabinet and their metadata fields
    """
    pass 



