# tkinter
from tkinter import filedialog
# custom tkinter
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
# utils
import os
# import random
import datetime as dt
from PIL import Image
import glob
# from OpenSSL import crypto
# from Crypto.PublicKey import ECC
# signing
from cert_make import Certificate
from pyhanko.keys import load_cert_from_pemder
from pyhanko_certvalidator import ValidationContext
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import validate_pdf_signature
from pyhanko.sign.validation.settings import KeyUsageConstraints


f = ("Times bold", 14)
root_cert = load_cert_from_pemder('CA/ca.pem')
vc = ValidationContext(trust_roots=[root_cert])

app = ctk.CTk()

app.title("Validación Firma Electrónica")
app.eval("tk::PlaceWindow . center")
# app.maxsize(900,  600)
app.geometry("300x400")
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("light")
# self.geometry('600x400')
# self['bg'] = '#5d8a82'
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=9)
app.grid_rowconfigure(2, weight=1)

f = ("Times bold", 14)

image_frame = ctk.CTkFrame(app, width=300,  height=80)
image_frame.grid(row=0, column=0, sticky="nsew")

my_image = ctk.CTkImage(light_image=Image.open("TEC-logo.png"),
                        dark_image=Image.open("TEC-logo.png"),
                        size=(280, 80))

image_label = ctk.CTkLabel(image_frame, image=my_image, text="").grid(
    row=0,  column=0,  padx=5,  pady=5)

container = ctk.CTkFrame(app, width=300,  height=220)
container.grid(row=1, column=0, sticky="nsew")

container.columnconfigure(0, weight=1)
container.rowconfigure((0, 1), weight=1)

output_frame = ctk.CTkFrame(app, width=300,  height=100)
output_frame.grid(row=2, column=0, sticky="nsew")
output_frame.columnconfigure(0, weight=1)
output_frame.rowconfigure(0, weight=1)
# self.columnconfigure(0, weight=1)
# self.rowconfigure(0, weight=1)
# self.rowconfigure(1, weight=3)
#label = ctk.Label(self, text="Main Page")
#label.pack(padx=10, pady=10)

# validar uno
ctk.CTkButton(
    container,
    text="Validar uno",
    font=f,
    # width=25,
    # height=2,
    command=lambda: validate_one()
).grid(row=0,  column=0,  padx=20,  pady=20, sticky='ew')
#generate_sign.place(relx=0.5, rely=0.25, relwidth=0.9)

# validar muchos
ctk.CTkButton(
    container,
    text="Validar más",
    font=f,
    # width=25,
    # height=2,
    command=lambda: validate_more()
).grid(row=1,  column=0,  padx=20,  pady=20, sticky='ew')


def validate_one():
    # if not os.path.exists('firmados'):
    #     print("Creating CA driectory")
    # os.makedirs('CA')

    file = filedialog.askopenfile(
        initialdir="/Documents/documentos/firmados", title="Select Diploma", filetypes=[("pdf files", "*.pdf")]
    )
    try:
        with open(file.name, 'rb') as doc:
            r = PdfFileReader(doc)
            sig = r.embedded_signatures[0]
            status = validate_pdf_signature(sig, vc,
                                            key_usage_settings=KeyUsageConstraints(key_usage={'digital_signature'}))
            print(status.bottom_line)

        if status.bottom_line:
            CTkMessagebox(message="El certificado seleccionado es válido",
                          icon="check", option_1="Cerrar")
        else:
            CTkMessagebox(title="Error", message="El certificado seleccionado es inválido",
                          icon="cancel")

    except IndexError:
        CTkMessagebox(title="Advertencia", message="El certificado no tiene firma",
                      icon="warning", option_1="Cerrar")


def validate_more():
    # if not os.path.exists('firmados'):
    #     print("Creating CA driectory")
    #     os.makedirs('CA')

    directory = filedialog.askdirectory(
        initialdir="/Documents/firma", title="Save Sign"
    )
    iterator = glob.glob(os.path.join(directory, "*.pdf"))

    invalidos = []

    if len(iterator) > 0:
        for item in iterator:
            try:
                with open(item, 'rb') as doc:
                    r = PdfFileReader(doc)
                    sig = r.embedded_signatures[0]
                    status = validate_pdf_signature(sig, vc,
                                                    key_usage_settings=KeyUsageConstraints(key_usage={'digital_signature'}))
                    print(status.bottom_line)
                    if status.bottom_line == False:
                        invalidos.append(item.split('/')[-1])

            except IndexError:
                invalidos.append(item.split('/')[-1])

    if len(invalidos) > 0:
        CTkMessagebox(title="Error", message="Existen documentos inválidos",
                      icon="cancel")
        textbox = ctk.CTkTextbox(master=output_frame, height=100)
        textbox.grid(row=0, column=0, sticky="ew")
        for i, file in enumerate(invalidos):
            textbox.insert(f"{i}.0", f"{file}\n")
        textbox.configure(state="disabled")

    else:
        CTkMessagebox(message="Los documentos son válidos",
                      icon="check", option_1="Cerrar")

        ##########################################################################
        ##########################################################################


app.mainloop()
