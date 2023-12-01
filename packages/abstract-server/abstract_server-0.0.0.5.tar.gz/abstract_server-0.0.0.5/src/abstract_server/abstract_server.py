import requests
import socket
import platform
import uuid
import requests
import random
import json
def random_range(i,k):
    return random.randint(i,k)
def get_random_from_size(obj,minimum = 0):
    if len(obj) in [1]:
        return obj[0]
    return obj[random.randint(minimum,len(obj)-1)]
def write_to_file(file_path,contents):
    with open(file_path, 'w', encoding='UTF-8') as f:
        f.write(contents)
    return contents
def read_from_file(file_path):
    with open(file_path, 'r', encoding='UTF-8') as f:
        return f.read()
def json_read(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
def json_dump(file_path,data):
    with open(file_path, 'w') as file:
        json.dump(data,file, indent=4)
            
def send_to_server(data, server_url):
    try:
        # Sending a POST request to the server
        response = requests.post(server_url, json=data)
        return response.json()  # Assuming the server sends back a JSON response
    except requests.RequestException as e:
        return str(e)
    
def get_data_from_server(server_url):
    try:
        # Sending a GET request to the server
        response = requests.get(server_url)
        return response.json()  # Assuming the server sends back a JSON response
    except requests.RequestException as e:
        return str(e)


