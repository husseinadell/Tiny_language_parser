def scanner():
    words = {
        "Reserved Words": ["if", "then", "else", "end", "repeat", "until", "read", "write"],
        "Special Symbols": ["+", "-", "*", "/", "=", "<", "(", ")"]
            }

    Symbols = ["+", "-", "*", "/", "=", "<", "(", ")"]
    comment_flag = 0
    # file = open()
    with open("input.txt", 'r') as file:
        with open("output.txt", "w") as output:
            for line in file:
                if "(" in line:
                    line = line.replace('(', " ( ")
                if ")" in line:
                    line = line.replace(')', " ) ")
                tokens = line.split()
                for i in range(len(tokens)):
                    f_sym = []
                    for sym in Symbols:
                        if sym in tokens[i]:
                            f_sym.append(sym)
                    for q in range(len(f_sym)):
                        if ':=' in tokens[i] and f_sym[q] == "=":
                            f_sym.pop(q)
                            continue
                        if ':=' in tokens[i] and f_sym[q] == ":":
                            f_sym.pop(q)
                            continue
                    if ':=' in tokens[i]:
                        f_sym.append(':=')
                    if f_sym:
                        for s in f_sym:
                            tokens[i] = tokens[i].replace(s, " " + s + " ")
                line_m = " ".join(tokens)
                tokens_m = line_m.split()
                for token in tokens_m:
                    flag = 0
                    if "{" in token:
                        comment_flag = 1
                        continue
                    if "}" in token:
                        comment_flag = 0
                        continue
                    if comment_flag:
                        continue
                    if ";" in token:
                        token = token[:-1]
                        flag = 1
                    if token in words['Reserved Words']:
                        output.write(token)
                        output.write(", ")
                        output.write("Reserved Words \n")
                    elif token in words['Special Symbols']:
                        output.write(token)
                        output.write(", ")
                        output.write("Special Symbols \n")
                    elif token in words['Special Symbols']:
                        output.write(token)
                        output.write(", ")
                        output.write("Special Symbols \n")
                    elif token == ":=":
                        output.write(token)
                        output.write(", ")
                        output.write("Special Symbols \n")
                    else:
                        try:
                            int(token)
                            output.write(token)
                            output.write(", ")
                            output.write("Number \n")
                        except:
                            if len(token) == 0:
                                continue
                            output.write(token)
                            output.write(", ")
                            output.write("Identifier \n")
                    if flag:
                        output.write(";")
                        output.write(", ")
                        output.write("Special Symbol \n")
    return True

scanner()
