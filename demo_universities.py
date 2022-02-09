import json

import requests


host = 'http://127.0.0.1:5000/'


def get_university(university_id):
    response = requests.get(f'{host}universities/{university_id}/',headers={'Content-type': 'application/json'})
    
    print('Status code:', response.status_code)
    print(response.json())


def get_universities():
    response = requests.get(f'{host}universities/')
    
    print('Status code:', response.status_code)
    print(response.json())


def create_university(payload):
    response = requests.post(f'{host}universities/', json.dumps(payload), headers={'Content-type': 'application/json'})
    
    print('Status code:', response.status_code)
    print(response.json())


def delete_university(university_id):
    response = requests.delete(f'{host}universities/{university_id}/')
    
    print('Status code:', response.status_code)
    print(response.json())


def update_university(university_id, payload):
    response = requests.put(f'{host}universities/{university_id}/', json.dumps(payload), headers={'Content-type': 'application/json'})
    
    print('Status code:', response.status_code)
    print(response.json())
