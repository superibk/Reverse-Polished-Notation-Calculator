import math
import random
import re
import socket
from .prompt import RPNPrompt
from .utilities import Utilities


class Solution(RPNPrompt):
    def setup(self):
        self.stack = []
        self.repeat = 1
        self.var= {}
        self.macros = {}
        self.output = {}
        self.horizontal = True
        self.operators = {
            ### Arithemetic Operators ####
            "+":    {"num": 2, "exp": lambda a, b: a + b },
            "-":    {"num": 2, "exp": lambda a, b: a - b },
            "/":    {"num": 2, "exp": lambda a, b: a / b },
            "*":    {"num": 2, "exp": lambda a, b: a * b },
            "cla" : {"num": 0, "exp": lambda : self.stack.clear() and self.clear_var()},
            "clr":  {"num": 0, "exp": lambda : self.stack.clear()  },
            "clv":  {"num": 0, "exp": lambda : self.clear_var()  },
            "!":    {"num": 1, "exp": lambda a: (not a)  },
            "!=":   {"num": 2, "exp": lambda a, b: a != b},
            "%":    {"num": 2, "exp": lambda a, b: a % b },
            "++":   {"num": 1, "exp": lambda a : a + 1 },
            "--":   {"num": 1, "exp": lambda a : a - 1 },

            ##### Bitwise Operators ########
            "&":    {"num": 2, "exp": lambda a, b: a & b },
            "|":    {"num": 2, "exp": lambda a, b: a | b },
            "^":    {"num": 2, "exp": lambda a, b: a ^ b },
            "~":    {"num": 1, "exp": lambda a : ~a  },
            "<<":   {"num": 2, "exp": lambda a, b: a << b },
            ">>":   {"num": 2, "exp": lambda a, b: a >> b },

            ##### Boolean Operators ######
            "&&":   {"num": 2, "exp": lambda a, b: a and b },
            "||":   {"num": 2, "exp": lambda a, b: a or  b },
            "^^":   {"num": 2, "exp": lambda a, b: a != b  },

            ##### Comparison Operators ########
            "<":    {"num": 2, "exp": lambda a, b: a <  b  },
            "<=":   {"num": 2, "exp": lambda a, b: a <=  b },
            "==":   {"num": 2, "exp": lambda a, b: a == b  },
            ">":    {"num": 2, "exp": lambda a, b: a >  b  },
            ">=":   {"num": 2, "exp": lambda a, b: a >=  b },

            ###### Triginometric functions #######
            "acos": {"num": 1, "exp": lambda a: math.cos(a)  },
            "asin": {"num": 1, "exp": lambda a: math.asin(a) },
            "atan": {"num": 1, "exp": lambda a: math.atan(a) },
            "cos":  {"num": 1, "exp": lambda a: math.cos(a)  },
            "cosh": {"num": 1, "exp": lambda a: math.cosh(a) },
            "sin":  {"num": 1, "exp": lambda a: math.sin(a)  },
            "sinh": {"num": 1, "exp": lambda a: math.sinh(a) },
            "tanh": {"num": 1, "exp": lambda a: math.tanh(a) },

            ##### Numeric untilities #######
            "ceil": {"num": 1, "exp": lambda a: math.ceil(a) },
            "floor":{"num": 1, "exp": lambda a: math.floor(a) },
            "round":{"num": 1, "exp": lambda a: round(a) },
            "ip":   {"num": 1, "exp": lambda a: math.modf(a)[1] },
            "fp":   {"num": 1, "exp": lambda a: math.modf(a)[0] },
            "sign": {"num": 1, "exp": lambda a: -1 if int(math.copysign(1, a)) == -1 else 0 },
            "abs":  {"num": 1, "exp": lambda a: abs(a) },
            "max":  {"num": 2, "exp": lambda a, b: max(a, b) },
            "min":  {"num": 2, "exp": lambda a, b: min(a, b) },

            ##### Constants  #######
            "e":    {"num": 0, "exp": lambda : math.e },
            "pi":   {"num": 0, "exp": lambda : math.pi},
            "rand": {"num": 0, "exp": lambda : random.randint(0, 1000000000) },

            ##### Mathematic Function  #######
            "exp": {"num": 1, "exp": lambda a: math.exp(a) },
            "fact":{"num": 1, "exp": lambda a: math.factorial(a) },
            "sqrt":{"num": 1, "exp": lambda a: math.sqrt(a) },
            "ln":  {"num": 1, "exp": lambda a: math.log(a) },
            "log": {"num": 2, "exp": lambda a, b: math.log(a, b) },
            "pow": {"num": 2, "exp": lambda a, b: math.pow(a, b) },

            ######  Networking  ##########
            "hnl": {"num": 1, "exp": lambda a: socket.htonl(a) },
            "hns": {"num": 1, "exp": lambda a: socket.htons(a) },
            "nhl": {"num": 1, "exp": lambda a: socket.ntohl(a) },
            "nhs": {"num": 1, "exp": lambda a: socket.ntohs(a) },

            ##### Stak Manipulations ##########
            "pick":  {"num": 1, "exp": lambda a:  Utilities.pick(self.stack, a) },
            "repeat":{"num": 1, "exp": lambda a:  self.set_repeat(a) },
            "depth": {"num": 0, "exp": lambda  :  None if self.stack.append(len(self.stack)) else None },
            "drop":  {"num": 0, "exp": lambda  :  None if self.stack.pop() else None },
            "dropn": {"num": 1, "exp": lambda a:  Utilities.dropn(self.stack, a) },
            "dup":   {"num": 0, "exp": lambda  :  Utilities.dupn(self.stack, 1) },
            "dupn":  {"num": 1, "exp": lambda a:  Utilities.dupn(self.stack, a) },
            "roll":  {"num": 1, "exp": lambda a:  self.set_stack(Utilities.rotate(self.stack, a)) },
            "rolld": {"num": 1, "exp": lambda a:  self.set_stack(Utilities.rotate(self.stack, -a)) },
            "stack": {"num": 0, "exp": lambda  :  self.toggle_display() },
            "swap":  {"num": 0, "exp": lambda  :  Utilities.swap(self.stack) },

            ###### Macros and variables #######
            "macro": {"num": 1, "exp": lambda a: self.add_macro(a) },
            "var=":  {"num": 2, "exp": lambda a, b : self.set_var(a, b) },

            ###### display Mode  #######
            "bin": {"num": 0, "exp": lambda: print("bin cannot be used in an rpn expression, to switch display enter 'bin' alone") },
            "dec": {"num": 0, "exp": lambda: print("dec cannot be used in an rpn expression, to switch display enter 'dec' alone") },
            "hex": {"num": 0, "exp": lambda: print("hex cannot be used in an rpn expression, to switch display enter 'hex' alone ")},
            "oct": {"num": 0, "exp": lambda: print("oct cannot be used in an rpn expression, to switch display enter 'oct' alone") },

        }


    def toggle_display(self):
        self.horizontal = not self.horizontal

    def set_repeat(self, num):
        self.repeat = num
        return None

    def clear_var(self):
        self.var = None

    def set_stack(self, stack):
        self.stack = stack

    def set_var(self, char,  val):
        key = char[0].lower()
        self.var[key] = val
        return None

    def get_var(self):
        return self.var

    def add_macro(self, instruction):
        index = instruction.index("macro")
        key  = instruction[index+ 1]
        macros = " ".join(instruction[index + 2:])
        self.macros[key] = macros
        return None

    def eval(self, tokens):
        for char in tokens:

            try:
                if char in self.operators:
                    if char == "repeat":
                        self.operators[char]["exp"](self.stack.pop())
                        continue

                    if char == "macro":
                        self.operators[char]["exp"](tokens)
                        break


                    while(self.repeat > 0): # this is one by default
                        num_operand = self.operators[char]["num"]
                        if num_operand == 0 :
                            result = self.operators[char]["exp"]()
                        elif num_operand == 1:
                            a = self.stack.pop()
                            result = self.operators[char]["exp"](a)

                        elif num_operand == 2:
                            b = self.stack.pop()
                            a = self.stack.pop()
                            result = self.operators[char]["exp"](a, b)
                        else:
                            pass

                        if result is not None:
                            self.stack.append(result)

                        self.repeat -= 1 # decrement repeat
                    self.repeat = 1 # assign repeat back to one

                elif re.match("[a-zA-Z][a-zA-Z0-9]*=", char):
                    self.operators["var="]["exp"](char,self.stack.pop())

                elif char in self.var:
                    self.stack.append(int(self.var[char]))

                elif char in self.macros: # check if key in macro
                    eval_exp = self.macros[char].split(" ")
                    self.eval(eval_exp)

                else:
                    # value will be integer(any base) or float
                    try:
                        val = int(char, 0)
                        self.stack.append(val)

                    except ValueError:
                        try:
                            val = float(char)
                            self.stack.append(val)
                        except ValueError:
                            print("{}: Invalid character, operator or variable".format(char))


            except IndexError as e:
                print("{} operator requires {} value or numbers".format(char, self.operators[char]["num"] ))

            except Exception as e:
                pass


        self.output['content'] = self.stack if len(self.stack) > 0 else ""
        self.output['display'] = self.horizontal
        self.output['variable'] = self.var


        return self.output




