from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, session, request, flash, session, redirect
from flask.ext.socketio import SocketIO, emit, join_room, leave_room
from model import User, Country, Language, Language_desired, Game, Conversation, session as dbsession 
import jinja2


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
# thread = None



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch_game_card')
def fetch_game_card():

	#query for count of card type (e.g. 'taboo')
	#mimport random, choose a random number, use that number to query for a card within that group

	taboocard1 = dbsession.query(Game).get(1)


	return taboocard1


#get the data passed from the client
@socketio.on("new_msg", namespace="/chat")
def handle_new_msg(msg):
	print "hello", msg
	#send the data to all cients, via the id_tag , "msg_received"
	emit("msg_received", msg, broadcast=True)




#on button click, send url back to client
@socketio.on("put_first_img", namespace="/chat")
def put_first_img(img):
	taboocard1 = fetch_game_card()
	#send the data to all cients, via the id_tag , "msg_received"
	emit("img_url", taboocard1.filename, broadcast=True)





# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         time.sleep(50)
#         count += 1
#         socketio.emit('my response',
#                       {'data': 'Server generated event', 'count': count},
#                       namespace='/test')


# @app.route('/')
# def index():
#     global thread
#     if thread is None:
#         thread = Thread(target=background_thread)
#         thread.start()
#     return render_template('index.html')


# @socketio.on('my event', namespace='/test')
# def test_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my response',
#          {'data': message['data'], 'count': session['receive_count']})


# @socketio.on('my broadcast event', namespace='/test')
# def test_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my response',
#          {'data': message['data'], 'count': session['receive_count']},
#          broadcast=True)


# @socketio.on('join', namespace='/test')
# def join(message):
#     join_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my response',
#          {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
#           'count': session['receive_count']})


# @socketio.on('leave', namespace='/test')
# def leave(message):
#     leave_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my response',
#          {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
#           'count': session['receive_count']})


# @socketio.on('my room event', namespace='/test')
# def send_room_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my response',
#          {'data': message['data'], 'count': session['receive_count']},
#          room=message['room'])


# @socketio.on('connect', namespace='/test')
# def test_connect():
#     emit('my response', {'data': 'Connected', 'count': 0})


# @socketio.on('disconnect', namespace='/test')
# def test_disconnect():
#     print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
