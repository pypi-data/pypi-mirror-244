import re
import json
from collections import UserDict
from typing import Callable

class Action(UserDict):
	def __init__(self,*arg,**kw):
		super(Action, self).__init__(*arg, **kw)

class Decoration(UserDict):
	def __init__(self,*arg,**kw):
		super(Decoration, self).__init__(*arg, **kw)

class Tile():
	def __init__(self, angle : int, actions : list=[], decorations : list=[]):
		self.angle = angle
		self.actions = actions.copy()
		self.decorations = decorations.copy()

class Settings():
	def __init__(self, values : dict) -> None:
		self.version = values["version"]
		self.artist = values["artist"]
		self.specialArtistType = values["specialArtistType"]
		self.artistPermission = values["artistPermission"]
		self.song = values["song"]
		self.author = values["author"]
		self.separateCountdownTime = values["separateCountdownTime"]
		self.previewImage = values["previewImage"]
		self.previewIcon = values["previewIcon"]
		self.previewIconColor = values["previewIconColor"]
		self.previewSongStart = values["previewSongStart"]
		self.previewSongDuration = values["previewSongDuration"]
		self.seizureWarning = values["seizureWarning"]
		self.levelDesc = values["levelDesc"]
		self.levelTags = values["levelTags"]
		self.artistLinks = values["artistLinks"]
		self.speedTrialAim = values["speedTrialAim"]
		self.difficulty = values["difficulty"]
		self.requiredMods = values["requiredMods"]
		self.songFilename = values["songFilename"]
		self.bpm = values["bpm"]
		self.volume = values["volume"]
		self.offset = values["offset"]
		self.pitch = values["pitch"]
		self.hitsound = values["hitsound"]
		self.hitsoundVolume = values["hitsoundVolume"]
		self.countdownTicks = values["countdownTicks"]
		self.trackColorType = values["trackColorType"]
		self.trackColor = values["trackColor"]
		self.secondaryTrackColor = values["secondaryTrackColor"]
		self.trackColorAnimDuration = values["trackColorAnimDuration"]
		self.trackColorPulse = values["trackColorPulse"]
		self.trackPulseLength = values["trackPulseLength"]
		self.trackStyle = values["trackStyle"]
		self.trackTexture = values["trackTexture"]
		self.trackTextureScale = values["trackTextureScale"]
		self.trackGlowIntensity = values["trackGlowIntensity"]
		self.trackAnimation = values["trackAnimation"]
		self.beatsAhead = values["beatsAhead"]
		self.trackDisappearAnimation = values["trackDisappearAnimation"]
		self.beatsBehind = values["beatsBehind"]
		self.backgroundColor = values["backgroundColor"]
		self.showDefaultBGIfNoImage = values["showDefaultBGIfNoImage"]
		self.showDefaultBGTile = values["showDefaultBGTile"]
		self.defaultBGTileColor = values["defaultBGTileColor"]
		self.defaultBGShapeType = values["defaultBGShapeType"]
		self.defaultBGShapeColor = values["defaultBGShapeColor"]
		self.bgImage = values["bgImage"]
		self.bgImageColor = values["bgImageColor"]
		self.parallax = values["parallax"]
		self.bgDisplayMode = values["bgDisplayMode"]
		self.imageSmoothing = values["imageSmoothing"]
		self.lockRot = values["lockRot"]
		self.loopBG = values["loopBG"]
		self.scalingRatio = values["scalingRatio"]
		self.relativeTo = values["relativeTo"]
		self.position = values["position"]
		self.rotation = values["rotation"]
		self.zoom = values["zoom"]
		self.pulseOnFloor = values["pulseOnFloor"]
		self.bgVideo = values["bgVideo"]
		self.loopVideo = values["loopVideo"]
		self.vidOffset = values["vidOffset"]
		self.floorIconOutlines = values["floorIconOutlines"]
		self.stickToFloors = values["stickToFloors"]
		self.planetEase = values["planetEase"]
		self.planetEaseParts = values["planetEaseParts"]
		self.planetEasePartBehavior = values["planetEasePartBehavior"]
		self.defaultTextColor = values["defaultTextColor"]
		self.defaultTextShadowColor = values["defaultTextShadowColor"]
		self.congratsText = values["congratsText"]
		self.perfectText = values["perfectText"]
		self.legacyFlash = values["legacyFlash"]
		self.legacyCamRelativeTo = values["legacyCamRelativeTo"]
		self.legacySpriteTiles = values["legacySpriteTiles"]
		
