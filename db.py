import sqlite3
import logging

class Database:
    '''
    @brief: Helper to use sqlite3
    '''
    _CREATE_ANIME_TABLE = """CREATE TABLE IF NOT EXISTS anime
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL);"""
    _CREATE_PICTURES_TABLE = """CREATE TABLE IF NOT EXISTS pictures
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        filename TEXT NOT NULL,
        url TEXT NOT NULL,
        fk_anime INTEGER,
        FOREIGN KEY(fk_anime) REFERENCES anime(id));"""
    _FIND_ID_IN_ANIME_BY_NAME = """SELECT id from anime WHERE name LIKE :name;"""
    _FIND_ID_IN_PICTURES_BY_URL = """SELECT id from pictures WHERE url LIKE :url;"""
    _FIND_IN_PICTURES_BY_URL = """SELECT * from pictures WHERE url LIKE :url;"""
    _INSERT_ANIME = """INSERT INTO anime (name) VALUES (:name);"""
    _INSERT_PICTURES = """INSERT INTO pictures (name, filename, url, fk_anime)
        VALUES (:name, :filename, :url, :fk_anime);"""

    def __init__(self, dbname):
        '''
        @brief: It will connect to the database name (or create it) and create (if not exists)
        our tables pictures and anime
        @param: dbname: database name
        '''
        try:
            self.conn = sqlite3.connect(dbname)
            self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as e:
            logging.error("[%s]: %s", dbname, e)
            raise sqlite3.OperationalError
        else:
            try:
                self.cursor.execute(self._CREATE_ANIME_TABLE)
                self.cursor.execute(self._CREATE_PICTURES_TABLE)
            except sqlite3.OperationalError as e:
                logging.error("Unable to use database file: %s", e)
                raise sqlite3.OperationalError
            else:
                logging.info("Database created and connected")

    def __del__(self):
        self.cursor.close()
        logging.info("Database closed")

    def _addEntryAnime(self, anime, nbEntries):
        '''
        @brief: It will check if anime is already in our database 'anime' and add it if not
        @param anime: anime name we will add
        @param nbEntries: 0 if anime not found in anime table, else > 0
        @return False if any error, else id for 'anime'
        '''
        if nbEntries == 0:
            try:
                self.cursor.execute(self._INSERT_ANIME, {'name': anime})
                self.conn.commit()
                logging.info("Entry added in anime: %s", anime)
            except sqlite3.OperationalError as e:
                logging.error("Unable to add [%s] in anime", anime)
                return False
            if self.cursor.lastrowid == None:
                logging.error("Unable to find anime added previously: %s", e)
                return False
            else:
                return self.cursor.lastrowid
        else:
            try:
                cursor = self.cursor.execute(self._FIND_ID_IN_ANIME_BY_NAME, {'name': anime})
                myid = cursor.fetchone()[0]
                logging.info("Id found for [%s] in pictures: %d", anime, myid)
                return int(myid)
            except sqlite3.OperationalError as e:
                logging.error("Unable to find anime added previously: %s", e)
                return False

    def _addEntryPictures(self, name, filename, url, animeId):
        '''
        @brief: It will add an entry into pictures table with specific name, filename and url
        @param name: name from submission title
        @param filename: image filename (name from url)
        @param url: url where the picture is
        @param animeId: id from anime table
        '''
        name = name.replace("'", "\'")
        try:
            self.cursor.execute(self._INSERT_PICTURES,
                {'name': name, 'filename': filename, 'url': url, 'fk_anime': animeId})
            self.conn.commit()
            logging.info("Entry added in pictures: %s with fk_anime: %d", name, animeId)
        except sqlite3.OperationalError as e:
            logging.warning("Unable to add an entry in pictures into database: %s", e)
            return False
        if self.cursor.lastrowid == None:
            logging.error("Unable to find picture added previously: %s", e)
            return False
        else:
            return self.cursor.lastrowid

    def addEntry(self, name, filename, url, anime):
        '''
        @brief:
        @param name:
        @param filename:
        @param url:
        '''
        if anime:
            try:
                nbEntries = self.checkEntryAnime(anime)
            except sqlite3.OperationalError:
                return False
            myId = self._addEntryAnime(anime, nbEntries)
            if not myId:
                myId = None
        else:
            myId = None
        if myId:
            self._addEntryPictures(name, filename, url, myId)
        return True if anime and nbEntries == 0 else False

    def checkEntryAnime(self, anime):
        try:
            cursor = self.cursor.execute(self._FIND_ID_IN_ANIME_BY_NAME, {'name': anime})
        except sqlite3.OperationalError as e:
            logging.warning("Unable to execute select in db: %s", e)
            raise sqlite3.OperationalError
        else:
            nbEntries = sum(1 for _ in cursor)
            logging.info("Entries found in anime: %d", nbEntries)
            return nbEntries

    def checkEntryPictures(self, url):
        '''
        @brief: It will check if there is already the url in our table pictures
        @param url: URL we want to check in our table
        @return: False if any problem else return number of entries
        '''
        try:
            cursor = self.cursor.execute(self._FIND_ID_IN_PICTURES_BY_URL, {'url': url})
        except sqlite3.OperationalError as e:
            logging.warning("Unable to execute select in db: %s", e)
            raise sqlite3.OperationalError
        else:
            nbEntries = sum(1 for _ in cursor)
            logging.info("Entries found in pictures: %d", nbEntries)
            return nbEntries
