import pytesseract as pt, os

from tkinter import filedialog, Button, Label, messagebox
from tkinter.ttk import *
from tkinter import *

try:
    from PIL import Image
except ImportError:
    import Image
    
"""To Do: 
Make program executable
"""

#Global Variables
glob_select_folder = None
glob_destination_folder = None

def sel_popup():
    root = Tk()
    root.directory = filedialog.askdirectory()
    sel_path_lbl = Label(program, text=root.directory)
    sel_path_lbl.pack()  
    sel_path_lbl.place(x = 35, y = 32)
    global glob_select_folder
    glob_select_folder= str(root.directory)
    root.destroy()
    
def dest_popup():
    root = Tk()
    root.directory = filedialog.askdirectory()
    dest_path_lbl = Label(program, text=root.directory)
    dest_path_lbl.pack()  
    dest_path_lbl.place(x = 35, y = 84)  
    global glob_destination_folder 
    glob_destination_folder= str(root.directory)
    root.destroy()

#Main Program
def ocr():
    # If you don't have tesseract executable in your PATH, inc the following:
    pt.pytesseract.tesseract_cmd = \
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    
    text_list = []
    file_count = 0
    counter = 0
    global glob_select_folder
    global glob_destination_folder
    if glob_select_folder == None or glob_destination_folder == None:
        messagebox.showerror("Error", "Please select folders!")
        
    #Counts number of files in folder
    for file in os.listdir(glob_select_folder):
        file_count += 1
        
    #Heavy lifting iterater
    for file in os.listdir(glob_select_folder):
        #Progress bar code
        if counter == file_count/4:
            progress['value'] = 25
            program.update_idletasks()
        elif counter == file_count/2:
            progress['value'] = 50
            program.update_idletasks()
        elif counter == (file_count/4)*3:
            progress['value'] = 75
            program.update_idletasks()
        #Converts img file to text and saves as variable
        text = \
        pt.image_to_string(Image.open(os.path.join(glob_select_folder, file)))
        text_list.append(text + '\n\n\n')
        counter += 1
        
    progress['value'] = 90
    program.update_idletasks()
    num = 2
    filename = r'\screenshots.txt'
    #Checks if the file screenshots.txt already exists
    while os.path.exists(glob_destination_folder + filename):
            filename = r'\screenshots%s.txt' % (num)
            num += 1
    #Writes to the txt file
    with open(glob_destination_folder + filename,
              'a+', encoding='utf-8') as f:
        for item in text_list:
            f.write(str(file) + ': \n' + item)
            
    progress['value'] = 100

#Makes the main program popup    
program = Tk()
program.geometry("400x200")
program.title("Image to Text Converter")

#First grouping of lbls and btns for selecting folder of pics
sel_lbl = Label(program, text='Choose a folder with only images in it:')
sel_lbl.pack()  
sel_lbl.place(x = 20, y = 8) 
sel_btn = Button(program, text = "\\", command = sel_popup)
sel_btn.place(x = 20, y = 30)

#Second grouping of lbls and btns for selecting destination folder of txt doc
dest_lbl = Label(program, text="Choose a location for your text document:")
dest_lbl.pack()  
dest_lbl.place(x = 20, y = 60) 
dest_btn = Button(program, text = "\\", command = dest_popup)
dest_btn.place(x = 20, y = 82)

#Execute btn
run_btn = Button(program, text = "Execute", command = ocr)
run_btn.place(x = 150, y = 120)

#Progress bar
progress = Progressbar(program, orient = HORIZONTAL, length = 310,
                       mode = 'determinate') 
progress.pack(pady = 10)
progress.place(x = 20, y = 155)

program.mainloop()
    
