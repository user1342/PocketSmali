class RuntimeEnviroment():
    registers = {}  # A dictionary to store register values
    string_pool = {}  # A dictionary to store string values in a string pool
    return_registers = {}  # A dictionary to store special return registers

    def save_return_registers(self, return_registers):
        # Method to save return registers to the runtime environment
        self.return_registers = {}
        for register in return_registers:
            if register in self.registers:
                self.return_registers[register] = self.registers[register]

    def set_register(self, register, value, name="", type=""):
        # Method to set register value, name, and type in the runtime environment
        register = register.strip(",")  # Remove trailing comma from register

        if register not in self.registers:
            # If register does not exist in the registers dictionary, add it with value, name, and type
            self.registers[register] = {"value": value, "name": name, "type": type}
        else:
            if value is not None:
                # If register already exists and value is not None, update value, name, and type
                self.registers[register] = {"value": value, "name": name, "type": type}
            else:
                # If value is None, update name and/or type
                if name is not None:
                    self.registers[register]["name"] = name
                if type is not None:
                    self.registers[register]["type"] = type

    def get_register_value(self, register):
        # Method to get the value of a register from the runtime environment
        return self.registers[register]["value"]

    def add_to_string_pool(self, string_value):
        # Method to add a string value to the string pool and return the string ID
        if string_value not in self.string_pool.values():
            string_idx = len(self.string_pool) + 1
            self.string_pool[string_idx] = string_value
        else:
            string_idx = next(key for key, value in self.string_pool.items() if value == string_value)
        return "string-pool-{}".format(string_idx)

    def get_string_from_pool(self, string_id):
        # Method to get a string from the string pool using its ID
        string_id.strip("string-pool-")  # Remove "string-pool-" prefix from string ID
        if string_id in self.string_pool:
            return self.string_pool[string_id]
        else:
            raise Exception(f"String ID '{string_id}' does not exist in string pool")  # Raise exception if string ID is not found in the string pool