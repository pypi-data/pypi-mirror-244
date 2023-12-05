import json
import tkinter as tk
from tkinter import scrolledtext

# Function to save the data as JSON
def save_json():
    data = []
    num_entries = int(entry_count.get())
    
    for i in range(num_entries):
        input_data = input_entries[i].get("1.0", "end-1c")
        output_data = output_entries[i].get("1.0", "end-1c")
        
        entry = {"Input": input_data, "Output": output_data}
        data.append(entry)
    
    with open("dataset.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    result_label.config(text="Dataset has been created and saved as 'dataset.json'.")

# Create the main window
root = tk.Tk()
root.title("JSON Dataset Creator")

# Entry for the number of entries
entry_count_label = tk.Label(root, text="How many entries do you want in the dataset?")
entry_count_label.pack()
entry_count = tk.Entry(root)
entry_count.pack()

# Create lists to store input and output text widgets
input_entries = []
output_entries = []

# Create a canvas and scrollbar
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold your widgets
frame = tk.Frame(canvas)

# Function to add input and output text boxes dynamically
def add_entry_fields():
    num_entries = int(entry_count.get())
    
    for i in range(num_entries):
        input_label = tk.Label(frame, text=f"Input for entry {i + 1}:")
        input_label.pack()
        input_text = scrolledtext.ScrolledText(frame, width=40, height=5)
        input_text.pack()
        input_entries.append(input_text)
        
        output_label = tk.Label(frame, text=f"Output for entry {i + 1}:")
        output_label.pack()
        output_text = scrolledtext.ScrolledText(frame, width=40, height=5)
        output_text.pack()
        output_entries.append(output_text)

add_button = tk.Button(root, text="Add Entry Fields", command=add_entry_fields)
add_button.pack()

save_button = tk.Button(root, text="Save as JSON", command=save_json)
save_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Pack your scrollbar and canvas, and then create a window in your canvas containing your frame
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0,0), window=frame, anchor="nw")

def on_frame_configure(event):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

root.mainloop()
