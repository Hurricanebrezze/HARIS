from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
#from PIL import ImageTk, Image # Keep this commented out as per instruction
# Set of registered names
names = set()

# --- Main Application Class ---
class HARIS_App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        
        # Load names from file
        try:
            with open("nameslist.txt", "r") as f:
                x = f.read()
                z = x.rstrip().split(" ")
                for i in z:
                    if i: # Only add non-empty strings
                        names.add(i)
        except FileNotFoundError:
             # Create file if it doesn't exist
            open("nameslist.txt", "w").close()

        self.title_font = tkfont.Font(family='Helvetica', size=24, weight="bold")
        self.title("HARIS")
        
        # --- Full Screen Setup ---
        self.state('zoomed') # Maximize window
        
        # Fallback for full screen dimensions (useful if 'zoomed' fails or for initial calculations)
        # self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}") 
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        self.num_of_images = 0 # Initialize image count
        
        # Container to hold all frames/pages
        container = tk.Frame(self, bg="black")
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            # Save all names back to file
            with open("nameslist.txt", "w") as f:
                f.write(" ".join(filter(None, names))) # Filter None/empty strings
            self.destroy()

# --- Utility Function for Centering Buttons (Grid Manager) ---
def center_grid_widgets(frame, rows, columns):
    """Configures rows/columns to center widgets in a grid layout."""
    for i in range(rows):
        frame.grid_rowconfigure(i, weight=1)
    for j in range(columns):
        frame.grid_columnconfigure(j, weight=1)
    

# --- StartPage (Home Page) ---
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="black")
        self.controller = controller
        
        # Load and center image
        try:
            render = PhotoImage(file='homepagepic.png')
            img = tk.Label(self, image=render, bg="black")
            img.image = render
            img.grid(row=1, column=0, columnspan=2, pady=50, sticky="n") # Sifted to column 0, center-aligned by grid config
        except Exception:
            # Placeholder if image file is missing
            img = tk.Label(self, text="[Image Placeholder]", fg="white", bg="black", font=controller.title_font)
            img.grid(row=1, column=0, columnspan=2, pady=50, sticky="n")

        # Title Label
        label = tk.Label(self, text="Hello, I am HARIS...", font=self.controller.title_font, fg="white", bg="black")
        label.grid(row=0, column=0, columnspan=2, pady=(50, 20), sticky="n")

        # Buttons - Central Column (column 0 or 1)
        # Primary Button Color (OrangeRed)
        BUTTON_BG = "#FF4500" 
        BUTTON_FG = "#FFFFFF" 
        
        button1 = tk.Button(self, text="Sign up", fg=BUTTON_FG, bg=BUTTON_BG, 
                            command=lambda: self.controller.show_frame("PageOne"), 
                            width=15, height=2, font=('Helvetica', 14, 'bold'))
        
        button2 = tk.Button(self, text="Check a User", fg=BUTTON_FG, bg=BUTTON_BG, 
                            command=lambda: self.controller.show_frame("PageTwo"), 
                            width=15, height=2, font=('Helvetica', 14, 'bold'))
                            
        # Secondary Button Color (Lighter for Quit)
        button3 = tk.Button(self, text="Quit", fg="#000000", bg="#DCDCDC", 
                            command=self.on_closing, 
                            width=15, height=2, font=('Helvetica', 14, 'bold'))
                            
        # Place buttons in the center of the frame
        button1.grid(row=2, column=0, columnspan=2, pady=10)
        button2.grid(row=3, column=0, columnspan=2, pady=10)
        button3.grid(row=4, column=0, columnspan=2, pady=10)

        # Center all content
        center_grid_widgets(self, 5, 2)
        
        # Configure the row with the image to take less vertical space
        self.grid_rowconfigure(1, weight=2)
        # Configure other rows to distribute space
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

    def on_closing(self):
        self.controller.on_closing()

