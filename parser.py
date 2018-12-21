class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


def tokenizer(file="output.txt"):
    with open(file, 'r') as f:
        lst_tokens = []
        for line in f:
            tokens = line.split(',')
            token = Token(tokens[1].strip(), tokens[0].strip())
            lst_tokens.append(token)


class Node:
    def __init__(self, value, index, parent_node):
        self.value = value
        self.index = index
        self.parent_node = parent_node

    def get_index(self):
        return self.index

    def if_statement(self):
        words = ["if", "then", "else", "end", "repeat", "until", "read", "write", "assign"]
        return self.value in words


class Parser:
    def __init__(self, tokens_list, iterator=0):
        self.tokens_list = tokens_list
        self.iterator = iterator
        self.nodes = []
        self.parents = []
        self.current_node = 1

    def match(self):
        pass

    def program(self):
        pass

    def stmt_statement(self):
        pass

    def statement(self):
        pass

    def if_statement(self):
        pass

    def repeat_statement(self):
        pass

    def read_statement(self):
        pass

    def write_statement(self):
        pass

    def assign_statement(self):
        pass

    def expression(self):
        pass

    def simple_expression(self):
        pass

    def comparision(self):
        pass

    def addop(self):
        pass

    def factor(self):
        pass

    def term(self):
        pass

    def mul_op(self):
        pass

