![](https://i.imgur.com/y6hOYx3.png)
This is a library that makes automating events in ADOFAI levels more convenient.
<br>List of Classes:<br>
<hr>
<i><code style="color : white">LevelDict</code></i>
<dl>
    Initalize with <code>LevelDict(filename, encoding)</code> (encoding is optional, default is utf-8-sig)<br>
    <br><dt><code>LevelDict.filename : str</code>
    <dd>The filename of the file from which the <code>LevelDict</code> was obtained.
    <dt><code>LevelDict.encoding : str</code>
    <dd>The encoding of the file from which the <code>LevelDict</code> was obtained.
    <dt><code>LevelDict.leveldict : dict</code>
    <dd>The specified file in the form of nested dictionaries and lists.
    <dt><code>LevelDict.angleData : list[float]</code>
    <dd>A list of all tile angles in the level.
    <dt><code>LevelDict.actions : list[Action]</code>
    <dd>A list of all actions (tile-based events) in the level.
    <dt><code>LevelDict.decorations : list[Decoration]</code>
    <dd>A list of all decorations (including objects and text) in the level.
    <dt><code>LevelDict.nonFloorDecos : list[Decoration]</code>
    <dd>A list of all decorations in the level that are not tied to any particular tile.
    <dt><code>LevelDict.settings : Settings</code>
    <dd>The level settings, as a Settings object.
    <dt><code>LevelDict.tiles : list[Tile]</code>
    <dd>A list of all tiles in the level. (See <code>Tile</code> class)</dd>
    <br><dt><code>LevelDict.appendTile(self, angle : float) -> None:</code>
    <dd>Adds a single tile to the end of the level.
    <dt><code>LevelDict.appendTiles(self, angles : list[float]) -> None:</code>
    <dd>Adds a list of tiles to the end of the level.
    <dt><code>LevelDict.insertTile(self, angle : float, index : int) -> None:</code>
    <dd>Adds a single tile to the level before the specified index.
    <dt><code>LevelDict.insertTiles(self, angles : list[float], index : int) -> None:</code>
    <dd>Adds a list of tiles to the level before the specified index.
    <dt><code>LevelDict.addAction(self, event : Action) -> int:</code>
    <dd>Adds the given action to the level. Returns the index of the event within the tile.
    <dt><code>LevelDict.addDecoration(self, event : Decoration) -> int:</code>
    <dd>Adds the given decoration to the level. Returns the index of the event within the tile / within the list of non-floor decorations.
    <dt><code>LevelDict.getActions(self, condition : Callable) -> list[Action]:</code>
    <dd>Returns a list of actions in the level that meet the given condition. Returns a list of all actions if condition is not specified.
    <dt><code>LevelDict.getDecorations(self, condition : Callable) -> list[Decoration]:</code>
    <dd>Returns a list of decorations in the level that meet the given condition. Returns a list of all decorations if condition is not specified.
    <dt><code>LevelDict.removeActions(self, condition : Callable) -> list[Action]:</code>
    <dd>Removes all actions in the level that meet the given condition. Returns a list of removed actions.
    <dt><code>LevelDict.removeDecorations(self, condition : Callable) -> list[Decoration]:</code>
    <dd>Removes all decorations in the level that meet the given condition. Returns a list of removed decorations.
    <dt><code>LevelDict.popAction(self, tile, index) -> Action:</code>
    <dd>Removes the action at the specified tile at the specified index. Returns the event.
    <dt><code>LevelDict.popDecoration(self, tile, index) -> Decoration:</code>
    <dd>Removes the decoration at the specified tile at the specified index. Returns the event.
    <dt><code>LevelDict.replaceFieldAction(self, condition : Callable, field : str, new) -> None:</code>
    <dd>Changes the value of "field" to "new" in all actions that meet the given condition.
    <dt><code>LevelDict.replaceFieldDecoration(self, condition : Callable, field : str, new) -> None:</code>
    <dd>Changes the value of "field" to "new" in all decorations that meet the given condition.
    <dt><code>LevelDict.writeDictToFile(self, leveldict : dict, filename : str):</code>
    <dd>Writes the given dictionary to the specified file. Overwrites the original file if filename is not specified.
    <br><i>Use this if you are working with <code>LevelDict.leveldict</code>.</i>
    <dt><code>LevelDict.writeToFile(self, filename : str=None) -> None:</code>
    <dd>Writes the level to the specified file. Overwrites the original file if filename is not specified.
</dl>
<hr>
<i><code style="color : white">Settings</code></i><br>
Part of a LevelDict object. The properties of this class are equivalent to the parameters in the <code>settings</code> field of a .adofai file.
<hr>
<i><code style="color : white">Tile</code></i><br>
A list of Tiles is contained within a LevelDict object.
<dl>
    <dt><code>Tile.angle : float</code>
    <dd>The angle that the tile points towards (0 degrees is facing right, 90 degrees is facing upwards)
    <dt><code>Tile.actions : list[Action]</code>
    <dd>A list of actions which are present on that particular tile.
    <dt><code>Tile.decorations : list[Decoration]</code>
    <dd>A list of decorations which are present on that particular tile.
</dl>
<hr>
<i><code style="color : white">Action</code></i><br>
An event that goes on a tile (one with a purple icon). An <code> Action </code> object behaves like a <code>dict</code>. The keys depend on the event type. Check any entry in the <code>actions</code> field of a .adofai file for more information on the fields used by that event type.
<br><br>
Action objects are found in a list of actions in a <code>Tile</code> object.
<hr>
<i><code style="color : white">Decoration</code></i><br>
A decoration, object decoration, or text decoration (anything found in the decorations menu on the left sidebar). A <code> Decoration </code> object behaves like a <code>dict</code>. The keys depend on the event type. Check any entry in the <code>decorations</code> field of a .adofai file for more information on the fields used by that event type.
<br><br>
Decoration objects are found in a list of decorations in a <code>Tile</code> object. If the decoration is not tied to any tile, it is found in the list of non-floor decos.