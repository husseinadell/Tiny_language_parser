"""
This module scanns the code of TINY language from an input file, and produces an output filte
"""


class Scanner:

    def __init__(self):
        """Initialize paramaeters for the scanner."""
        self.reserverd_words = ["if", "then", "else", "end", "repeat", "until", "read", "write"]
        self.special_symbols = ["+", "-", "*", "/", "=", "<", "(", ")", ";", ":="]
        self.digits = "0123456789"
        self.letters = "abcdefghijklmnopqrstuvwxyz"
        self.current_state = 1
        self.set_value = ""
        self.set_type = ""
        self.tokens = []

    def process_line(self, line):
        """iterate over each char in line applying DFA."""
        for char in line:
            if self.current_state == 1:

                if char == "{":
                    self.current_state = 2    # Comment
                elif char == ":":
                    self.set_type = ", Assign"
                    self.set_value = char
                    self.current_state = 3    # Assign
                elif char in self.letters:
                    self.set_type = ", Identifier"
                    self.set_value = char
                    self.current_state = 4    # Identifier
                elif char in self.digits:
                    self.set_type = ", Number"
                    self.set_value = char
                    self.current_state = 5    # Number
                elif char in self.special_symbols:
                    self.set_type = ", SpecialSymbol"
                    self.set_value = char
                    self.tokens.append(self.set_value + self.set_type)  # Done
                    self.current_state = 1
                elif char != " " and char != "\n":
                    self.current_state = -1
            elif self.current_state == 2:

                if char == "}":
                    self.current_state = 1
                    self.set_value = ""
            elif self.current_state == 3:

                if char == "=":
                    self.set_value += char
                    self.tokens.append(self.set_value + self.set_type)  # Done
                    self.current_state = 1
                else:
                    self.current_state = -1
            elif self.current_state == 4:

                if char in self.letters:
                    self.set_value += char
                else:  # Done
                    self.current_state = 1
                    if self.set_value in self.reserverd_words:
                        self.set_type = ", Reserverd Word"
                    self.tokens.append(self.set_value + self.set_type)  # Done
            elif self.current_state == 5:

                if char in self.digits:
                    self.set_value += char
                else:  # Done
                    self.tokens.append(self.set_value + self.set_type)
                    self.current_state = 1
            # elif self.current_state == 6:
            #
            #
            #     self.tokens.append(self.set_value + self.set_type)
            #     self.current_state = 1

    def file_process(self, in_file="tiny_in.txt", out_file="tiny_out.txt"):
        in_file = open(in_file)
        count = 0
        for line in in_file:
            count += 1
            self.process_line(line)
            if self.current_state < 0:
                break

        if self.current_state < 0:
            print("Error in line ", count)
            return
        else:
            out_file = open(out_file, 'w')
            for token in self.tokens:
                out_file.write(token+"\n")
            out_file.close()
            print("Scanning run successfully!")


if __name__ == '__main__':
    scanner = Scanner()
    while True:
        fname = input("Enter the file name (or click enter for \"tiny_in.txt\"): ")
        if len(fname) < 1:
            scanner.file_process()
            cmd = input("click y to contenue or any key to exit: ")
            if cmd == 'y' or cmd == "Y":
                continue
            else:
                break
        else:
            try:
                scanner.file_process(fname)
            except Exception:
                print('File cannot be opened:', fname)
