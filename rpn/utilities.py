from collections import deque

class Utilities:
    @staticmethod
    def swap(stack):
        if len(stack) >= 2:
            first = stack.pop()
            second = stack.pop()
            stack.append(first)
            stack.append(second)
        else:
            print("swap: requires 2 or more values, {} value avaiable".format(len(stack)))


    @staticmethod
    def dropn(stack, n):
        size = len(stack)
        if size >= 1:
            del stack[-n:]

    @staticmethod
    def dupn(stack, n):
        size = len(stack)
        vars = stack[size - n: ]
        del stack[-n:]
        for k in vars:
            stack.append(k)
            stack.append(k)

    @staticmethod
    def rotate(stack, n):
        stack = deque(stack)
        stack.rotate(n)
        stack = list(stack)
        return stack

    @staticmethod
    def pick(stack, n):
        size = len(stack)
        if size > n:
            return stack[size - n ]
        print("pick: invalid {} is greater than the number of item ({}) in the stack".format(n, size))






