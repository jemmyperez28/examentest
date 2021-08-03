Feature: Crear un nuevo registro en tabla Persona

  Scenario: Crear registro usando Data Valida
    Given usuario crea jemmy x en tabla persona
    When envia la data a http://localhost:5000/persona/nueva_persona
    Then El usuario debe recibir una respuesta 200 como status code
    And nombre debe estar en cuerpo de respuesta 

