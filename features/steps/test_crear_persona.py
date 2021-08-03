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
