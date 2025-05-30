import tkinter as tk
from tkinter import *
from tkinter import messagebox,simpledialog
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import sqlite3
import os
from tkinter import filedialog, messagebox

window =tk.Tk()
window.geometry('500x500')
window.title('our')
icon=PhotoImage(file='p.png')
window.iconphoto(True, icon)
window.config(bg='pink')
photo=PhotoImage(file='p.png')
root=None

pygame.mixer.init()

MUSIC_FOLDER = "music_files"
os.makedirs(MUSIC_FOLDER, exist_ok=True)


conn = sqlite3.connect("shelf_app.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL
)
""")
conn.commit()

# Create tables
conn_songs = sqlite3.connect("music.db")
c_songs = conn_songs.cursor()
c_songs.execute("""
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT NULL
)
""")
conn_songs.commit()



def music():
    global root 
    root.destroy()  

    music = tk.Tk()
    music.geometry('500x600')
    music.title('Songs')
    music.config(bg='pink')

    mimage = tk.PhotoImage(file='music.png') 
    mimage = mimage.subsample(2, 2) 
    
    # --- Header ---
    m1 = tk.Label(music, text='Music', font=('Arial', 20), bg='pink', fg='white',
                  relief='groove', bd=5, padx=5, pady=5, image=mimage, compound='top')
    m1.image = mimage
    m1.pack(pady=10)

    # --- Scrollable Area (Songs + Buttons) ---
    main_frame = tk.Frame(music, bg='pink')
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame, bg='pink', highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas, bg='pink')
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def resize_scrollable_frame(event):
        canvas.itemconfig(canvas_window, width=event.width)

    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", resize_scrollable_frame)

    # --- Song List Loader ---
    def loadsong():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        c_songs.execute("SELECT id, name, path FROM songs")
        songs = c_songs.fetchall()

        if not songs:
            tk.Label(scrollable_frame, text="No songs added yet.", font=("Arial", 15),
                     bg="pink", fg="white",relief=GROOVE).pack(pady=20)
            return

        for song_id, name, path in songs:
            btn = tk.Button(scrollable_frame, text=name, font=("Arial", 14),
                            bg="pink", fg="white", relief="groove", bd=2,
                            command=lambda p=path: play_song(p))
            btn.pack(fill=tk.X, padx=20, pady=5)

        # --- Add Song Button ---
        add_btn = tk.Button(scrollable_frame, text="Add Song", font=('Arial', 14), bg='pink', fg='white',
                            relief='groove', bd=5, padx=5, pady=5, command=add_song)
        add_btn.pack(pady=15)

        # --- Stop and Back Buttons ---
        control_frame = tk.Frame(scrollable_frame, bg='pink')
        control_frame.pack(pady=10)

        stop_btn = tk.Button(control_frame, text='Stop', font=('Arial', 14), bg='pink', fg='white',
                             relief='groove', bd=5, padx=5, pady=5, command=stop)
        stop_btn.pack(side=LEFT, padx=10)

        back_btn = tk.Button(control_frame, text='Back', font=('Arial', 14), bg='pink', fg='white',
                             relief='groove', bd=5, padx=5, pady=5, command=goback)
        back_btn.pack(side=RIGHT, padx=10)

    # --- Music Control Functions ---
    def play_song(path):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        except Exception as e:
            messagebox.showerror("Playback Error", str(e))

    def stop():
        pygame.mixer.music.stop()
    
    

    def goback():
        stop()
        music.destroy()
        click()

    def add_song():
        file_path = filedialog.askopenfilename(
            title="Select a song",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All files", "*.*")]
        )
        if file_path:
            name = os.path.basename(file_path)
            try:
                c_songs.execute("INSERT INTO songs (name, path) VALUES (?, ?)", (name, file_path))
                conn_songs.commit()
                messagebox.showinfo("Success", f"Added '{name}' successfully!")
                loadsong()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add song:\n{str(e)}")

    loadsong()
    music.mainloop()

from tkinter import *

def counter():
    root.destroy()  # Destroys the previous window if it's there
    
    win = Tk()  # Don't name this "counter", it'll overwrite the function name!
    win.geometry('500x500')
    win.title('Counter')
    win.config(bg='pink')

    Label(win, text='Counter', font=('Arial', 20), bg='pink', fg='white').pack(pady=20)

    count = IntVar()
    count.set(0)

    def increment():
        count.set(count.get() + 1)

    # Display the number
    Label(win, textvariable=count, font=('Arial', 48), bg='pink', fg='white').pack(pady=20)

    # Button with image
    try:
        img = Image.open('count.jpg')  # use your image filename
        img = img.resize((100, 100))   # optional resize
        photo = ImageTk.PhotoImage(img)
        Button(win, image=photo, command=increment, relief='groove', bd=5,
               padx=5, pady=5, bg='pink', activebackground='pink').pack()
        win.image = photo  # prevent garbage collection
    except: 
        Button(win, text="Click Me", command=increment, font=('Arial', 20),
               bg='pink', fg='white', relief='groove', bd=5, padx=5, pady=5).pack()
        
    
    def goback():
        win.destroy()
        click()    
    exit=Button(win, text='Exit', font=('Arial', 20), bg='pink', fg='white', relief='groove', bd=5, padx=5, pady=5, command=goback)
    exit.pack(pady=20)

    win.mainloop()

def list():
    root.destroy()
    todo_win = tk.Tk()
    todo_win.geometry('500x500')
    todo_win.title('To-Do List')
    todo_win.config(bg='pink')

    main_frame = tk.Frame(todo_win, bg='lavender')
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame, bg='lavender', highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas, bg='lavender')
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

    # Function to refresh todo list from DB
    def load_todos():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        c.execute("SELECT id, task FROM todos")
        todos = c.fetchall()

        if not todos:
            tk.Label(scrollable_frame, text="No tasks added yet.", font=("Arial", 15),
                     bg="lavender", fg="black").pack(pady=20)
            return

        for todo_id, task in todos:
            frame = tk.Frame(scrollable_frame, bg='lavender', pady=5)
            frame.pack(fill=tk.X, padx=10)

            label = tk.Label(frame, text=task, font=("Arial", 14), bg='lavender', anchor='w')
            label.pack(side=tk.LEFT, padx=10)

            # Delete button
            def delete_task(id=todo_id):
                c.execute("DELETE FROM todos WHERE id=?", (id,))
                conn.commit()
                load_todos()

            del_btn = tk.Button(frame, text='Delete', bg='pink', fg='white', font=('Arial', 12),
                                relief='groove', bd=3, command=delete_task)
            del_btn.pack(side=tk.RIGHT, padx=5)

    # Add new task function
    def add_task():
        task = simpledialog.askstring("New Task", "Enter the task:")
        if task:
            c.execute("INSERT INTO todos (task) VALUES (?)", (task,))
            conn.commit()
            load_todos()

    # Add Task button
    add_btn = tk.Button(todo_win, text="Add Task", font=('Arial', 15), bg='pink', fg='white',
                        relief='groove', bd=5, padx=5, pady=5, command=add_task)
    add_btn.pack(pady=10)

    # Back button
    def goback():
        todo_win.destroy()
        click()

    back_btn = tk.Button(todo_win, text='Back', font=('Arial', 15), bg='pink', fg='white',
                         relief='groove', bd=5, padx=5, pady=5, command=goback)
    back_btn.pack(pady=10)

    load_todos()
    todo_win.mainloop()


def click():
    global root
    
    root=tk.Tk()
    root.geometry('500x500')
    bg = PhotoImage(file = "BCK.png")
 
  
# Show image using label
    label1 = Label( root, image = bg)
    label1.place(x = 0, y = 0)

    B1=Button(root,text='Music',font=('Arial', 20),bg='pink',fg='white',relief='groove',bd=5,padx=5,pady=5,command=music,activebackground='pink')
    B1.pack(pady=20)
    B2=Button(root,text='List',font=('Arial', 20),bg='pink',fg='white',relief='groove',bd=5,padx=5,pady=5,command=list,activebackground='pink')
    B2.pack(pady=30)
    B3=Button(root,text='counter',font=('Arial', 20),bg='pink',fg='white',relief='groove',bd=5,padx=5,pady=5,command=counter,activebackground='pink')
    B3.pack(pady=30)
   
    

    root.mainloop()

def startapp():
    window.destroy()
    click()
label =Button(window,
             text="Hi cuties \n Welcome to your world",
             font=('Arial', 20), bg='pink', fg='white',relief='groove',bd=5,padx=5,pady=5,
             image=photo,compound='bottom',command=startapp)
label.pack(pady=20)





window.mainloop()
