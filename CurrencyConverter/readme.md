# Wox - Plugin for Python

### Flow for plugin
 - Define `plugin.json`
 - Make `main.py`

---
### Define `plugin.json`
 
 ```
 {
    "ID":"61c15660-fbc9-4706-9c74-705c50276523",
    "ActionKeyword":"cc",
    "Name":"Currency Converter",
    "Description":"Convert currency by format as <source> <des> <amount>",
    "Author":"Fred Zhou",
    "Version":"1.0",
    "Language":"python",
    "Website":"https://github.com/genauzhou88/wox_plugin",
    "IcoPath":"Images\\app.png",
    "ExecuteFileName":"main.py"
}
 ```
 
 > `ID`: defines uniqueness of plugin and can be generated from `https://www.uuidgenerator.net/`
 >
 > `ActionKeyword`: to enable the plugin in launcher
 > 
 > `Name`: Name of Plugin
 > 
 > `Description`: Short Description of the plugin
 >
 > `Author`: Name of creator of plugin
 >
 > `Version`: Version of Plugin
 >
 > `Language`: "python"
 >
 > `Website`: Website link to plugin
 >
 > `IcoPath`: Path to icon
 >
 > `ExecuteFileName`: The main file from where the execution to plugin can start

---
### Make main executable or start file `Main.py`
Use pre-defined wox integrations by importing `Wox`
 - `from wox import Wox`
 - Make a `class` and pass `Wox` as an argument to it
 - Initiate the class in the following manner:
```
 if __name__ == "__main__":
    HelloWorld()
```
 - The app receives the keyStrokes in `query()` of `main.py`
 - The context-menu for the result can be programmed in `context_menu` of `main.py`
 - The results in drop-down can be assigned triggers by defining custom method in `JsonRPCAction` of `results`
 

