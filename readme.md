# Coder House: Proyecto Final Curso de Python

## Olivero Aimaretti Alexis Ivan
## Trivia Web APP

La aplicación web de trivia es un juego en el que los jugadores hacen preguntas y deben responder con estimaciones aproximadas. El ganador es aquel cuya respuesta sea la más cercana a la correcta.

Las preguntas que los jugadores generan se agrupan en eventos. Estos eventos se van creando y cerrando, lo que da lugar a ganadores de eventos, aquellos que acumulan más puntos a lo largo de diversas preguntas.

## USUARIOS

La aplicación permite el acceso a dos tipos de usuarios:
### **Players**
Los jugadores tienen acceso a revisar respuestas y preguntas generadas por ellos mismos. Además, pueden participar en eventos y ver los puntajes y tablas de posiciones.

La aplicación para los jugadores se divide en las siguientes secciones:


1. **Answers**
Permite visualizar todas las respuestas realizadas por el jugador registrado.

2. **Questions**
Permite visualizar y gestionar las preguntas realizadas por el jugador registrado.

3. **Events**
Permite participar en eventos, respondiendo a preguntas generadas por otros jugadores y consultar el ranking del evento.

4. **Scores**
Muestra un listado con las puntuaciones por evento y por pregunta, una vez que se haya determinado el resultado.

### **Staff**
Los miembros del staff cuentan con una sección adicional en la barra de navegación que les permite ver el listado de jugadores, todas las respuestas y preguntas generadas. Además, pueden ver, añadir, editar y eliminar eventos y reglas de preguntas.


## DINAMICA

1. Un jugador crea una pregunta asignada a un evento, con reglas asociadas (que determinan cómo se asignarán los puntajes).

2. Los demás jugadores pueden participar respondiendo a la pregunta desde la sección de eventos. La pregunta estará disponible al hacer clic en añadir respuesta.

3. Cuando todos los jugadores hayan participado, el creador de la pregunta podrá cerrarla, evitando que se sigan cargando respuestas.

4. Después de cerrarla, el creador de la pregunta debera calcular el resultado por medio del boton correspondiente
.
5. Una vez calculado el resultado, se podrá ver el listado de respuestas y el ganador de la pregunta.

6. El ganador de la pregunta recibirá puntos (según las reglas) que se acumularán a lo largo del evento.

7. La dinámica continúa de la misma forma hasta que el evento se cierra.

8. Durante el juego, los jugadores pueden consultar los puntajes de las preguntas y el ranking del evento.
.
8. Al cerrar el evento, se muestra el ranking con el ganador, el segundo y tercer puesto. A partir de este momento, no se pueden cargar más preguntas.


## OTRAS FUNCIONALIDADES

### Profile
Cuando un usuario se registra, se crea un registro en el modelo Players mediante signals, con relacion uno a uno con User, que será el perfil del usuario. En el perfil, el usuario puede cargar sus datos y su avatar.


### Account
Permite al jugador cambiar su correo electrónico o contraseña.


### Exchange
Es un sistema de chat integrado en la aplicación, donde todos los jugadores pueden enviar mensajes entre sí en un chat compartido.
Este sistema de mensajeria permite identificar los mensajes no leidos desde su ultimo acceso al chat.

## Models

#### Players
- user: One-to-one relationship with Django's User model
- image: Image field for the player's avatar
- first_name: Player's first name
- last_name: Player's last name
- date_birth: Player's date of birth
- phone: Player's phone number
- address: Player's address
- city: Player's city
- state: Player's state
- country: Player's country

#### Event
- name: Event name
- date: Event date
- status: Event status (open or closed)
- result: Event result (undetermined or determined)

#### QuestionsRules
- name: Rule name
- description: Rule description
- points: Points for correct answer
- bonus_exact_answer: Bonus for exact answer
- allows_draw: Boolean indicating if draws are allowed
- allows_wildcard: Boolean indicating if wildcards are allowed
- points_draw: Points awarded for a draw

#### Questions
- title: Question title
- category: Question category
- question: The actual question text
- date: Date the question was asked
- correct_answer: The correct answer for the question
- author: Foreign key to the Players model
- status: Question status (open or closed)
- result: Question result (undetermined or determined)
- event: Foreign key to the Event model
- question_rule: Foreign key to the QuestionsRules model

#### Answers
- answer: Answer text
- player: Foreign key to the Players model
- question: Foreign key to the Questions model

#### PlayerScore
- winner_answer: Foreign key to the Answers model
- points: Points awarded for the answer

#### Chat
- sender: Foreign key to Django's User model (sender of the chat message)
- date: Date and time the message was sent (automatically set to the current date and time)
- content: The text content of the chat message
- readers: Many-to-many relationship with Django's User model (users who have read the chat message)
