import graphviz
from scanner import  scanner


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
        return lst_tokens


class Node:
    def __init__(self, value="root", index=0, parent_node=-1):
        self.value = value
        self.index = index
        self.parent_node = parent_node
        self.connect_parent = True

    def __str__(self):
        return self.value + "," + str(self.index) + " p: " + str(self.parent_node) + " " + str(self.connect_parent)

    def get_index(self):
        return self.index

    def is_statement(self):
        words = ["if", "repeat", "read", "write", "assign"]
        for word in self.value.split('\n'):
            if word in words:
                return True
        return False


class Parser:
    def __init__(self, tokens_list):
        self.tokens_list = tokens_list
        self.iterator = 0
        self.nodes = []
        self.parents = []
        self.current_node = 1
        self.con_par = True

    def program(self):

        self.statement_sequence()
        for t in self.nodes:
            print(t)
        return

    def match(self, expected_value):
        if self.tokens_list[self.iterator].value == expected_value or self.tokens_list[self.iterator].type == expected_value:
            self.iterator += 1
        else:
            print("expect", expected_value)
            print(self.tokens_list[self.iterator - 1].value)
            print(self.tokens_list[self.iterator].value)
            print(self.tokens_list[self.iterator + 1].value)
            raise ValueError("tokens are not in right sequence")
        return

    def statement_sequence(self):
        self.con_par = True
        self.statement()
        while self.tokens_list[self.iterator].value == ";":
            self.con_par = False
            self.match(";")
            self.statement()
        return

    def statement(self):
        token = self.tokens_list[self.iterator]
        node = Node(token.value, self.current_node, self.parents[-1])
        node.connect_parent = self.con_par
        self.nodes.append(node)
        self.current_node += 1
        self.parents.append(node.index)

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

        else:
            node.value = "assign"
            self.assign_statement()
            self.parents.pop()
        return

    def if_statement(self):
        self.match("if")
        self.expression()
        self.match("then")
        self.statement_sequence()
        if self.tokens_list[self.iterator].value == "else":
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
        self.match("read")
        if self.tokens_list[self.iterator].type == "identifier":
            # node = Node(self.tokens_list[self.iterator].value, self.current_node, self.parents[-1])
            # self.nodes.append(node)
            # self.current_node += 1
            self.nodes[-1].value = 'read\n({})'.format(self.tokens_list[self.iterator].value)
            self.match("identifier")
            return
        else:
            raise ValueError("read isn't followed by an identifier")

    def write_statement(self):
        self.match("write")
        self.expression()
        return

    def assign_statement(self):
        # print("new assign")
        # print(self.tokens_list[self.iterator-1].value)
        # print(self.tokens_list[self.iterator].value)
        # print(self.tokens_list[self.iterator+1].value)
        if self.tokens_list[self.iterator].type == "identifier":
            # node = Node(self.tokens_list[self.iterator].value, self.current_node, self.parents[-1])
            # self.nodes.append(node)
            # self.current_node += 1
            # self.parents.append(node.index)
            self.nodes[-1].value = "assign\n({})".format(self.tokens_list[self.iterator].value)
            self.match("identifier")
        else:
            raise ValueError("assign isn't followed by an identifier")
        self.match(":=")
        self.expression()
        # self.parents.pop()
        return

    def expression(self):
        self.simple_expression()
        if self.tokens_list[self.iterator].value in ['<', '=']:
            self.comparison()
            self.simple_expression()
            self.parents.pop()
        return

    def simple_expression(self):
        self.term()
        nested_op = 0
        while self.tokens_list[self.iterator].value in ['+', '-']:
            self.addop()
            self.term()
            nested_op += 1
        while nested_op > 0:
            self.parents.pop()
            nested_op -= 1

    def comparison(self):
        if self.tokens_list[self.iterator].value in ['<', '=']:
            node = Node("Op\n("+self.tokens_list[self.iterator].value+")", self.current_node, self.parents[-1])
            self.nodes.append(node)
            self.parents.append(node.index)
            self.nodes[self.current_node - 2].parent_node = self.parents[-1]
            self.current_node += 1
            self.match(self.tokens_list[self.iterator].value)

    def addop(self):
        token = self.tokens_list[self.iterator]
        if token.value == "+":
            node = Node("Op\n("+self.tokens_list[self.iterator].value+")", self.current_node, self.parents[-1])
            self.nodes.append(node)
            self.parents.append(self.current_node)
            self.nodes[self.current_node - 2].parent_node = self.parents[-1]
            self.current_node += 1
            self.match("+")
        elif token.value == "-":
            node = Node("Op\n("+self.tokens_list[self.iterator].value+")", self.current_node, self.parents[-1])
            self.nodes.append(node)
            self.parents.append(self.current_node)
            self.nodes[self.current_node - 2].parent_node = self.parents[-1]
            self.current_node += 1
            self.match("-")
        else:
            raise ValueError("add op isn't + or -")

    def factor(self):
        if self.tokens_list[self.iterator].value == "(":
            self.match("(")
            self.expression()
            self.match(")")
        elif self.tokens_list[self.iterator].type == "identifier":
            node = Node(self.tokens_list[self.iterator].value+"\n(ID)", self.current_node, self.parents[-1])
            self.nodes.append(node)
            self.current_node += 1
            self.match("identifier")
        elif self.tokens_list[self.iterator].type == "number":
            node = Node("const\n("+self.tokens_list[self.iterator].value+")", self.current_node, self.parents[-1])
            self.nodes.append(node)
            self.current_node += 1
            self.match("number")

    def term(self):
        self.factor()
        nested_operations = 0
        while self.tokens_list[self.iterator].value == "*" or self.tokens_list[self.iterator].value == "/":
            self.mul_op()
            self.factor()
            nested_operations += 1

        while nested_operations > 0:
            self.parents.pop()
            nested_operations -= 1
        return

    def mul_op(self):
        node = Node("Op\n("+self.tokens_list[self.iterator].value+")", self.current_node, self.parents[-1])
        self.nodes.append(node)
        self.parents.append(self.current_node)
        self.nodes[self.current_node - 2].parent_node = self.parents[-1]
        self.current_node += 1
        if self.tokens_list[self.iterator].value == "*":
            self.match("*")
        elif self.tokens_list[self.iterator].value == "/":
            self.match("/")
        else:
            raise ValueError("mul op isn't * or /")
        return

    def draw_tree(self):
        tree = graphviz.Digraph(comment="syntax tree", format="png")

        for node in self.nodes:
            if node.is_statement():
                tree.node(str(node.index), str(node.value), shape="square")
            elif node.value == "root" or node.parent_node == -1:
                pass
            else:
                tree.node(str(node.index), str(node.value))

        for node in self.nodes:
            if node.parent_node != 0 and node.connect_parent:
                tree.edge(str(node.parent_node), str(node.index))
            elif node.parent_node != 0 and not node.connect_parent:
                tree.edge(str(node.parent_node), str(node.index), style='dashed', color='white')

        for i in range(len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                if (self.nodes[i].parent_node == self.nodes[j].parent_node) and (not self.nodes[j].connect_parent) and\
                        (self.nodes[j].is_statement() and self.nodes[i].is_statement()):
                    tree.edge(str(self.nodes[i].index), str(self.nodes[j].index), constraint='false')
                    break
                elif (self.nodes[i].parent_node == self.nodes[j].parent_node) and self.nodes[j].connect_parent and\
                        (self.nodes[j].is_statement() and self.nodes[i].is_statement()):
                    break
        tree.render('Syntax-Tree.gv', view=True)


# if __name__ == "__main__":
#     scanner("test1.txt")
#     lst_tokens = tokenizer(file='output.txt')
#     init_node = Node()
#     parser = Parser(lst_tokens)
#     parser.parents.append(init_node.index)
#     parser.program()
#     parser.draw_tree()
