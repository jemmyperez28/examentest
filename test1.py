import requests 
idpersona = 1
response = requests.get('http://localhost:5000/persona/get_mascotas/'+str(idpersona))
print(response.url)