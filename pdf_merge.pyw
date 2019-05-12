import os
import PyPDF2
from tkinter import filedialog
from tkinter import *


def pop_up(msg):
    popup = Toplevel()
    popup.title("PDF Merger")
    popup.resizable(False, False)

    label = Label(popup, text=msg, width=40)
    label.pack()

    button = Button(popup, text="OK", command=popup.destroy,
                    pady=5)
    button.pack()

    popup.mainloop()


def pdf_merge(fileEntry1, fileEntry2, outputEntry):
    try:
        filename1 = fileEntry1.get()
        filename2 = fileEntry2.get()
        outputFilename = outputEntry.get()

        pdfFile1 = open(filename1, 'rb')
        pdfFile2 = open(filename2, 'rb')
    except FileNotFoundError:
        pop_up("Invalid files to merge!")
        return

    pdfReader1 = PyPDF2.PdfFileReader(pdfFile1)
    pdfReader2 = PyPDF2.PdfFileReader(pdfFile2)

    pdfWriter = PyPDF2.PdfFileWriter()

    for page in range(pdfReader1.numPages):
        pageObj = pdfReader1.getPage(page)
        pdfWriter.addPage(pageObj)

    for page in range(pdfReader2.numPages):
        pageObj = pdfReader2.getPage(page)
        pdfWriter.addPage(pageObj)

    try:
        pdfOutput = open(outputFilename, 'wb')
    except FileNotFoundError:
        pop_up("Invalid save location!")
        return

    pdfWriter.write(pdfOutput)
    pdfOutput.close()
    pdfFile1.close()
    pdfFile2.close()
    pop_up('Merged {} and {}!'.format(os.path.basename(filename1),
                                      os.path.basename(filename2)))


def get_pdf_file_1():
    global entry1_stringvar
    filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"),
                                                     ("All files", "*.*")],
                                          title="Choose first PDF")
    entry1_stringvar.set(filename)


def get_pdf_file_2():
    global entry2_stringvar
    filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"),
                                                     ("All files", "*.*")],
                                          title="Choose second PDF")
    entry2_stringvar.set(filename)


def browse_dirs():
    global merged_stringvar
    filename = filedialog.asksaveasfilename(filetypes=[("PDF files", "*.pdf"),
                                                       ("All files", "*.*")],
                                            defaultextension=".pdf",
                                            title="Save merged PDF as...")
    merged_stringvar.set(filename)


# windows and frames
root = Tk()
root.title("PDF Merger")
root.resizable(False, False)

top_frame = Frame(root)
topLeft_frame = Frame(top_frame)
topLeft_entry_frame = Frame(topLeft_frame)
topLeft_label_frame = Frame(topLeft_frame)
topRight_frame = Frame(top_frame)
topRight_entry_frame = Frame(topRight_frame)
topRight_label_frame = Frame(topRight_frame)
middle_frame = Frame(root)
middle_label_frame = Frame(middle_frame)
middle_entry_frame = Frame(middle_frame)
bottom_frame = Frame(root)

# Entrys with StringVars and Labels
entry1_stringvar = StringVar()
entry1 = Entry(topLeft_entry_frame, textvariable=entry1_stringvar, width=40)
entry1_label = Label(topLeft_label_frame, text="Choose first PDF:")

entry2_stringvar = StringVar()
entry2 = Entry(topRight_entry_frame, textvariable=entry2_stringvar,
               width=40)
entry2_label = Label(topRight_label_frame, text="Choose second PDF:")

merged_stringvar = StringVar()
mergedEntry = Entry(middle_entry_frame, textvariable=merged_stringvar,
                    width=40)
merged_label = Label(middle_label_frame, text="Save merged PDF as...")

# browse buttons
browse_button1 = Button(topLeft_entry_frame, text="Browse...",
                        command=lambda: get_pdf_file_1())
browse_button2 = Button(topRight_entry_frame, text="Browse...",
                        command=lambda: get_pdf_file_2())
browse_button3 = Button(middle_entry_frame, text="Browse...",
                        command=lambda: browse_dirs())

# set up main Button
merge_button = Button(bottom_frame, text="Merge!",
                      command=lambda: pdf_merge(entry1_stringvar,
                                                entry2_stringvar,
                                                merged_stringvar))

# packing statements
#  frames
top_frame.pack(side=TOP, padx=3)
topLeft_frame.pack(side=LEFT)
topLeft_label_frame.pack(side=TOP)
topLeft_entry_frame.pack(side=TOP)
topRight_frame.pack(side=LEFT)
topRight_label_frame.pack(side=TOP)
topRight_entry_frame.pack(side=TOP)
middle_frame.pack(side=TOP)
middle_label_frame.pack(side=TOP)
middle_entry_frame.pack(side=TOP)
bottom_frame.pack(side=TOP)

# widgets
entry1_label.pack()
entry1.pack(side=LEFT, fill=X, expand=1, padx=5)
browse_button1.pack(side=LEFT, pady=5)
entry2_label.pack()
entry2.pack(side=LEFT, fill=X, expand=1, padx=5)
browse_button2.pack(side=LEFT, pady=5)
merged_label.pack()
mergedEntry.pack(side=LEFT, fill=X, expand=1, padx=5)
browse_button3.pack(side=LEFT, pady=5)
merge_button.pack(pady=5)

# initiate
root.mainloop()
