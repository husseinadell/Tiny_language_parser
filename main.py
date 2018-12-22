import tkinter as tk
from parser import Parser, Node, tokenizer
from scanner import scanner


class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Parser")

        self.label = tk.Label(master, text="This is our Tiny language cool parser!")
        self.label.config(font=('Courier', 20))
        self.label.pack()

        self.label = tk.Label(master, text="please enter the file name and make sure it's in the same project folder")
        self.label.config(font=('TimesNewRoman', 15))
        self.label.pack()

        self.text_box = tk.Entry()
        self.text_box.pack(padx=100, pady=10)

        self.greet_button = tk.Button(master, text="Parse!", command=self.parse)
        self.greet_button.pack()

        self.close_button = tk.Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def parse(self):
        # print(self.text_box.get())
        scanner(self.text_box.get())
        lst_tokens = tokenizer(file='output.txt')
        init_node = Node()
        parser = Parser(lst_tokens)
        parser.parents.append(init_node.index)
        parser.program()
        parser.draw_tree()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")
    my_gui = MyFirstGUI(root)
    root.mainloop()

