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
from pyhanko import stamp
from pyhanko.pdf_utils import text
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import fields, signers


# class MyFrame(ctk.CTkFrame):
#     def __init__(self, parent, **kwargs):
#         super().__init__(parent, **kwargs)
# add widgets onto the frame, for example:
# self.label = ctk.CTkLabel(self)
# self.label.grid(row=0, column=0)
f = ("Times bold", 14)


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):

        ctk.CTk.__init__(self, *args, **kwargs)
        self.title("Firma Electrónica")
        self.eval("tk::PlaceWindow . center")
        # self.maxsize(900,  600)
        self.geometry("300x400")
        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode("light")
        # self.geometry('600x400')
        # self['bg'] = '#5d8a82'
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)

        self.f = ("Times bold", 14)

        image_frame = ctk.CTkFrame(self, width=300,  height=100)
        image_frame.grid(row=0, column=0, sticky="nsew")

        my_image = ctk.CTkImage(light_image=Image.open("TEC-logo.png"),
                                dark_image=Image.open("TEC-logo.png"),
                                size=(280, 80))

        image_label = ctk.CTkLabel(image_frame, image=my_image, text="").grid(
            row=0,  column=0,  padx=5,  pady=5)

        container = ctk.CTkFrame(self, width=300,  height=300)
        container.grid(row=1, column=0, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # We will now create a dictionary of frames
        self.frames = {}
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (MainPage, PageOne, PageTwo):
            frame = F(container, self)
            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Using a method to switch frames
        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top_frame
        frame.tkraise()


##########################################################################
##########################################################################


class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        # # Create left and right frames
        # left_frame  =  ctk.CTkFrame.__init__(self, parent, width=200,  height=  400,  bg='grey')
        # left_frame.grid(row=0,  column=0,  padx=10,  pady=5)

        # right_frame  = ctk.CTkFrame.__init__(self, parent, width=650,  height=400,  bg='grey')
        # right_frame.grid(row=1,  column=0,  padx=10,  pady=5)

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1), weight=1)
        #label = ctk.Label(self, text="Main Page")
        #label.pack(padx=10, pady=10)

        # ir a página generar
        ctk.CTkButton(
            self,
            text="Generar Llave",
            font=f,
            # width=25,
            # height=2,
            command=lambda: controller.show_frame(PageOne)
        ).grid(row=0,  column=0,  padx=20,  pady=10, sticky='ew')
        #generate_sign.place(relx=0.5, rely=0.25, relwidth=0.9)

        # ir a página firmar
        button_firma = ctk.CTkButton(
            self,
            text="Firmar",
            font=f,
            # width=25,
            # height=2,
            command=lambda: controller.show_frame(PageTwo)
        ).grid(row=1,  column=0,  padx=20,  pady=10, sticky='ew')

        # button_firma.cget('fg_color')

##########################################################################
##########################################################################


class PageOne(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2), weight=1)

        # titulo
        if os.path.exists('CA/fecha.txt'):
            file = open(os.path.join("CA/fecha.txt"), "r")
            contenido = file.readline()
            label = ctk.CTkLabel(
                self, text=f'Última llave generada el \n {str(contenido)}', font=ctk.CTkFont(family="Times bold", size=14))
            file.close()
        else:
            contenido = "Generar llave por primera vez"
            label = ctk.CTkLabel(
                self, text=contenido, font=f)

        label.grid(row=0,  column=0,  padx=20,  pady=20, sticky='ew')

        # generar llave
        generate_sign_button = ctk.CTkButton(
            self,
            text="Generar llave privada",
            font=f,
            command=lambda: self.generate_ca(generate_sign_button)
        )
        generate_sign_button.grid(
            row=1,  column=0,  padx=20,  pady=20, sticky='ew')

        # regresar
        switch_window_button = ctk.CTkButton(
            self,
            text="Regresar",
            font=f,
            command=lambda: controller.show_frame(MainPage),
        )
        switch_window_button.grid(
            row=2,  column=0,  padx=20,  pady=20, sticky='ew')

    def set_contenido(self, contenido):
        self.contenido = contenido

    def generate_ca(self, button):
        if not os.path.exists('CA'):
            print("Creating CA driectory")
            os.makedirs('CA')

        directory = filedialog.askdirectory(
            initialdir="/Documents/firma", title="Save Sign"
        )
        if directory != (''):
            button.configure(fg_color='orchid3')

            print("Generating certificates")

            cls = Certificate()
            cls.CA()
            # Save date
            now = dt.datetime.now()

            with open(os.path.join(directory, "fecha.txt"), "wt") as f:
                f.write(str(now.strftime("%d/%m/%Y, %H:%M:%S")))
            self.set_contenido(str(dt.date.today()))

            label = ctk.CTkLabel(
                self, text=f'Última llave generada el \n {str(now.strftime("%d/%m/%Y, %H:%M:%S"))}', font=ctk.CTkFont(family="Times bold", size=14))
            label.grid(row=0,  column=0,  padx=20,  pady=20, sticky='ew')

            CTkMessagebox(title="Directorio selecionado", message=directory)


