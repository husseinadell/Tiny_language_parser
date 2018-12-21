class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


def tokenizer(file="output.txt"):
    with open(file, 'r') as f:
        lst_tokens = []
        for line in f:
            tokens = line.split(',')
            token = Token(tokens[1].strip().lower(), tokens[0].strip().lower())
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
    def __init__(self, tokens_list):
        self.tokens_list = tokens_list
        self.iterator = 0
        self.nodes = []
        self.parents = []
        self.current_node = 1
        self.connect_parent = True

    def program(self):
        # hossam
        self.statement_sequence()
        return

    def match(self, expected_value):
        # hossam
        if self.tokens_list[self.iterator].value == expected_value:
            self.iterator += 1
        else:
            raise ValueError("tokens are not in right sequence")
        return

    def statement_sequence(self):
        # hossam
        self.statement()
        while self.tokens_list[self.iterator].value == ";":
            self.match(";")
            self.statement()
        return

    def statement(self):
        # hossam
        token = self.tokens_list[self.iterator]
        node = Node(token.value, self.current_node, self.parents[-1])
        self.nodes.append(node)
        self.current_node += 1
        self.parents.append(node)

        if token.value == "if":
            self.if_statement()
            self.parents.pop()

        elif token.value == "repeat":
            self.repeat_statement()
            self.parents.pop()

        elif token.value == "read":
            self.read_statement()
            self.parents.pop()

        elif token.value == "write":
            self.write_statement()
            self.parents.pop()

        elif token.value == "assign":
            self.assign_statement()
            self.parents.pop()

        else:
            raise ValueError("Reserved Word {} Not Supported".format(token.value))
        return

    def if_statement(self):
        self.match("if")
        self.expression()
        self.match("then")
        self.statement_sequence()
        if self.tokens_list[self.iterator] == "else":
            self.match("else")
            self.statement_sequence()
        self.match("end")
        return

    def repeat_statement(self):
        self.match("repeat")
        self.statement_sequence()
        self.match("until")
        self.expression()
        return

    def read_statement(self):
        # hossam
        self.match("read")
        if self.tokens_list[self.iterator].type == "Identifier":
            node = Node(self.tokens_list[self.iterator].value, self.current_node, self.parents[-1])
            self.nodes.append(node)
            self.current_node += 1
            self.match("Identifier")
            return
        else:
            raise ValueError("read isn't followed by an identifier")

    def write_statement(self):
        # hossam
        self.match("write")
        self.expression()
        return

    def assign_statement(self):
        pass

    def expression(self):
        pass

    def simple_expression(self):
        pass

    def comparision(self):
        pass

    def addop(self):
        # hossam
        token = self.tokens_list[self.iterator]
        if token.value == "+":
            node = Node(self.tokens_list[self.iterator].value, self.current_node, self.parents[-1])
            self.nodes.append(node)
            self.parents.append(self.current_node)
            self.nodes[self.current_node - 2].parent_node = self.parents[-1]
            self.current_node += 1
            self.match("+")
        elif token.value == "-":
            node = Node(self.tokens_list[self.iterator].value, self.current_node, self.parents[-1])
            self.nodes.append(node)
            self.parents.append(self.current_node)
            self.nodes[self.current_node - 2].parent_node = self.parents[-1]
            self.current_node += 1
            self.match("-")
        else:
            raise ValueError("add op isn't + or -")

    def factor(self):
        pass

    def term(self):
        # hossam
        self.factor()
        nested_operations = 0
        while self.tokens_list[self.iterator] == "*" or self.tokens_list[self.iterator] == "/":
            self.mul_op()
            self.factor()
            nested_operations += 1

        while nested_operations > 0:
            self.parents.pop()
            nested_operations -= 1
        return

    def mul_op(self):
        # hossam
        if self.tokens_list[self.iterator].value == "*":
            pass
        if self.tokens_list[self.iterator].value == "/":
            pass
        else:
            raise ValueError("mul op isn't * or /")
        return

    def draw_tree(self):
        pass
