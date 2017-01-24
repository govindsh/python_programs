#Python Imports
from Tkinter import *
import tkMessageBox
import os
from ScrolledText import ScrolledText
import fnmatch
from re import search
import time
import math

class File_search:
    # Constructor
    def __init__(self,master):
        
        # To run debug on, change variable to True
        self.debug = False
        filename_cache = 'cache.txt'
        
        # We create three frames. Top, main, bottom frames. Some prefer grid manager.
        self.top_frame = Frame(master,bg='#f4d142')
        self.top_frame.pack(side=TOP)
        
        # Main frame
        frame = Frame(master,bg='#ddd6d4')
        frame.pack(fill='y', expand=True)
        
        # Bottom frame
        self.bottom_frame = Frame(master,bg='#bcecf2')
        self.bottom_frame.pack(side=BOTTOM)

        if os.path.isfile(filename_cache):
            self.Log("File exists")
            # Read contents of file and append contents to listbox
            fh = open(filename_cache,'r')
            self.file_list = fh.readlines()
            fh.close()
            self.file_list_box_label = Label(frame,text="Recently searched files",bg='#ddd6d4')
            self.file_list_box_label.pack(side=TOP)
            self.file_list_box = Listbox(frame,selectmode=SINGLE,bg='#ddd6d4')
            self.file_list_box.pack(side=TOP)
            for item in self.file_list:
                self.file_list_box.insert(END,item)
        else:
            self.Log("File does not exists")

        # Labels and entry's for accepting input
        file_label = Label(self.top_frame,text="Filename",bg='#f4d142')
        file_label.pack(side=LEFT)
        
        self.file_name = Entry(self.top_frame,bg='#f4d142')
        self.file_name.pack(side=LEFT)
        
        dir_label = Label(self.top_frame,text="Directory (where file might be) **",bg='#f4d142')
        dir_label.pack(side=LEFT,pady=50)
        
        self.dir_name = Entry(self.top_frame,bg='#f4d142')
        self.dir_name.pack(side=LEFT)
        
        note_label = Label(frame,text="** If this is empty then the current working directory is taken",bg='#ddd6d4')
        note_label.pack(side=BOTTOM)
        
        # Create search button
        self.search = Button(frame,text="Search",command=self.search_file,bg='#ddd6d4')
        self.search.pack(side=LEFT,padx=10)
        
        # Create cache button
        self.cache = Button(frame,text="Cache filename",command=self.write_filename_for_caching,bg='#ddd6d4')
        self.cache.pack(side=LEFT,padx=10)
        
        # Create clear button
        self.clear = Button(frame,text="Clear Fields",command=self.clear_text,bg='#ddd6d4')
        self.clear.pack(side=LEFT,padx=10)
        
        # Label and text box for displaying output
        self.output_label = Label(self.bottom_frame,text="Search output:",bg='#bcecf2')
        self.output_label.pack(side=TOP)
        
        self.output = ScrolledText(self.bottom_frame,bg='#D66B54') # ScrolledText looks better. Can use Text as well.
        self.output['font'] = ('monaco','12')
    
    def check_dir_access(self,cwd):
        """ Function to check access to file """
        if os.path.exists(cwd):
            return True
        else:
            return False
    
    def clear_text(self,time_labels=0):
        """ Function to clear text and labels after search is clicked """
        dummy = 0
        if time_labels == 0:
            self.output.delete(1.0,END)
            self.file_name.delete(0,END)
            self.dir_name.delete(0,END)
        if time_labels == 1:
            try:
                self.time_label.pack_forget()
                self.time_taken_label.pack_forget()
            except AttributeError:
                dummy=1
        return

    def write_filename_for_caching(self):
        """ Write filename (that returns success for search) to file """ 
        try:
            if self.success == True:
                self.output.delete(1.0, END)
                filename_cache = 'cache.txt' # created in current working directory
                filename_to_write = self.file_name.get()
                filename_to_write = filename_to_write.strip()
                fh = open(filename_cache,'a')
                fh.write(filename_to_write + "\n")
                fh.close()
                self.output.text = "Cache updated successfully!"
                self.output.insert(1.0, self.output.text)
                if filename_to_write not in self.file_list:
                    self.file_list_box.insert(END,filename_to_write)
                else:
                    self.output.text = "File already in cache!"
                    self.output.insert(END, self.output.text)
        except AttributeError:
            # If button is clicked with empty filename or before searching, throw error
            tkMessageBox.showinfo('Note','File name has to be searched before caching')
        return

    def search_file(self):
        # Clear time labels if search if performed more than once
        self.clear_text(time_labels=1)
        
        # Start timer
        start_time = time.time()
        
        # Delete any existing output
        self.output.delete(1.0,END)
        
        # Empty array
        paths = []
        
        # Get input from ENTRY boxes
        dir_name = self.dir_name.get()
        dir_name = dir_name.strip()
        if dir_name is '':
            cwd = '.'
        else:
            cwd = dir_name
            bool = self.check_dir_access(cwd)
            if bool == False:
                tkMessageBox.showerror("Error", "Directory doesn't exist. Please check spelling.")
            
        search_file = self.file_name.get()
        search_file = search_file.strip()

        # Validate empty inputs
        if search_file == '' and self.file_list_box.curselection() == []:
            tkMessageBox.showerror('Select one...','Enter filename or choose one file from listbox')

        if search_file == '':
            if self.file_list_box.curselection() != []:
                self.file_name.insert(0, self.file_list_box.get(self.file_list_box.curselection()))
        
        search_file = self.file_name.get()
        search_file = search_file.strip()

        # Validate wildcard
        if '*' not in search_file:
            # No wildcard
            for root, dirs, files in os.walk(cwd):
                for filename in files: 
                    if filename.lower() == search_file.lower():
                        paths.append(os.path.abspath(root) + '/' + filename)
        else:
            # Wildcard match
            for root, dirs, files in os.walk(cwd): 
                for filename in files:
                    if fnmatch.fnmatch(filename.lower(),search_file.lower()):
                        paths.append(os.path.abspath(root) + '/' + filename)
        
        # If found update output with paths
        if len(paths) > 0:
            self.Log(str(len(paths)) + " file(s) found ")
            self.output.text = str(len(paths)) + " files found with name " + search_file + "\n\n"
            for path in paths:
                self.success = True
                self.Log("File found at ---> "+ str(path) + "\n")
                self.output.text += str(path) + "\n"
        # Else -> error
        else:
            self.output.text = "Error: File not found."
            self.Log("File not found")
        
        # Display time taken
        done_time = time.time()
        time_taken = done_time - start_time
        time_taken = math.ceil(time_taken)
        
        self.time_taken_label = Label(self.bottom_frame,text=str(time_taken) + " second(s)",bg='#bcecf2')
        self.time_taken_label.pack(side=BOTTOM)
        
        self.time_label = Label(self.bottom_frame,text="Time taken: ",bg='#bcecf2')
        self.time_label.pack(side=BOTTOM)
        
        # Insert output text in ScrolledText
        self.output.insert(1.0,self.output.text)
        self.output.pack(side=BOTTOM)
        
        return
    
    
    def Log(self,msg):
        """ Function to print debug messages """
        if self.debug == True:
            print msg
        return

# Create app instance and run
root = Tk()
root.wm_title("File Search")
fs_app = File_search(root)

root.mainloop()

    
