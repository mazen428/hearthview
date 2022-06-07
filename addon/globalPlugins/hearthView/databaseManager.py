# databaseManager
# A part of NVDA HearthView add-on
# Copyright (C) 2022 mazen428
# This file is covered by the GNU General Public License version 2.0.
# See the file LICENSE for more details.


import urllib.request
import urllib.parse
import json
import os
import time
from logHandler import log
import math
import globalVars


class CardDB:
	def __init__(self):
		self._db = None
		self.DBPath = os.path.join(globalVars.appArgs.configPath, "addons", "hearthView", "cards.json")
		self.version = 0
		self.lastCheck = 0

	def _check(self, update=True):
		if os.path.isfile(self.DBPath):
			with open(self.DBPath, "r") as f:
				db = json.load(f)
				self.lastCheck = db.pop(0)
				self.version = db.pop(0)
				self._db = tuple(db)
			if (math.floor(time.time()) - self.lastCheck) > 86400 and update:
				self.update()
			return
		self.update() if update else None

	def update(self):
		log.info(f"checking for updates for cards. Version: {self.version}")
		with urllib.request.urlopen(urllib.request.Request(url="https://api.hearthstonejson.com/v1/latest/enUS/cards.collectible.json", headers={"User-Agent": "Mozilla/5.0"})) as req:
			netVersion = int(urllib.parse.urlparse(req.geturl()).path.split("/")[2])
			if netVersion <= self.version:
				return
			log.info(f"updating to {netVersion}")
			db = json.load(req)
		db.insert(0, math.floor(time.time()))
		db.insert(1, netVersion)
		with open(self.DBPath, "w") as f:
			json.dump(db, f)
		self._check(False)

	def get(self):
		self._check(True)
		return self._db

	def search(self, query, exact):
		db = self.get()
		if exact:
			for i in db:
				if i["name"].casefold() == query:
					return i
		elif not exact:
			return tuple((i for i in db if query in i["name"].casefold()))
