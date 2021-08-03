from behave import given, when, then, step
import requests
@given('usuario crea jemmy x en tabla persona')
def step_impl(context):
    context.request_body = {"nombre": "Jemmy X"}
@when('envia la data a http://localhost:5000/persona/nueva_persona')
def step_impl(context):
    response = requests.post('http://localhost:5000/persona/nueva_persona', json=context.request_body)
    context.respuesta = response
@then('El usuario debe recibir una respuesta 200 como status code')
def step_impl(context):
    assert context.respuesta.status_code == 200
@step('nombre debe estar en cuerpo de respuesta')
def step_impl(context):
    response_data = context.respuesta.json()
    assert response_data['nombre'] == "Jemmy X"

@given('los datos de la mascota nueva y usuario')
def step_impl(context):
    context.request_body = {
                            "nombre_mascota": "test_mascota",
                            "tipo": "perro",
                            "idpersona": 1
                            }
@when('envia la data a /persona/nueva_mascota')
def step_impl(context):
    response = requests.post('http://localhost:5000/persona/nueva_mascota', json=context.request_body)
    context.respuesta = response
@then('usuario recibe respuesta 200 del servidor')
def step_impl(context):
    assert context.respuesta.status_code == 200
@step('El usuario debe recibir el nombre de la mascota insertada')
def step_impl(context):
    response_data = context.respuesta.json()
    assert response_data['nombre_mascota'] == "test_mascota"

@given('el id de una persona')
def step_impl(context):
    context.idpersona = 1
@when('envia la data a /persona/get_mascotas/<int:id>')
def step_impl(context):
    response = requests.get('http://localhost:5000/persona/get_mascotas/'+str(context.idpersona))
    context.respuesta = response
@then('usuario recibe otra respuesta 200 del servidor')
def step_impl(context):
    assert context.respuesta.status_code == 200










