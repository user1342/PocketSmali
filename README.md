<p align="center">
    <img width=100% src="cover.gif">
  </a>
</p>
<b><p align="center"> 🤖 A modular and extendable Python tool for emulating simple SMALI code. 📱 </p></b>

<br>
<div align="center">

![GitHub contributors](https://img.shields.io/github/contributors/user1342/PocketSmali)
![GitHub Repo stars](https://img.shields.io/github/stars/user1342/PocketSmali?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/user1342/PocketSmali?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/user1342/PocketSmali)

</div>

PocketSmali is a Python tool designed to emulate small chunks of SMALI code.

Instructions covered:
- ```const-string``` : Emulates the declaration of a string constant in SMALI code.
- ```const``` : Emulates the declaration of a numeric constant in SMALI code.
- ```.local``` : Emulates the declaration of a local variable in SMALI code.
- ```invoke*``` : Emulates the invocation of a method in SMALI code, including different variants such as ```invoke-virtual```, ```invoke-direct```, ```invoke-static```, and others.
- ```move-result*``` : Emulates the handling of the result from a method invocation in SMALI code, including different variants such as ```move-result```, ```move-result-object```, ```move-result-wide```, and others.

# ➡️ Instalation

Download and use as a Python package:
```bash 
pip install git+https://github.com/user1342/PocketSmali.git
```
PocketSmali has been tested on *Windows 11* and *Ubuntu 22.04.2 LTS*.

# 📲 Emulating SMALI

Simple, one instruction emulation:
```python
from PocketSmali.Emulator import Emulator
emulator = Emulator()
emulator.emulate_smali_instruction('const-string v0, "TAG"')
print(str(emulator))
```

SMALI code emulation:
```python
from PocketSmali.Emulator import Emulator

code = '''
.method public printVar()Ljava/lang/String;
    .locals 2

    .line 28
    const-string v0, "TAG"

    const-string v1, "Hello World"

    invoke-static {v0, v1}, Landroid/util/Log;->v(Ljava/lang/String;Ljava/lang/String;)I

    .line 29
    return-object v1
.end method'''

emulator = Emulator(is_verbose=True)
emulator.emulate_smali_code(code)
```
Emulating from a SMALI file:
```python
from PocketSmali.Emulator import Emulator

emulator = Emulator(is_verbose=True, smali_files_root_dir=r"MyApplication3\app\build\outputs\apk\debug\app-debug")
emulator.emulate_smali_method(r"MyApplication3\app\build\outputs\apk\debug\app-debug\smali_classes3\com\example"
                              r"MyApplication3\app\build\outputs\apk\debug\app-debug\smali_classes3\com\example\myapplication\MainActivity.smali","onCreate") 
```

# 🙏 Contributions
PocketSmali is both extendable and modular. To add handlers for other SMALI instructions, create a Python file in the ```opcode_handlers``` subfolder. Inside of this file, create a method that handles a specific instruction type - this method should take the parameters ```(opcode, operands, runtime_env, emulator)```. Then add to the ```dict_of_opcode_handlers``` dictionary in the Emulator class with the key being the name of the instruction and the value being a reference to your created method for handling it.

# ⚖️ Code of Conduct
PocketSmali follows the Contributor Covenant Code of Conduct. Please make sure [to review](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) and adhere to this code of conduct when contributing to Obfu[DE]scate.

# 🐛 Bug Reports and Feature Requests
If you encounter a bug or have a suggestion for a new feature, please open an issue in the GitHub repository. Please provide as much detail as possible, including steps to reproduce the issue or a clear description of the proposed feature. Your feedback is valuable and will help improve PocketSmali for everyone.

# 📜 License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)
