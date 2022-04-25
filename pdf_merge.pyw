from pikepdf import Pdf
from tkinter import filedialog
import tkinter as tk


class ListOfEntries():
    def __init__(self, parent, entries_list=[]):
        self.parent = parent
        self.entries_list = entries_list
        self.add_entry()

    def add_entry(self, text=''):
        if len(self.entries_list) > 0:
            self.entries_list[len(self.entries_list) - 1].insert(0, text)

        new_entry = tk.Entry(self.parent, width=40)
        self.entries_list.append(new_entry)
        self.pack_in()

    def pack_in(self):
        for entry in self.entries_list:
            entry.pack(side=tk.TOP, anchor='s')


class LabelledBrowseBox():
    def __init__(self, parent, label_text, title, button_label,
                 name='', open=True):
        self.parent = parent
        self.name = tk.StringVar()
        self.name.set(name)
        self.label_text = label_text
        self.title = title
        self.label = tk.Label(self.parent, text=self.label_text, width=40)
        self.entry = tk.Entry(self.parent, textvariable=self.name)
        if open:
            self.button = tk.Button(self.parent, text=button_label,
                                    command=self.open_pdf)
        else:
            self.button = tk.Button(self.parent, text=button_label,
                                    command=self.save_pdf)

    def pack_in(self):
        self.label.pack(side=tk.TOP)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=5)
        self.button.pack(side=tk.LEFT, pady=5)

    def open_pdf(self):
        filename = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf"),
                       ("All files", "*.*")],
            title=self.title)
        self.name.set(filename)

    def save_pdf(self):
        filename = filedialog.asksaveasfilename(
            filetypes=[("PDF files", "*.pdf"),
                       ("All files", "*.*")],
            defaultextension=".pdf",
            title=self.title)
        self.name.set(filename)


def pop_up(msg):
    popup = tk.Toplevel()
    popup.title("PDF Merger")
    popup.resizable(False, False)

    label = tk.Label(popup, text=msg, width=40)
    label.pack()

    button = tk.Button(popup, text="OK", command=popup.destroy,
                       pady=5)
    button.pack()

    popup.mainloop()


def pdf_merge(content_list, output_entry):
    filenames_list = []

    output_filename = output_entry.get()

    for content in content_list:
        if content.get() != '':
            filenames_list.append(content.get())
        else:
            continue

    pdf = Pdf.new()

    for filename in filenames_list:
        src = Pdf.open(filename)
        pdf.pages.extend(src.pages)

    pdf.save(output_filename)

    pop_up('Merged files!')


def check_not_empty(list, box_content):
    if box_content.get() != '':
        list.add_entry(box_content.get())


# windows and frames
root = tk.Tk()
root.title("PDF Merger")
root.resizable(False, False)

top_frame = tk.Frame(root)
top_right_frame = tk.Frame(top_frame)
middle_frame = tk.Frame(root)
bottom_frame = tk.Frame(root)

# Entrys
entry = LabelledBrowseBox(top_frame, "Choose next PDF: ",
                          "Choose next PDF...", "Browse...")

entry_list = ListOfEntries(top_right_frame)

output_entry = LabelledBrowseBox(middle_frame, "Save merged PDF as: ",
                                 "Save merged PDF as...", "Browse...",
                                 open=False)

# other buttons
add_button = tk.Button(top_frame, text=">",
                       command=lambda: (check_not_empty(entry_list,
                                                        entry.name),
                                        entry.name.set('')))

merge_button = tk.Button(bottom_frame, text="Merge!",
                         command=lambda: pdf_merge(entry_list.entries_list,
                                                   output_entry.name))

# packing statements
#  frames
top_frame.pack(side=tk.TOP, padx=3)
top_right_frame.pack(side=tk.RIGHT)
middle_frame.pack(side=tk.TOP)
bottom_frame.pack(side=tk.TOP)

# widgets
entry.pack_in()
output_entry.pack_in()
add_button.pack(side=tk.LEFT, padx=5)
merge_button.pack(pady=5)

# initiate
root.mainloop()
