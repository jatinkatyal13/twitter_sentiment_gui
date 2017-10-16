import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import lib as analyser
import sqlite3


# create database connection to sqlite3
def create_connection(file_name):
	try:
		conn = sqlite3.connect(file_name)
		return conn
	except Exception as e:
		print(e)
	return None

def clean_db(conn):
	sql = ''' 
		DELETE FROM credentials WHERE consumer_key = ''
	'''
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()

# create table
def create_table(conn):
	sql = ''' 
		CREATE TABLE IF NOT EXISTS credentials ( consumer_key varchar(100), consumer_secret varchar(100), access_token varchar(100), access_token_secret varchar(100));
	'''
	cur = conn.cursor()
	cur.execute(sql)
	sql = '''
		INSERT INTO credentials VALUES ('', '', '', '')
	'''
	cur.execute(sql)
	conn.commit()

def update_table(conn, consumer_key, consumer_secret, access_token, access_token_secret):
	sql = '''
		UPDATE credentials SET consumer_key =  ?, consumer_secret = ?, access_token = ?, access_token_secret = ?
	'''
	cur = conn.cursor()
	cur.execute(sql, (consumer_key, consumer_secret, access_token, access_token_secret))
	conn.commit()

def getKeys():
	global connect
	sql = '''
		SELECT * FROM credentials;
	'''
	res = list()
	cur = connect.cursor()
	cur.execute(sql)
	for row in cur:
		res = row
	return res

class ResultWindow(Gtk.Window):
	def __init__(self, result):
		print(result[1][1])
		Gtk.Window.__init__(self, title = 'Result')

		self.vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
		self.add(self.vbox)

		self.hbox1 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=3)
		self.label11 = Gtk.Label("Positive : ")
		self.hbox1.pack_start(self.label11, True, True, 0)
		self.label12 = Gtk.Label(str(result[1][1]) + "%")
		self.hbox1.pack_start(self.label12, True, True, 0)
		self.vbox.pack_start(self.hbox1, True, True, 0)

		self.hbox1 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=3)
		self.label11 = Gtk.Label("Neutral : ")
		self.hbox1.pack_start(self.label11, True, True, 0)
		self.label12 = Gtk.Label(str(result[2][1]) + "%")
		self.hbox1.pack_start(self.label12, True, True, 0)
		self.vbox.pack_start(self.hbox1, True, True, 0)

		self.hbox1 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=3)
		self.label11 = Gtk.Label("Negative : ")
		self.hbox1.pack_start(self.label11, True, True, 0)
		self.label12 = Gtk.Label(str(result[3][1]) + "%")
		self.hbox1.pack_start(self.label12, True, True, 0)
		self.vbox.pack_start(self.hbox1, True, True, 0)


class CredentialAddWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title = "Add Credentials")

		self.vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
		self.add(self.vbox)

		self.consumer_key = Gtk.Entry()
		self.consumer_key.set_placeholder_text("Consumer Key")
		self.vbox.pack_start(self.consumer_key, True, True, 0)

		self.consumer_secret = Gtk.Entry()
		self.consumer_secret.set_placeholder_text("Consumer Secret")
		self.vbox.pack_start(self.consumer_secret, True, True, 0)

		self.access_token = Gtk.Entry()
		self.access_token.set_placeholder_text("Access Token")
		self.vbox.pack_start(self.access_token, True, True, 0)

		self.access_token_secret = Gtk.Entry()
		self.access_token_secret.set_placeholder_text("Access Token Secret")
		self.vbox.pack_start(self.access_token_secret, True, True, 0)

		self.saveButton = Gtk.Button(label = "Save")
		self.saveButton.connect("clicked", self.saveButtonClicked)
		self.vbox.pack_start(self.saveButton, True, True, 0)

	def saveButtonClicked(self, widget):
		global connect
		consumer_key = self.consumer_key.get_text()
		consumer_secret = self.consumer_secret.get_text()
		access_token = self.access_token.get_text()
		access_token_secret = self.access_token_secret.get_text()
		update_table(connect, consumer_key, consumer_secret, access_token, access_token_secret)
		self.close()

class MainWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title = "Twitter Sentiment")

		self.vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
		self.add(self.vbox)


		self.hbox1 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 3)

		self.credentialButton = Gtk.Button(label = "Add Credentials")
		self.credentialButton.connect("clicked", self.credentialButtonClick)
		self.hbox1.pack_start(self.credentialButton, True, True, 0)

		self.vbox.pack_start(self.hbox1, True, True, 0)




		self.hbox2 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 3)

		self.searchEntry = Gtk.Entry()
		self.searchEntry.set_placeholder_text("Search Handle")
		self.hbox2.pack_start(self.searchEntry, True, True, 0)

		self.searchButton = Gtk.Button(label = "Search")
		self.searchButton.connect("clicked", self.searchButtonClick)
		self.hbox2.pack_start(self.searchButton, True, True, 0)

		self.vbox.pack_start(self.hbox2, True, True, 0)

	def searchButtonClick(self, widget):
		handle = self.searchEntry.get_text()
		keys = getKeys()
		result = analyser.getSentimentGraph(handle, {
			'consumer_key':keys[0],
			'consumer_secret':keys[1],
			'access_token':keys[2],
			'access_token_secret':keys[3]
		})
		print(result)
		window = ResultWindow(result)
		window.show_all()

	def credentialButtonClick(self, widget):
		window = CredentialAddWindow()
		window.show_all()


if __name__ == '__main__':

	global connect

	connect = create_connection("db.sqlite3")
	create_table(connect)
	clean_db(connect)

	window = MainWindow()
	window.connect("delete-event", Gtk.main_quit)
	window.show_all()
	Gtk.main()
