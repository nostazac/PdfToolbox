; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
AppName = PDFtools
AppVersion = 1.0
DefaultDirName = {pf}\PDFtools
OutputDir = Output
OutputBaseFilename = PdftoolSetup
Compression = lzma
SolidCompression = yes

[Files]
Source: "dist\*"; DestDir:"(PDF_tools)"

[Icons]
Name: "commondesktop}\PDFtools"; Filename: "{PDF_tools}\PDFtools.exe"

