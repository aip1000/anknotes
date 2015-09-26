### Python Imports
from sqlite3 import dbapi2 as sqlite
import time
import os

### Anki Shared Imports
from anknotes.constants import *

try:
	from aqt import mw
except:
	pass

ankNotesDBInstance = None
dbLocal = False

def last_anki_profile_name():
	anki_profile_path_root = os.path.abspath(os.path.join(os.path.dirname(PATH), '..' + os.path.sep))
	print anki_profile_path_root
	name = ANKI.PROFILE_NAME
	if name and os.path.isdir(os.path.join(anki_profile_path_root, name)): return name 
	if os.path.isfile(FILES.USER.LAST_PROFILE_LOCATION): name = file(FILES.USER.LAST_PROFILE_LOCATION, 'r').read().strip()
	if name and os.path.isdir(os.path.join(anki_profile_path_root, name)): return name 
	name = ANKI.PROFILE_NAME
	if name and os.path.isdir(os.path.join(anki_profile_path_root, name)): return name     
	dirs = [x for x in os.listdir(anki_profile_path_root) if os.path.isdir(os.path.join(anki_profile_path_root, x)) and x is not 'addons']
	if not dirs: return ""
	return dirs[0]

def ankDBSetLocal():
	global dbLocal
	dbLocal = True


def ankDBIsLocal():
	global dbLocal
	return dbLocal

def ankDB(reset=False):
	global ankNotesDBInstance, dbLocal
	if not ankNotesDBInstance or reset:
		if dbLocal:
			ankNotesDBInstance = ank_DB( os.path.abspath(os.path.join(PATH, '..' + os.path.sep , '..' + os.path.sep  , last_anki_profile_name() + os.path.sep, 'collection.anki2')))
		else:
			ankNotesDBInstance = ank_DB()
	return ankNotesDBInstance


def escape_text_sql(title):
	return title.replace("'", "''")


def get_evernote_title_from_guid(guid):
	return ankDB().scalar("SELECT title FROM %s WHERE guid = '%s'" % (TABLES.EVERNOTE.NOTES, guid))


def get_anki_deck_id_from_note_id(nid):
	return long(ankDB().scalar("SELECT did FROM cards WHERE nid = ?", nid))


def get_evernote_guid_from_anki_fields(fields):
	if not FIELDS.EVERNOTE_GUID in fields: return None
	return fields[FIELDS.EVERNOTE_GUID].replace(FIELDS.EVERNOTE_GUID_PREFIX, '')


def get_all_local_db_guids():
	return [x[0] for x in ankDB().all("SELECT guid FROM %s WHERE 1 ORDER BY title ASC" % TABLES.EVERNOTE.NOTES)]


