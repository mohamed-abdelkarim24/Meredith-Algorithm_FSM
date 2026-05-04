import customtkinter as ctk
import subprocess

class FSMGui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FSM Implication Table Solver")
        self.geometry("900x700")
        
        # 1. Config Section (Top)
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.pack(pady=10, padx=10, fill="x")
        
        self.label_num = ctk.CTkLabel(self.config_frame, text="Number of States:")
        self.label_num.pack(side="left", padx=10)
        
        self.entry_num = ctk.CTkEntry(self.config_frame, width=60)
        self.entry_num.pack(side="left", padx=10)
        self.entry_num.insert(0, "4") 
        
        self.btn_generate = ctk.CTkButton(self.config_frame, text="Generate Table", command=self.generate_grid)
        self.btn_generate.pack(side="left", padx=10)

        # 2. Table Section (Middle)
        self.table_frame = ctk.CTkScrollableFrame(self, width=850, height=450)
        self.table_frame.pack(pady=10, padx=10)
        
        self.grid_widgets = [] # List to store our Entry widgets

        # 3. Action Section (Bottom)
        self.btn_solve = ctk.CTkButton(self, text="Run Algorithm", command=self.run_logic, fg_color="#2ecc71", hover_color="#27ae60")
        self.btn_solve.pack(pady=10)

        self.result_label = ctk.CTkLabel(self, text="Results will appear here", font=("Arial", 16, "bold"))
        self.result_label.pack(pady=20)

    def generate_grid(self):
        # Clear the old table before building a new one
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.grid_widgets = []

        try:
            num_states = int(self.entry_num.get())
        except ValueError:
            return

        # Create Header Row
        headers = ["State Name", "Next (Input 0)", "Output (0)", "Next (Input 1)", "Output (1)"]
        for col, text in enumerate(headers):
            lbl = ctk.CTkLabel(self.table_frame, text=text, font=("Arial", 12, "bold"))
            lbl.grid(row=0, column=col, padx=10, pady=5)

        # Create Rows for each state
        for r in range(num_states):
            row_entries = []
            for c in range(5):
                entry = ctk.CTkEntry(self.table_frame, width=120)
                entry.grid(row=r+1, column=c, padx=5, pady=2)
                
                # Auto-fill the first column with A, B, C...
                if c == 0:
                    entry.insert(0, chr(65 + r)) 
                
                row_entries.append(entry)
            self.grid_widgets.append(row_entries)

    def run_logic(self):
        # Build the input string for the C++ engine
        # Format expected by C++: NumStates Next0 Out0 Next1 Out1 ...
        num_states = len(self.grid_widgets)
        input_data = f"{num_states}\n"
        
        for row in self.grid_widgets:
            # We skip the first cell (State Name) because the C++ map 
            # uses it as a key, but our logic fills it by reading sequentially
            state_name = row[0].get()
            n0 = row[1].get()
            o0 = row[2].get()
            n1 = row[3].get()
            o1 = row[4].get()
            
            # Formatted line for C++ cin
            input_data += f"{state_name} {n0} {o0} {n1} {o1}\n"

        try:
            # Call your compiled .exe
            process = subprocess.Popen(
                ['main.exe'], 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            output, errors = process.communicate(input=input_data)
            
            if output.strip():
                self.result_label.configure(text=f"Equivalent Pairs:\n{output}", text_color="#3498db")
            else:
                self.result_label.configure(text="No equivalent states found.", text_color="white")
        except Exception as e:
            self.result_label.configure(text=f"Error: {e}", text_color="red")

if __name__ == "__main__":
    app = FSMGui()
    app.mainloop()