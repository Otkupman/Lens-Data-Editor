import tkinter as tk
from tkinter import ttk, messagebox

class LensDataEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Lens Data Editor")

        self.table = ttk.Treeview(root, columns=("Surface Number", "Radius", "Thickness", "Refractive Index"), show='headings')
        self.table.heading("Surface Number", text="№")
        self.table.heading("Radius", text="Radius")
        self.table.heading("Thickness", text="Thickness")
        self.table.heading("Refractive Index", text="Refractive Index")

        self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(root, text="Add Row", command=self.add_row)
        self.add_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(root, text="Delete Row", command=self.delete_row)
        self.delete_button.pack(side=tk.LEFT)

        self.check_button = tk.Button(root, text="Check Data", command=self.check_data)
        self.check_button.pack(side=tk.LEFT)

        # Initialize with 2 rows
        for i in range(2):
            self.table.insert("", "end", values=(i + 1, "0", "0", "0"))

        self.table.bind("<Double-1>", self.on_double_click)

    def add_row(self):
        selected_item = self.table.selection()
        if selected_item:
            index = self.table.index(selected_item[0])
            self.table.insert("", index + 1, values=("", "", "", ""))
        else:
            # Get the current number of rows
            current_count = len(self.table.get_children())
            self.table.insert("", "end", values=("", "", "", ""))

        self.update_surface_numbers()

    def delete_row(self):
        selected_item = self.table.selection()
        if selected_item:
            self.table.delete(selected_item[0])
            self.update_surface_numbers()

    def update_surface_numbers(self):
        for index, item in enumerate(self.table.get_children()):
            self.table.item(item, values=(index + 1,) + self.table.item(item, "values")[1:])

    def on_double_click(self, event):
        item = self.table.selection()[0]
        column = self.table.identify_column(event.x)
        column_index = int(column.replace("#", "")) - 1

        # Prevent editing the surface number
        if column_index == 0:
            return

        # Get the current value
        value = self.table.item(item, "values")[column_index]

        # Create an entry widget to edit the value
        self.entry = tk.Entry(self.root)
        self.entry.insert(0, value)

        # Get the position of the cell
        x, y, width, height = self.table.bbox(item, column)
        self.entry.place(x=self.table.winfo_x() + x, y=self.table.winfo_y() + y, width=width)

        # Focus on the entry widget
        self.entry.focus()

        # Bind the return key to save the value
        self.entry.bind("<Return>", lambda e: self.save_value(item, column_index))
        self.entry.bind("<FocusOut>", lambda e: self.save_value(item, column_index))

    def save_value(self, item, column_index):
        new_value = self.entry.get()
        self.table.item(item, values=self.update_values(item, column_index, new_value))
        self.entry.destroy()

    def update_values(self, item, column_index, new_value):
        values = list(self.table.item(item, "values"))
        values[column_index] = new_value
        return tuple(values)

    def check_data(self):
        data = []
        for item in self.table.get_children():
            data.append(self.table.item(item, "values"))
        messagebox.showinfo("Table Data", "\n".join([str(row) for row in data]))

if __name__ == "__main__":
    root = tk.Tk()
    app = LensDataEditor(root)
    root.mainloop()