class LevelDict:

	def __init__(self, filename, encoding="utf-8-sig") -> None:
		
		self.filename = filename
		self.encoding = encoding
		leveldict = self.__getFileDict()
		angleData = leveldict["angleData"]
		angleData.append(angleData[len(angleData)-1])
		actions = leveldict["actions"]
		decorations = leveldict["decorations"]
		self.nonFloorDecos = [Decoration(j) for j in decorations if "floor" not in j.keys()]
		self.settings = Settings(leveldict["settings"])
		self.tiles = list()

		for angle in angleData:
			self.tiles.append(Tile(angle))

		for action in actions:
			self.tiles[action["floor"]].actions.append(Action(action))

		for deco in decorations:
			if "floor" in deco.keys():
				self.tiles[deco["floor"]].decorations.append(Decoration(deco))

	def __getFileString(self) -> str:
		"""Returns the specified file in string format.
		It is reccomended to use getFileDict() unless absolutely necessary.
		"""
		with open(self.filename, "r", encoding=self.encoding) as f:
			s = f.read()
			return s

	def __getFileDict(self) -> dict:
		"""Returns the specified file in the form of nested dictionaries and lists.
		"""
		a = self.__getFileString()
		sp=re.split(r"(?<!\\)(?:\\\\)*(\")",a)

		for i in range(len(sp)):
			if i % 4 == 0:
				sp[i] = re.sub(r"(\n|\t)", "", sp[i])
				sp[i] = re.sub(r"\,(( *)(\]|\}))", "\\3", sp[i])
				sp[i] = re.sub(r"(\]|\})(\[|\{)", "\\1,\\2", sp[i])
		
		a = ''.join(sp)
		final = json.loads(a)
		return final

	def __addTile(self, angle : float, index : int=None) -> None:
		if index is not None:
			self.tiles.insert(index, Tile(angle))
		else:
			self.tiles.insert(len(self.tiles)-1, Tile(angle))
			self.tiles[len(self.tiles)-1].angle = self.tiles[len(self.tiles)-2].angle

	def __addTiles(self, angles : list[float], index : int=None) -> None:
		
		if index is not None:
			for angle in reversed(angles):
				self.__addTile(angle, index)
		else:
			for angle in angles:
				self.__addTile(angle)

	def appendTile(self, angle : float) -> None:
		"""Adds a single tile to the end of the level.
		"""
		self.__addTile(angle)
		for i in range(len(self.tiles)-1, len(self.tiles)):
			for action in self.tiles[i].actions:
				action["floor"] += 1
			for deco in self.tiles[i].decorations:
				deco["floor"] += 1

	def appendTiles(self, angles : list[float]) -> None:
		"""Adds a list of tiles to the end of the level.
		"""
		self.__addTiles(angles)
		for i in range(len(self.tiles)-1, len(self.tiles)):
			for action in self.tiles[i].actions:
				action["floor"] += len(angles)
			for deco in self.tiles[i].decorations:
				deco["floor"] += len(angles)

	def insertTile(self, angle : float, index : int) -> None:
		"""Adds a single tile to the level before the specified index.
		"""
		self.__addTile(angle, index)
		for i in range(index+1, len(self.tiles)):
			for action in self.tiles[i].actions:
				action["floor"] += 1
			for deco in self.tiles[i].decorations:
				deco["floor"] += 1

	def insertTiles(self, angles : list[float], index : int) -> None:
		"""Adds a list of tiles to the level before the specified index.
		"""
		self.__addTiles(angles, index)
		for i in range(index+len(angles), len(self.tiles)):
			for action in self.tiles[i].actions:
				action["floor"] += len(angles)
			for deco in self.tiles[i].decorations:
				deco["floor"] += len(angles)
	
	def addAction(self, event : Action) -> int:
		"""Adds the given action to the level.
		Returns the index of the event within the tile.
		"""

		self.tiles[event["floor"]].actions.append(event)
		return len(self.tiles[event["floor"]].actions) - 1

	def addDecoration(self, event : Decoration) -> int:
		"""Adds the given decoration to the level.
		Returns the index of the event within the tile / within the list of non-floor decorations.
		"""
		
		if "floor" in event.keys():
			self.tiles[event["floor"]].decorations.append(event)
			return len(self.tiles[event["floor"]].decorations) - 1
		else:
			self.nonFloorDecos.append(event)
			return len(self.nonFloorDecos) - 1

	def getActions(self, condition : Callable) -> list[Action]:
		"""Returns a list of actions in the level that meet the given condition.
		Returns a list of all actions if condition is not specified.
		"""
		matches = []
		for tile in self.tiles:
			matches.extend(list(filter(condition, tile.actions)))
				
		return matches
	
	def getDecorations(self, condition : Callable) -> list[Decoration]:
		"""Returns a list of decorations in the level that meet the given condition.
		Returns a list of all decorations if condition is not specified.
		"""
		matches = []
		for tile in self.tiles:
			matches.extend(list(filter(condition, tile.decorations)))
		matches.extend(list(filter(condition, self.nonFloorDecos)))
		return matches

	def removeActions(self, condition : Callable) -> list[Action]:
		"""Removes all actions in the level that meet the given condition.
		Returns a list of removed actions.
		"""
		matches = []
		for tile in self.tiles:
			matches.extend(list(filter(condition, tile.actions)))
		
		for tile in self.tiles:
			tile.actions = [action for action in tile.actions if action not in matches]

		return matches
	
	def removeDecorations(self, condition : Callable) -> list[Decoration]:
		"""Removes all decorations in the level that meet the given condition.
		Returns a list of removed decorations.
		"""
		matches = []
		for tile in self.tiles:
			matches.extend(list(filter(condition, tile.decorations)))
		matches.extend(list(filter(condition, self.nonFloorDecos)))

		for tile in self.tiles:
			tile.decorations = [deco for deco in tile.decorations if deco not in matches]
		self.nonFloorDecos = [deco for deco in self.nonFloorDecos if deco not in matches]

		return matches

	def popAction(self, tile, index) -> Action:
		"""Removes the action at the specified tile at the specified index.
		Returns the event.
		"""

		return self.tiles[tile].actions[index].pop()

	def popDecoration(self, tile, index) -> Decoration:
		"""Removes the decoration at the specified tile at the specified index.
		Returns the event.
		"""

		return self.tiles[tile].decorations[index].pop()

	def replaceFieldAction(self, condition : Callable, field : str, new) -> None:
		"""Changes the value of "field" to "new" in all actions that meet the given condition.
		"""
		eventlist = self.removeActions(condition)
		for action in eventlist:
			if field in action:
				action[field] = new

		for action in eventlist:
			self.addAction(action)

	def replaceFieldDecoration(self, condition : Callable, field : str, new) -> None:
		"""Changes the value of "field" to "new" in all decorations that meet the given condition.
		"""
		eventlist = self.removeDecorations(condition)
		for deco in eventlist:
			if field in deco:
				deco[field] = new

		for deco in eventlist:
			self.addDecoration(deco)

	def writeDictToFile(self, leveldict : dict, filename : str=None):
		"""Writes the given dictionary to the specified file.
		Overwrites the original file if filename is not specified.
		"""
		name = self.filename if filename is None else filename
		filestring = json.dumps(leveldict, indent=4)
		with open(name, "w", encoding=self.encoding) as f:
			f.write(filestring)

	def writeToFile(self, filename : str=None) -> None:
		"""Writes the level to the specified file.
		Overwrites the original file if filename is not specified.
		"""
		
		final = {"angleData": [], "settings": {}, "actions": [], "decorations": []}
		final["settings"] = self.settings.__dict__
		for tile in self.tiles:
			final["angleData"].append(tile.angle)
			final["actions"].extend([action.__dict__["data"] for action in tile.actions])
			final["decorations"].extend([decoration.__dict__["data"] for decoration in tile.decorations])
		
		final["decorations"] += [decoration.__dict__["data"] for decoration in self.nonFloorDecos]
		final["angleData"].pop()

		name = self.filename if filename is None else filename
		filestring = json.dumps(final, indent=4)
		with open(name, "w", encoding=self.encoding) as f:
			f.write(filestring)
