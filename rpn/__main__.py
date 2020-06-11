from .eval import Solution
import argparse
import sys

class RPN(Solution):

    def display(self, result):
        ##### display properties ######
        display = result['display']
        content = result['content']
        variable = result['variable']
        if display: # if horizontal
            if variable and  len(variable) > 0:
                print("[", end=' ')
                for key, val in variable.items():
                    print("{}={}".format(key, self.convert(val)), end=' ')
                print("]", end=' ')
            for i in content:
                print(self.convert(i), end=' ')




        else:
            if variable and len(variable) > 0:
                for key, val in variable.items():
                    print("[{}={}]".format(key, self.convert(val)))
            for k in reversed(content):
                print(self.convert(k))


    def default(self, input_exp):
        if type(input_exp) is str:
            exp = input_exp.strip()
            eval_exp = exp.split(" ")
            result =  self.eval(eval_exp)
        else:
            result = self.eval(input_exp)
        self.display(result)



    def emptyline(self):
        if self.output:
            self.display(self.output)



def main():
    interactive = RPN()
    interactive.setup_display()
    interactive.setup()

    parser = argparse.ArgumentParser(description='Evaluate a reversed polish notation expression', prog="rpn")
    parser.add_argument('expression',help='an integer for the accumulator', nargs="*")
    parser.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()

    if not sys.stdin.isatty():
        stdin = parser.parse_args().stdin.read().splitlines()
    else:
        stdin = []

    if (stdin):
        interactive.default(stdin[0])
    elif args.expression:
        interactive.default(args.expression)
    else:
        interactive.cmdloop()


if __name__ == '__main__':
    main()
