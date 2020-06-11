from cmd import Cmd

class RPNPrompt(Cmd):
    prompt = '> '
    intro = "rpn interactive"

    def convert(self, val):
        return self.convert_mode[self.mode](val)

    def to_hex(self,val):
        return hex(val)

    def to_bin(self,val):
        return bin(val)

    def to_dec(self,val): #value already in integer/decemer
        return val

    def to_oct(self,val):
        return oct(val)


    def setup_display(self):
        self.mode = "dec"
        # ######  Display Modes ###########
        self.convert_mode = {"bin": self.to_bin , "hex": self.to_hex ,"dec": self.to_dec ,"oct": self.to_oct }

    def do_exit(self, inp):
        print("Bye")
        return True

    def do_bin(self, inp):
        self.mode = "bin"
        print("Binary Display Mode")

    def do_dec(self, inp):
        self.mode = "dec"
        print("Decimal Display Mode")

    def do_hex(self, inp):
        self.mode = "hex"
        print("Hexadecimal Display Mode")

    def do_oct(self, inp):
        self.mode = "oct"
        print("Octal Display Mode")



    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def help_add(self):
        print("Add a new entry to the system.")


    do_EOF = do_exit
    help_EOF = help_exit
