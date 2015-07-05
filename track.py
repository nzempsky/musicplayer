import spotipy

class Track:
	'''A track object that contains information like the artist, track name, track ID, art, and time'''
	def __init__(self, track_id, spotify):
		self.spotify = spotify
		self.track_id = track_id
		result = spotify.track("spotify:track:" + track_id)
		self.track_name = result['name']
		self.artist_name = result['artists'][0]['name']
		self.length = result["duration_ms"]
		track_name_underscore = self.track_name.replace(" ", "_")
		artist_name_underscore = self.artist_name.replace(" ", "_")
		self.artpath = 'art/' + artist_name_underscore + '/'+ track_name_underscore + '.jpg'