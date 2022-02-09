import json

import requests


host = 'http://127.0.0.1:5000/'


def get_country(country_id):
    response = requests.get(f'{host}universities/{country_id}/')
    
    print('Status code:', response.status_code)
    print(response.json())


def get_countries():
    response = requests.get(f'{host}countries/')
    
    print('Status code:', response.status_code)
    print(response.json())


def create_country(payload):
    response = requests.post(f'{host}countries/', json.dumps(payload), headers={'Content-type': 'application/json'})
    
    print('Status code:', response.status_code)
    print(response.json())


def delete_country(university_id):
    response = requests.delete(f'{host}countries/{university_id}/')
    
    print('Status code:', response.status_code)
    print(response.json())


def update_country(university_id, payload):
    response = requests.put(f'{host}countries/{university_id}/', json.dumps(payload), headers={'Content-type': 'application/json'})
    
    print('Status code:', response.status_code)
    print(response.json())