# --- PageOne (Sign Up - Enter Name) ---
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="black")
        self.controller = controller
        
        # Primary Button Color
        BUTTON_BG = "#FF4500" 
        BUTTON_FG = "#FFFFFF" 
        # Secondary Button Color
        CANCEL_BG = "#DCDCDC" 
        CANCEL_FG = "#000000" 

        tk.Label(self, text="Enter the Name for New User", fg="white", bg="black", font='Helvetica 16 bold').grid(row=0, column=0, columnspan=3, pady=(50, 20), sticky="n")
        
        tk.Label(self, text="Name:", fg="white", bg="black", font='Helvetica 14').grid(row=1, column=0, pady=10, padx=10, sticky="e")
        
        self.user_name = tk.Entry(self, borderwidth=3, bg="#A9A9A9", font='Helvetica 14', width=20)
        self.user_name.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="w")
        
        self.buttoncanc = tk.Button(self, text="Cancel", bg=CANCEL_BG, fg=CANCEL_FG, 
                                    command=lambda: controller.show_frame("StartPage"), 
                                    width=15, height=2, font=('Helvetica', 12, 'bold'))
        
        self.buttonext = tk.Button(self, text="Next", fg=BUTTON_FG, bg=BUTTON_BG, 
                                   command=self.start_training, 
                                   width=15, height=2, font=('Helvetica', 12, 'bold'))
        
        self.buttonclear = tk.Button(self, text="Clear", command=self.clear, fg=BUTTON_FG, bg=BUTTON_BG, 
                                     width=15, height=2, font=('Helvetica', 12, 'bold'))
        
        # Positioning buttons in the center
        self.buttoncanc.grid(row=2, column=0, pady=20, padx=10)
        self.buttonclear.grid(row=2, column=1, pady=20, padx=10)
        self.buttonext.grid(row=2, column=2, pady=20, padx=10)
        
        center_grid_widgets(self, 3, 3)

    def start_training(self):
        global names
        name_input = self.user_name.get().strip()
        if not name_input or name_input.lower() == "none":
            messagebox.showerror("Error", "Name cannot be empty or 'None'!")
            return
        elif name_input in names:
            messagebox.showerror("Error", "User already exists!")
            return
            
        names.add(name_input)
        self.controller.active_name = name_input
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")
        
    def clear(self):
        self.user_name.delete(0, 'end')

# --- PageTwo (Check User - Select/Enter Name) ---
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="black")
        global names
        self.controller = controller
        
        # Primary Button Color
        BUTTON_BG = "#FF4500" 
        BUTTON_FG = "#FFFFFF" 
        # Secondary Button Color
        CANCEL_BG = "#DCDCDC" 
        CANCEL_FG = "#000000" 

        tk.Label(self, text="Check User Access", fg="white", bg="black", font='Helvetica 16 bold').grid(row=0, column=0, columnspan=3, pady=(50, 20), sticky="n")

        # Entry for new name (alternate method)
        tk.Label(self, text="Enter Username:", fg="white", bg="black", font='Helvetica 14').grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.user_name = tk.Entry(self, borderwidth=3, bg="#A9A9A9", font='Helvetica 14', width=20)
        self.user_name.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="w")
        
        # Dropdown for existing names
        tk.Label(self, text="Select Existing User:", fg="white", bg="black", font='Helvetica 14').grid(row=2, column=0, pady=10, padx=10, sticky="e")
        self.menuvar = tk.StringVar(self)
        
        # Use a placeholder for initial population, actual population happens in refresh_names
        self.dropdown = tk.OptionMenu(self, self.menuvar, "No Users Registered")
        self.dropdown.config(bg="#A9A9A9", fg="#000000", font='Helvetica 14')
        self.dropdown["menu"].config(bg="#A9A9A9", fg="#000000", font='Helvetica 14')
        self.dropdown.grid(row=2, column=1, columnspan=2, ipadx=8, padx=10, pady=10, sticky="w")

        # Buttons
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg=CANCEL_BG, fg=CANCEL_FG, 
                                    width=15, height=2, font=('Helvetica', 12, 'bold'))
                                    
        self.buttonclear = tk.Button(self, text="Clear Entry", command=self.clear, fg=BUTTON_FG, bg=BUTTON_BG, 
                                     width=15, height=2, font=('Helvetica', 12, 'bold'))
                                     
        self.buttonext_entry = tk.Button(self, text="Go (Entry)", command=self.next_foo_entry, fg=BUTTON_FG, bg=BUTTON_BG, 
                                         width=15, height=2, font=('Helvetica', 12, 'bold'))
                                         
        self.buttonext_dropdown = tk.Button(self, text="Go (Select)", command=self.next_foo_dropdown, fg=BUTTON_FG, bg=BUTTON_BG, 
                                            width=15, height=2, font=('Helvetica', 12, 'bold'))

        # Positioning buttons
        self.buttoncanc.grid(row=3, column=0, pady=20, padx=10)
        self.buttonclear.grid(row=3, column=1, pady=20, padx=10)
        self.buttonext_entry.grid(row=3, column=2, pady=20, padx=10)
        
        self.buttonext_dropdown.grid(row=4, column=0, columnspan=3, pady=10)

        center_grid_widgets(self, 5, 3)
        self.refresh_names() # Initial population

    def next_foo_entry(self):
        name_input = self.user_name.get().strip()
        if not name_input or name_input.lower() == 'none':
            messagebox.showerror("ERROR", "Name cannot be empty or 'None'")
            return
        if name_input not in names:
            messagebox.showerror("ERROR", f"User '{name_input}' not registered!")
            return
            
        self.controller.active_name = name_input
        self.controller.show_frame("PageFour") 
        
    def next_foo_dropdown(self):
        selected_name = self.menuvar.get()
        if not selected_name or selected_name == "No Users Registered":
            messagebox.showerror("ERROR", "Please select a user first.")
            return
            
        self.controller.active_name = selected_name
        self.controller.show_frame("PageFour")

    def clear(self):
        self.user_name.delete(0, 'end')

    def refresh_names(self):
        global names
        self.menuvar.set('')
        menu = self.dropdown['menu']
        menu.delete(0, 'end')
        
        if not names:
            menu.add_command(label="No Users Registered", state="disabled")
            self.menuvar.set("No Users Registered")
            return
            
        # Initial setting of menuvar to the first name or empty
        sorted_names = sorted(list(names))
        if sorted_names:
            self.menuvar.set(sorted_names[0])
            
        for name in sorted_names:
            menu.add_command(label=name, command=tk._setit(self.menuvar, name))

