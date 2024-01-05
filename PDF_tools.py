# !usr/bin/python
# DATE: NOV 12 2023
# DEVELOPER REDTAIL ZAGT
# LANGUAGE: PYTHON WITH TKINTER 
# MODULES: TKINTER AND PIL TOGETHER WITH PDYPDF



import os
from tkinter import Tk,Label, Button, filedialog, simpledialog, Menu, font
import tkinter as tk
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image

class PDFApp():
    def __init__(self, master):
        self.master = master
        master.title("PDF Toolbox")
        
        
        menubar = Menu(master)
        master.config(menu=menubar)
        
        
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label = "File", menu = file_menu)
        file_menu.add_command(label="Exit", command = master.quit())
        
        custom_font = font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.label = Label(master, text="PDF Toolbox", font = custom_font, fg="Black", bg = "grey")
        self.label.pack()
        
        buttons_frame = tk.Frame(root, bg = "black")
        buttons_frame.pack(fill = tk.BOTH, expand=True, padx = 20 , pady = 40)
    
        self.merge_button = Button(buttons_frame, text="Merge PDFs", command = self.merge_pdfs, bg = "orange", relief = tk.RAISED, borderwidth=3)
        self.merge_button.pack(expand = True, fill = tk.BOTH, padx = 10, pady = 10)
        
        self.convert_doc_button = Button(buttons_frame, text = " Convert Doc to PDF", command = self.convert_to_pdf, bg = "orange", relief = tk.RAISED, borderwidth=3)
        self.convert_doc_button.pack(expand = True, fill = tk.BOTH, padx = 10, pady = 10)
        
        self.convert_img_button = Button(buttons_frame, text="Convert Image to PDF", command=self.convert_to_pdf, bg = "orange", relief = tk.RAISED, borderwidth=3)
        self.convert_img_button.pack(expand = True, fill = tk.BOTH, padx = 10, pady = 10)
        
        self.lock_pdf_button = Button(buttons_frame, text="Lock PDF", command=self.lock_pdf, bg = "orange",relief = tk.RAISED, borderwidth=3)
        self.lock_pdf_button.pack(expand = True, fill = tk.BOTH, padx = 10, pady = 10)
        
        self.convert_img_button = Button(buttons_frame, text="Reset Password", command=self.reset_password_in_main, bg = "orange", relief = tk.RAISED, borderwidth=3)
        self.convert_img_button.pack(expand = True, fill = tk.BOTH, padx = 10, pady = 10)
    
    
    def pdf_operation(input_path, output_path, password, operation):
        input_pdf = PdfReader(input_path)
        
        #check if password is correct for operation specified
        if not input_pdf.decrypt(password):
            print("Incorrect password, Operation aborted.")
            return
        
        output_pdf = PdfWriter()
        
        if operation == 'lock':
            output_pdf.encrypt(password)
            
        elif operation == 'reset':
            new_password = simpledialog.askstring("New Password", "Enter new password for PDF: ")
            
            if new_password:
                output_pdf.encrypt(new_password)
                
            else:
                print("Invalid new password. Operation aborted")
                return
        with open(output_path, 'wb') as output_file:
            output_pdf.write(output_file)
            
        
    def merge_pdfs(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        
        if file_paths:
            merger = PdfMerger()
        
        for path in file_paths:
            merger.append(path)
            
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        
        if output_path:
            with open(output_path, "wb") as output_file:
                merger.write(output_path)
                merger.close()
            
    def convert_to_pdf(self):
        file_path = filedialog.askopenfilename()
        
        if file_path.lower().endswith(('.doc', '.docx')):
            output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", ".pdf")])
            self.convert_doc_to_pdf(file_path, output_path)
            
        elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
            
            output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            self.convert_img_to_pdf(file_path, output_path)
            
    def convert_doc_to_pdf(self, doc_path, pdf_path):
        
        try:
            import docx2pdf
            docx2pdf.convert(doc_path ,pdf_path)
        except ImportError:
            print("Please install the 'python-docx2pdf' Library: pip install docx2pdf")
            
    def convert_img_to_pdf(self, img_path, pdf_path):
        
        from PIL import Image
        image = Image.open(img_path)
        pdf_path = filedialog.asksaveasfilename(defaultextension= ".pdf", filetype = [("Pdf files", "*.pdf")])
        
        if pdf_path:
            
            pdf_path = pdf_path.replace(".pdf", "")# remove the .pdf extension if included
            image.save(pdf_path + ".pdf","PDF", resolution = 100.0)
        
    def lock_pdf(self):
        input_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        
        if input_path:
            
            input_pdf = PdfReader(open(input_path, "rb"))
            output_pdf = PdfWriter()
            
            for page_num in range(len(input_pdf.pages)):
                output_pdf.add_page(input_pdf.pages[page_num])
                
            password = simpledialog.askstring("Password", "Enter password for the PDF: ")
            if password:
                output_pdf.encrypt(password)
                
                output_path = filedialog.asksaveasfilename(defaultextension = ".pdf", filetypes=[("PDF files", "*.pdf")])
                
                if output_path:
                    with open(output_path, "wb") as output_file:
                        output_pdf.write(output_file)
                        
    def reset_password(self,input_path, output_path, current_password, new_password):
        input_pdf = PdfReader(input_path)
        
        # Check the current password
        if not input_pdf.decrypt(current_password):
            print("Incorrect current password. Unable to reset password.")
            return
        
        output_pdf = PdfWriter()
        
        for page_num in range(len(input_pdf.pages)):
            output_pdf.add_page(input_pdf.pages[page_num])
            
        output_pdf.encrypt(new_password)
        
        with open(output_path, 'wb') as output_file:
            output_pdf.write(output_file)
    
    def reset_password_in_main(self):
        
        file_path = filedialog.askopenfilename()
        
        if file_path:
            current_password = simpledialog.askstring("Password", "Enter current passwprd for PDF: ")
            
            if current_password:
                new_password = simpledialog.askstring("New Password", "Enter new password for the PDF: ")
                
                if new_password:
                    output_path = filedialog.askopenfilenames(defaultextension = ".pdf", filetypes = [("PDF files", "*.pdf")])
                    
                    if output_path:
                        self.reset_password(file_path, output_path, current_password, new_password)


if __name__ == "__main__":
    root = Tk()
    width = 300
    height = 500
    root.geometry(f"{width}x{height}")
    root.minsize(width, height)
    root.maxsize(width, height)
    
    root.configure(bg = "#596E7A")
    app = PDFApp(root)
    root.mainloop()