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

def update_reg_v0(emulator):
    emulator.runtime_env.set_register("v0","string-pool-2")

emulator = Emulator()
emulator.breakpoints[29] = update_reg_v0
emulator.add_stub("android/util/Log")
emulator.emulate_smali_code(code)
print(str(emulator))