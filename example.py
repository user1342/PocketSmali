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

emulator = Emulator()
emulator.emulate_smali_code(code)
print(str(emulator))