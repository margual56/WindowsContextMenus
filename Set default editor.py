from tkinter import filedialog as fd
import codecs
import os

filename = fd.askopenfilename(title="Select the editor executable", filetypes=(("Executable files", "*.exe"),))
filename += " %1"

print(filename)

processed = ""
for letter in filename:
    processed += str(codecs.encode(bytes(letter, encoding='utf-8'), "hex"), 'utf-8') + ",00,"

processed += "00,00"

print(processed)

extension = input("\n\nExtension of the file (without the dot):\n> ")
key = extension + "file"
print(key)

description = input("File description")

template = fd.askopenfilename(title="Select template file", filetypes=(("Template", "." + extension),))
icon = fd.askopenfilename(title="Select the icon for the file", filetypes=(("Icon", ".ico"),))
if not template == '':
    os.system("copy \"template\" \"%appdata%\\Microsoft\\Windows\\Templates\"")

with open("setEditProgram.reg", 'w') as f:
    f.write("Windows Registry Editor Version 5.00\n")
    f.write("[HKEY_CLASSES_ROOT\\." + extension + "]\n")
    f.write("@= \"" + key + "\"\n")

    # template
    f.write("[HKEY_CLASSES_ROOT\\." + extension + "\\ShellNew]\n")
    if not template == '':
        f.write("\"Filename\" = \"" + template.split("/")[len(template.split("/"))-1] + "\"\n")
    else:
        f.write("\"Filename\" = \"\"\n")

    # file type name
    f.write("[HKEY_CLASSES_ROOT\\" + key + "]\n")
    f.write("@= \"" + description + "\"\n")

    # "edit" button's default editor
    f.write("[HKEY_CLASSES_ROOT\\" + key + "\\shell\\edit]\n")
    f.write("[HKEY_CLASSES_ROOT\\" + key + "\\shell\\edit\\command]\n")
    f.write("@=hex(2):" + processed)

    f.write("[HKEY_CLASSES_ROOT\\" + key + "\\DefaultIcon]\n")
    f.write("@= \"" + icon + "\"\n")
