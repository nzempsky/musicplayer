import spotipy
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
import json, urllib, os
import requests
from track import Track
from Tkinter import *


#! /usr/bin/env python

import os, sys
from pygame.locals import *
spotify = spotipy.Spotify()

number_of_songs = 10



def display_box(screen, message):
	"Print a message in a box in the middle of the screen"
	fontobject = pygame.font.Font(None,18)
	pygame.draw.rect(screen, (255,255,255), ((screen.get_width()) - 302, (screen.get_height()) - 24,300,24), 1)
	if len(message) != 0:
		screen.blit(fontobject.render(message, 1, (255,255,255)), ((screen.get_width()) - 300, (screen.get_height()) - 18))

class PyManMain:
	"""The Main PyMan Class - This class handles the main 
	initialization and creating of the Game."""
	
	def __init__(self, queue, width=800,height=600):
		"""Initialize"""
		"""Initialize PyGame"""
		pygame.init()
		"""Set the window Size"""
		self.width = width
		self.height = height
		"""Create the Screen"""
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.screen.set_alpha(None)
		self.queue = queue

		pygame.font.init()
		self.current_string = []
		

														  
	def MainLoop(self):
		"""This is the Main Loop of the Game"""
		
		"""Load All of our Sprites"""
		self.LoadSprites();
		"""tell pygame to keep sending up keystrokes when they are
		held down"""
		
		"""Create the background"""
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0,0,0))
		direction = K_RIGHT
		directiony = K_DOWN

		while 1:
			if(self.photo.x > (self.width - self.photo.length)/2):
				direction = K_LEFT

			elif (self.photo.x <= 0):
				direction = K_RIGHT

			if(self.photo.y > (self.height - self.photo.length)/2):
				directiony = K_UP

			elif(self.photo.y <= 0):
				directiony = K_DOWN


			self.photo.move(direction)
			self.photo.move(directiony)

			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					self.photo.pause()
					sys.exit()
				elif event.type == KEYDOWN:
					if (event.key == K_RIGHT):
						self.photo.next()
						print('next song')
					inkey = event.key
					if inkey == K_BACKSPACE:
						self.current_string = self.current_string[0:-1]
					elif inkey == K_RETURN:
						query = ''.join(self.current_string)
						self.current_string = []
						track_id = look_up(query)
						download_images(track_id)
						self.queue.append(Track(track_id, spotify))

					elif inkey <= 127:
						self.current_string.append(chr(inkey))
					display_box(self.screen, "Add track: " + string.join(self.current_string,""))

			"""Do the Drawging"""               
			self.screen.blit(self.background, (0, 0))     

			self.photo_sprites.draw(self.screen)
			display_box(self.screen, "Add track: " + string.join(self.current_string,""))
			pygame.display.flip()


					
	def LoadSprites(self):
		"""Load the sprites that we need"""
		self.photo = Photo(self.queue)
		self.photo_sprites = pygame.sprite.RenderPlain((self.photo))

		
class Photo(pygame.sprite.Sprite):
	"""This is our snake that will move around the screen"""
	
	def __init__(self, queue):
		pygame.sprite.Sprite.__init__(self) 
		self.length = 300
		self.image = pygame.image.load(queue[0].artpath)
		self.image = pygame.transform.scale(self.image, (self.length, self.length))
		self.image = self.image.convert()
		self.rect = self.image.get_rect()

		self.track = queue[0]
		print self.track.track_id
		self.play_song(self.track.track_id)
		"""Set the number of Pixels to move each time"""
		self.x_dist = 2
		self.y_dist = 1 
		self.x = 0
		self.y = 0
		self.song_number = 0

		
	def move(self, key):
		"""Move your self in one of the 4 directions according to key"""
		"""Key is the pyGame define for either up,down,left, or right key
		we will adjust outselfs in that direction"""
		xMove = 0;
		yMove = 0;
		
		if (key == K_RIGHT):
			xMove = self.x_dist
		elif (key == K_LEFT):
			xMove = -self.x_dist
		elif (key == K_UP):
			yMove = -self.y_dist
		elif (key == K_DOWN):
			yMove = self.y_dist
		self.rect = self.rect.move(xMove,yMove);
		self.rect.move_ip(xMove,yMove);
		self.x += xMove
		self.y += yMove


	def play_song(self, track_id):
		from subprocess import Popen, PIPE
		scpt = "tell application \"Spotify\" to play track \"" + "spotify:track:" + track_id + "\""
		print scpt
		args = ['2', '2']
		p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate(scpt)

	def pause(self):
		from subprocess import Popen, PIPE
		scpt = '''tell application "Spotify" to pause track'''
		args = ['2', '2']
		p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate(scpt)

	def next(self):
		if(self.song_number + 1 < len(queue)):
			self.song_number = (self.song_number + 1)
			self.track = queue[self.song_number]
			self.play_song(self.track.track_id)
			self.image = pygame.image.load(self.track.artpath)
			self.image = pygame.transform.scale(self.image, (self.length, self.length))
			self.image = self.image.convert()


def download_images(track_id):
	spotify = spotipy.Spotify()
	result = spotify.track(track_id)
	track_name = result['name'].replace (" ", "_")
	artist_name = result['artists'][0]['name'].replace (" ", "_")
	if not os.path.exists('art/' + artist_name):
		os.makedirs('art/' + artist_name)
	address = 'art/' + artist_name + '/'+ track_name + '.jpg'
	f = open(address,'wb')
	f.write(urllib.urlopen(result['album']['images'][0]['url']).read())
	f.close()
	return True


def look_up(track_name):
	spotify = spotipy.Spotify()
	result = spotify.search(q='track:' + track_name, type='track')
	return result['tracks']['items'][0]['id']


def callback():
	print e.get() # This is the text you may want to use later

		
#Used to start everything		
if (len(sys.argv) < 2):
	print 'Incorrect number of arguments'
else:
	track_name = ''
	for word in sys.argv[1:len(sys.argv)]:
		track_name += str(word)
		track_name += ' '
	track_id = look_up(track_name)
	download_images(track_id)
	queue = []
	queue.append(Track(track_id, spotify))
	MainWindow = PyManMain(queue, 800, 600)
	MainWindow.MainLoop()