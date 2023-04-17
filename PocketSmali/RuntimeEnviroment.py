class RuntimeEnviroment():
    registers = {}
    string_pool = {}
    # A dict of special registers returned by a method
    return_registers = {}


    def save_return_registers(self, return_registers):
        self.return_registers = {}
        for register in return_registers:
            if register in self.registers:
                self.return_registers[register] = self.registers[register]

    def set_register(self, register, value, name="", type = ""):
        register = register.strip(",")


        if register not in self.registers:
            self.registers[register] = {"value":value,"name":name, "type": type}
        else:
            if value != None:
                self.registers[register] = {"value":value,"name":name, "type": type}
            else:
                # If not above then updating register info via local, etc
                if name != None:
                    self.registers[register]["name"] = name
                if type != None:
                    self.registers[register]["type"] = type

    def get_register_value(self, register):
        return self.registers[register]["value"]

    def add_to_string_pool(self, string_value):
        if string_value not in self.string_pool.values():
            string_idx = len(self.string_pool) + 1
            self.string_pool[string_idx] = string_value
        else:
            string_idx = next(key for key, value in self.string_pool.items() if value == string_value)
        return "string-pool-{}".format(string_idx)

    def get_string_from_pool(self, string_id):
        string_id.strip("string-pool-")
        # Get a string from the string pool
        if string_id in self.string_pool:
            return self.string_pool[string_id]
        else:
            raise Exception(f"String ID '{string_id}' does not exist in string pool")


