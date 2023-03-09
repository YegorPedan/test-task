from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///playlist.db'
db = SQLAlchemy(app)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    url = db.Column(db.String(200))

    def __repr__(self):
        return '<Song %r>' % self.title

@app.route('/songs', methods=['GET'])
def get_songs():
    songs = Song.query.all()
    return jsonify([song.__dict__ for song in songs])

@app.route('/songs', methods=['POST'])
def add_song():
    data = request.get_json()
    song = Song(title=data['title'], artist=data['artist'], album=data['album'], duration=data['duration'], url=data['url'])
    db.session.add(song)
    db.session.commit()
    return jsonify({'message': 'Song added successfully'})

@app.route('/songs/<int:id>', methods=['GET'])
def get_song(id):
    song = Song.query.get(id)
    if song:
        return jsonify(song.__dict__)
    else:
        return jsonify({'error': 'Song not found'})

@app.route('/songs/<int:id>', methods=['PUT'])
def update_song(id):
    song = Song.query.get(id)
    if song:
        data = request.get_json()
        song.title = data['title']
        song.artist = data['artist']
        song.album = data['album']
        song.duration = data['duration']
        song.url = data['url']
        db.session.commit()
        return jsonify({'message': 'Song updated successfully'})
    else:
        return jsonify({'error': 'Song not found'})

@app.route('/songs/<int:id>', methods=['DELETE'])
def delete_song(id):
    song = Song.query.get(id)
    if song:
        if song.playing:
            return jsonify({'error': 'Song is currently playing'})
        else:
            db.session.delete(song)
            db.session.commit()
            return jsonify({'message': 'Song deleted successfully'})
    else:
        return jsonify({'error': 'Song not found'})

@app.route('/play', methods=['POST'])
def play():
    data = request.get_json()
    song = Song.query.get(data['id'])
    if song:
        song.playing = True
        db.session.commit()
        return jsonify({'message': 'Song is now playing'})
    else:
        return jsonify({'error': 'Song not found'})

@app.route('/pause', methods=['POST'])
def pause():
    data = request.get_json()
    song = Song.query.get(data['id'])
    if song:
        song.playing = False
        db.session.commit()
        return jsonify({'message': 'Song is now paused'})
    else:
        return jsonify({'error': 'Song not found'})

@app.route('/next', methods=['POST'])
def next_song():
    data = request.get_json()
    song = Song.query.get(data