##########################################################################
##########################################################################


class PageTwo(ctk.CTkFrame):
    def __init__(self, parent, controller):
        global color
        ctk.CTkFrame.__init__(self, parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        # archivo
        select_file_button = ctk.CTkButton(
            self,
            text="Select Diploma",
            font=f,
            command=lambda: self.open_file(
                select_file_button, select_files_button)
        )
        select_file_button.grid(
            row=0,  column=0,  padx=20,  pady=8, sticky='ew')

        # archivos
        select_files_button = ctk.CTkButton(
            self,
            text="Select Diploma",
            font=f,
            command=lambda: self.open_many_files(
                select_files_button, select_file_button)
        )
        select_files_button.grid(
            row=0,  column=1,  padx=20,  pady=8, sticky='ew')

        # llave privada
        select_key_button = ctk.CTkButton(
            self,
            text="Select Private Key",
            font=f,
            command=lambda: self.open_key(select_key_button)
        )
        select_key_button.grid(
            row=1,  column=0,  padx=20,  pady=8, sticky='ew', columnspan=2)

        # certificado
        select_cert_button = ctk.CTkButton(
            self,
            text="Select Certificate",
            font=f,
            command=lambda: self.open_cert(select_cert_button)
        )
        select_cert_button.grid(
            row=2,  column=0,  padx=20,  pady=8, sticky='ew', columnspan=2)

        # firmar
        one_sign_button = ctk.CTkButton(
            self,
            text="Firmar Uno",
            font=f,
            command=lambda: self.sign_one(one_sign_button)
        )
        one_sign_button.grid(
            row=3,  column=0,  padx=20,  pady=8, sticky='ew', columnspan=2)

        # firmar
        # many_sign_button = ctk.CTkButton(
        #     self,
        #     text="Firmar Más",
        #     font=f,
        #     command=lambda: self.sign_many(many_sign_button)
        # )
        # many_sign_button.grid(
        #     row=3,  column=1,  padx=20,  pady=8, sticky='ew')

        # regresar
        switch_window_button = ctk.CTkButton(
            self,
            text="Return to menu",
            font=f,
            command=lambda: controller.show_frame(MainPage)
        )
        switch_window_button.grid(
            row=4,  column=0,  padx=20,  pady=30, sticky='ew', columnspan=2)

    def open_file(self, button, other_button):
        global file
        file = filedialog.askopenfile(
            initialdir="/Documents/firma", title="Select Diploma", filetypes=[("pdf files", "*.pdf")]
        )

        if file != None:
            button.configure(fg_color='orchid3')
            other_button.configure(fg_color='#3B8ED0')
            CTkMessagebox(title="Archivo selecionado", message=file.name)

    def open_many_files(self, button, other_button):
        global file
        file = filedialog.askdirectory(
            initialdir="/Documents/firma", title="Save Sign"
        )

        if file != (''):
            if len(glob.glob(os.path.join(file, "*.pdf"))) > 0:
                button.configure(fg_color='orchid3')
                other_button.configure(fg_color='#3B8ED0')
                CTkMessagebox(title="Archivos selecionado",
                              message=f"Carpeta '{file.split('/')[-1]}' seleccionada")

    def open_key(self, button):
        global key_name
        key_name = filedialog.askopenfile(
            initialdir="/Documents/firma", title="Select Private Key", filetypes=[("private keys", "*.key")]
        )
        if key_name != None:
            button.configure(fg_color='orchid3')
            CTkMessagebox(title="Llave selecionada", message=key_name.name)

    def open_cert(self, button):
        global cert_name
        cert_name = filedialog.askopenfile(
            initialdir="/Documents/firma", title="Select Certificate", filetypes=[("certificates", "*.pem")]
        )
        if cert_name != None:
            button.configure(fg_color='orchid3')
            CTkMessagebox(title="Certificado selecionado",
                          message=cert_name.name)

    def load_sign(self, root_ca_path, key_path, file, name=False):
        ''' Load CA and Key'''

        signer = signers.SimpleSigner.load(
            key_path, root_ca_path, key_passphrase=b'1234'
        )

        with open(file, 'rb') as inf:
            w = IncrementalPdfFileWriter(inf)
            fields.append_signature_field(
                w, sig_field_spec=fields.SigFieldSpec(
                    'Signature', box=(200, 200, 400, 250)
                )
            )

            meta = signers.PdfSignatureMetadata(field_name='Signature',
                                                signer_key_usage='digital_signature')
            pdf_signer = signers.PdfSigner(
                meta, signer=signer, stamp_style=stamp.TextStampStyle(
                    # the 'signer' and 'ts' parameters will be interpolated by pyHanko, if present
                    stamp_text='Signed by: %(signer)s\nTime: %(ts)s',
                    text_box_style=text.TextBoxStyle()
                ),
            )

            if name != False:
                with open(f"documentos_firmados/{name}-signed.pdf", 'wb') as outf:
                    pdf_signer.sign_pdf(w, output=outf)
            else:
                with open(f"documentos_firmados/{file.split('/')[-1]}-signed.pdf", 'wb') as outf:
                    pdf_signer.sign_pdf(w, output=outf)

    def sign_one(self, button):
        if not os.path.exists('documentos_firmados'):
            os.makedirs('documentos_firmados')

        if type(file) == str:
            try:
                for f in glob.glob(os.path.join(file, "*.pdf")):
                    self.load_sign(cert_name.name, key_name.name, f)

                    # button.configure(fg_color='orchid3')
                CTkMessagebox(message="Diplomas firmado digitalmente",
                              icon="check", option_1="Cerrar")
            except NameError:
                CTkMessagebox(title="Error",
                              message="Primero selecciona todos los archivos",
                              icon="cancel")

        else:
            try:
                self.load_sign(cert_name.name, key_name.name,
                               file.name, file.name.split('/')[-1])
                CTkMessagebox(message="Diploma firmado digitalmente",
                              icon="check", option_1="Cerrar")
                # button.configure(fg_color='orchid3')
            except NameError:
                CTkMessagebox(title="Error",
                              message="Primero selecciona todos los archivos",
                              icon="cancel")
        # CTkMessagebox(message="Diploma firmado digitalmente",
        #               icon="check", option_1="Cerrar")


app = App()
app.mainloop()


# def nextPage():
#     app.destroy()
#     import pag_02


# def prevPage():
#     app.destroy()
#     import pag_03


# main_frame = tk.Frame(ws,  width=300,  height=600,  bg='grey')
# main_frame.grid(row=0,  column=0,  padx=40,  pady=40)

# tk.Label(main_frame,  text="Menú principal",  relief=tk.RAISED, bg='#5d8a82',
#          font=f).grid(row=0,  column=0,  padx=20,  pady=20)

# tk.Label(
#     ws,
#     text="Menú principal",
#     padx=20,
#     pady=20,
#     bg='#5d8a82',
#     font=f
# ).pack(expand=True, fill=tk.BOTH)

# ctk.CTkButton(
#     app,
#     text="Generar Llave",
#     font=f,
#     # width=25,
#     # height=2,
#     command=nextPage
# ).grid(row=0,  column=0,  padx=20,  pady=20, sticky='ew')

# ctk.CTkButton(
#     app,
#     text="Firmar",
#     font=f,
#     # width=25,
#     # height=2,
#     command=prevPage
# ).grid(row=1,  column=0,  padx=20,  pady=20, sticky='ew')

# # run app
# app.mainloop()

######################################################################
######################################################################
######################################################################