class ank_DB(object):
	def __init__(self, path=None, text=None, timeout=0):
		encpath = path
		if isinstance(encpath, unicode):
			encpath = path.encode("utf-8")
		if path:
			self._db = sqlite.connect(encpath, timeout=timeout)
			self._db.row_factory = sqlite.Row
			if text:
				self._db.text_factory = text
			self._path = path
		else:
			self._db = mw.col.db._db
			self._path = mw.col.db._path
			self._db.row_factory = sqlite.Row
		self.echo = os.environ.get("DBECHO")
		self.mod = False

	def setrowfactory(self):
		self._db.row_factory = sqlite.Row

	def execute(self, sql, *a, **ka):
		s = sql.strip().lower()
		# mark modified?
		for stmt in "insert", "update", "delete":
			if s.startswith(stmt):
				self.mod = True
		t = time.time()
		if ka:
			# execute("...where id = :id", id=5)
			res = self._db.execute(sql, ka)
		elif a:
			# execute("...where id = ?", 5)
			res = self._db.execute(sql, a)
		else:
			res = self._db.execute(sql)
		if self.echo:
			# print a, ka
			print sql, "%0.3fms" % ((time.time() - t) * 1000)
			if self.echo == "2":
				print a, ka
		return res

	def executemany(self, sql, l):
		self.mod = True
		t = time.time()
		self._db.executemany(sql, l)
		if self.echo:
			print sql, "%0.3fms" % ((time.time() - t) * 1000)
			if self.echo == "2":
				print l

	def commit(self):
		t = time.time()
		self._db.commit()
		if self.echo:
			print "commit %0.3fms" % ((time.time() - t) * 1000)

	def executescript(self, sql):
		self.mod = True
		if self.echo:
			print sql
		self._db.executescript(sql)

	def rollback(self):
		self._db.rollback()

	def scalar(self, sql, *a, **kw):
		res = self.execute(sql, *a, **kw).fetchone()
		if res:
			return res[0]
		return None

	def all(self, sql, *a, **kw):
		return self.execute(sql, *a, **kw).fetchall()

	def first(self, sql, *a, **kw):
		c = self.execute(sql, *a, **kw)
		res = c.fetchone()
		c.close()
		return res

	def list(self, sql, *a, **kw):
		return [x[0] for x in self.execute(sql, *a, **kw)]

	def close(self):
		self._db.close()

	def set_progress_handler(self, *args):
		self._db.set_progress_handler(*args)

	def __enter__(self):
		self._db.execute("begin")
		return self

	def __exit__(self, exc_type, *args):
		self._db.close()

	def totalChanges(self):
		return self._db.total_changes

	def interrupt(self):
		self._db.interrupt()

	def InitTags(self, force=False):
		if_exists = " IF NOT EXISTS" if not force else ""
		self.execute(
			"""CREATE TABLE %s `%s` ( `guid` TEXT NOT NULL UNIQUE, `name` TEXT NOT NULL, `parentGuid` TEXT, `updateSequenceNum` INTEGER NOT NULL, PRIMARY KEY(guid) );""" % (
				if_exists, TABLES.EVERNOTE.TAGS))

	def InitNotebooks(self, force=False):
		if_exists = " IF NOT EXISTS" if not force else ""
		self.execute(
			"""CREATE TABLE %s `%s` ( `guid` TEXT NOT NULL UNIQUE, `name` TEXT NOT NULL, `updateSequenceNum` INTEGER NOT NULL, `serviceUpdated` INTEGER NOT NULL, `stack` TEXT, PRIMARY KEY(guid) );""" % (
				if_exists, TABLES.EVERNOTE.NOTEBOOKS))

	def InitSeeAlso(self, forceRebuild=False):
		if_exists = "IF NOT EXISTS"
		if forceRebuild:
			self.execute("DROP TABLE %s " % TABLES.SEE_ALSO)
			self.commit()
			if_exists = ""
		self.execute(
			"""CREATE TABLE %s `%s` ( `id` INTEGER, `source_evernote_guid` TEXT NOT NULL, `number` INTEGER NOT NULL DEFAULT 100, `uid` INTEGER NOT NULL DEFAULT -1, `shard` TEXT NOT NULL DEFAULT -1, `target_evernote_guid` TEXT NOT NULL, `html` TEXT NOT NULL, `title` TEXT NOT NULL, `from_toc` INTEGER DEFAULT 0, `is_toc` INTEGER DEFAULT 0, `is_outline` INTEGER DEFAULT 0, PRIMARY KEY(id) );""" % (if_exists, TABLES.SEE_ALSO))
				
	def Init(self):
		self.execute(
			"""CREATE TABLE IF NOT EXISTS `%s` ( `guid` TEXT NOT NULL UNIQUE, `title` TEXT NOT NULL, `content` TEXT NOT NULL, `updated` INTEGER NOT NULL, `created` INTEGER NOT NULL, `updateSequenceNum` INTEGER NOT NULL, `notebookGuid` TEXT NOT NULL, `tagGuids` TEXT NOT NULL, `tagNames` TEXT NOT NULL, PRIMARY KEY(guid) );""" % TABLES.EVERNOTE.NOTES)
		self.execute(
			"""CREATE TABLE IF NOT EXISTS `%s` ( `guid` TEXT NOT NULL, `title` TEXT NOT NULL, `content` TEXT NOT NULL, `updated` INTEGER NOT NULL, `created` INTEGER NOT NULL, `updateSequenceNum` INTEGER NOT NULL, `notebookGuid` TEXT NOT NULL, `tagGuids` TEXT NOT NULL, `tagNames` TEXT NOT NULL)""" % TABLES.EVERNOTE.NOTES_HISTORY)        
		self.execute(
			"""CREATE TABLE IF NOT EXISTS `%s` ( 	`root_title`	TEXT NOT NULL UNIQUE, 	`contents`	TEXT NOT NULL, 	`tagNames`	TEXT NOT NULL, 	`notebookGuid`	TEXT NOT NULL, 	PRIMARY KEY(root_title) );""" % TABLES.AUTO_TOC)
		self.execute(
			"""CREATE TABLE IF NOT EXISTS `%s` ( `guid` TEXT, `title` TEXT NOT NULL, `contents` TEXT NOT NULL, `tagNames` TEXT NOT NULL DEFAULT ',,', `notebookGuid` TEXT, `validation_status` INTEGER NOT NULL DEFAULT 0, `validation_result` TEXT);""" % TABLES.NOTE_VALIDATION_QUEUE)
		self.InitSeeAlso()
		self.InitTags()
		self.InitNotebooks()
