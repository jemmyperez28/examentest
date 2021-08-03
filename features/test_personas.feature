Feature: Feature para algunos Casos de Personas 

  Scenario: Crear registro usando Data Valida
    Given usuario crea jemmy x en tabla persona
    When envia la data a http://localhost:5000/persona/nueva_persona
    Then El usuario debe recibir una respuesta 200 como status code
    And nombre debe estar en cuerpo de respuesta 

  Scenario: Insertar Mascota Perteneciente a Usuario
    Given los datos de la mascota nueva y usuario 
    When envia la data a /persona/nueva_mascota
    Then usuario recibe respuesta 200 del servidor
    And El usuario debe recibir el nombre de la mascota insertada

  Scenario: Mostrar todas las mascotas pertenecientes a una persona
    Given el id de una persona 
    When envia la data a /persona/get_mascotas/<int:id>
    Then usuario recibe otra respuesta 200 del servidor