# --- PageThree (Data Capture and Training) ---
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="black")
        self.controller = controller
        
        # Primary Button Color
        BUTTON_BG = "#FF4500" 
        BUTTON_FG = "#FFFFFF" 

        tk.Label(self, text="New User Data Setup", font='Helvetica 16 bold', fg="white", bg="black").grid(row=0, column=0, columnspan=2, pady=(50, 20), sticky="n")
        
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 14', fg="white", bg="black")
        self.numimglabel.grid(row=1, column=0, columnspan=2, pady=10, sticky="n")
        
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg=BUTTON_FG, bg=BUTTON_BG, 
                                       command=self.capimg, width=20, height=3, font=('Helvetica', 14, 'bold'))
                                       
        self.trainbutton = tk.Button(self, text="Train The Model", fg=BUTTON_FG, bg=BUTTON_BG,
                                     command=self.trainmodel, width=20, height=3, font=('Helvetica', 14, 'bold'))
                                     
        self.capturebutton.grid(row=2, column=0, padx=20, pady=30)
        self.trainbutton.grid(row=2, column=1, padx=20, pady=30)
        
        center_grid_widgets(self, 3, 2)

    def capimg(self):
        self.numimglabel.config(text="Captured Images = 0 ")
        messagebox.showinfo("INSTRUCTIONS", f"We will Capture 300 pictures of {self.controller.active_name}'s face.")
        
        # External call - assume it returns the count
        x = start_capture(self.controller.active_name) 
        
        self.controller.num_of_images = x
        self.numimglabel.config(text=f"Number of images captured = {x}")

    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "Not enough Data, Capture at least 300 images!")
            return
            
        # External call
        train_classifer(self.controller.active_name) 
        
        messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
        self.controller.show_frame("PageFour")

# --- PageFour (Detection/Functionality) ---
class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="black")
        self.controller = controller

        # Primary Button Color
        BUTTON_BG = "#FF4500" 
        BUTTON_FG = "#FFFFFF" 
        # Secondary Button Color
        BACK_BG = "#DCDCDC" 
        BACK_FG = "#000000" 

        label = tk.Label(self, text="Detection Functions", font='Helvetica 16 bold', fg="white", bg="black")
        label.grid(row=0, column=0, columnspan=2, pady=(50, 20), sticky="n")
        
        button1 = tk.Button(self, text="Start Face Recognition", command=self.openwebcam, fg=BUTTON_FG, bg=BUTTON_BG, 
                            width=20, height=3, font=('Helvetica', 14, 'bold'))
                            
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg=BACK_BG, fg=BACK_FG, 
                            width=20, height=3, font=('Helvetica', 14, 'bold'))
                            
        # Place buttons in the center
        button1.grid(row=1, column=0, padx=20, pady=30)
        button4.grid(row=1, column=1, padx=20, pady=30)
        
        center_grid_widgets(self, 2, 2)

    def openwebcam(self):
        # External call
        main_app(self.controller.active_name)
        
# --- Application Execution ---
if __name__ == "__main__":
    app = HARIS_App()
    # Attempt to set icon if available
    try:
        app.iconphoto(True, tk.PhotoImage(file='icon.ico'))
    except tk.TclError:
        pass # Ignore error if icon file is missing
        
    app.mainloop()