<p align="center">
    <img width=100% src="cover.gif">
  </a>
</p>
<b><p align="center"> 🤖 A modular and extendable Python tool for emulating simple SMALI methods. 📱 </p></b>

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
