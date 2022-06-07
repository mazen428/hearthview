from . import databaseManager
import globalPluginHandler
import scriptHandler


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.manager = databaseManager.CardDB()
