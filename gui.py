import customtkinter as ctk
import subprocess
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class FSMGui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FSM Implication Table Solver")
        self.geometry("1100x900")
        self.resizable(True, True)
        
        # 1. Config Section
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(self.config_frame, text="Type:").pack(side="left", padx=5)
        self.machine_type = ctk.CTkSegmentedButton(self.config_frame, values=["mealy", "moore"], command=self.generate_grid)
        self.machine_type.set("mealy")
        self.machine_type.pack(side="left", padx=10)

        ctk.CTkLabel(self.config_frame, text="Input Bits (n):").pack(side="left", padx=5)
        self.entry_inputs = ctk.CTkEntry(self.config_frame, width=50)
        self.entry_inputs.pack(side="left", padx=5)
        self.entry_inputs.insert(0, "1")

        ctk.CTkLabel(self.config_frame, text="States:").pack(side="left", padx=5)
        self.entry_num = ctk.CTkEntry(self.config_frame, width=50)
        self.entry_num.pack(side="left", padx=5)
        self.entry_num.insert(0, "4") 
        
        self.btn_generate = ctk.CTkButton(self.config_frame, text="Generate Table", command=self.generate_grid)
        self.btn_generate.pack(side="left", padx=15)

        # 2. Table Section
        self.table_frame = ctk.CTkScrollableFrame(self, width=1050, height=450)
        self.table_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.grid_widgets = [] 

        # 3. Action Section
        self.btn_solve = ctk.CTkButton(self, text="Run Reduction", command=self.run_logic, fg_color="#2ecc71", hover_color="#27ae60", font=("Arial", 14, "bold"))
        self.btn_solve.pack(pady=10)

        # 4. Results Section
        ctk.CTkLabel(self, text="Results:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20)
        self.result_text = ctk.CTkTextbox(self, width=1050, height=250, font=("Consolas", 15))
        self.result_text.pack(pady=10, padx=10, fill="x")
        self.result_text.insert("0.0", "Enter data and click 'Run Reduction'...")

    def generate_grid(self, _=None):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.grid_widgets = []
        try:
            num_states = int(self.entry_num.get().strip())
            input_bits = int(self.entry_inputs.get().strip()) 
            num_inputs = 2 ** input_bits 
            m_type = self.machine_type.get()
        except ValueError:
            return

        headers = ["State"]
        if m_type == "mealy":
            for i in range(num_inputs): headers.append(f"Next (In {i})")
            for i in range(num_inputs): headers.append(f"Out (In {i})")
        else:
            for i in range(num_inputs): headers.append(f"Next (In {i})")
            headers.append("Output")

        for col, text in enumerate(headers):
            lbl = ctk.CTkLabel(self.table_frame, text=text, font=("Arial", 12, "bold"))
            lbl.grid(row=0, column=col, padx=10, pady=5)

        for r in range(num_states):
            row_entries = []
            for c in range(len(headers)):
                entry = ctk.CTkEntry(self.table_frame, width=85) 
                entry.grid(row=r+1, column=c, padx=2, pady=2)
                if c == 0: entry.insert(0, chr(65 + r)) 
                entry.bind("<Key>", lambda e, r=r, c=c: self.handle_arrows(e, r, c))
                row_entries.append(entry)
            self.grid_widgets.append(row_entries)

    def handle_arrows(self, event, row, col):
        new_row, new_col = row, col
        if event.keysym == "Up": new_row -= 1
        elif event.keysym == "Down": new_row += 1
        elif event.keysym == "Left": new_col -= 1
        elif event.keysym == "Right": new_col += 1
        else: return
        if 0 <= new_row < len(self.grid_widgets) and 0 <= new_col < len(self.grid_widgets[0]):
            self.grid_widgets[new_row][new_col].focus_set()

    def run_logic(self):
        m_type = self.machine_type.get()
        input_bits = self.entry_inputs.get()
        all_states = [row[0].get().strip() for row in self.grid_widgets if row[0].get().strip()]
        num_states = len(all_states)
        
        input_data = f"{m_type} {input_bits} {num_states}\n"
        for row in self.grid_widgets:
            input_data += " ".join([e.get().strip() for e in row]) + "\n"

        try:
            # USE RESOURCE PATH TO FIND THE BUNDLED EXE
            cpp_exe = resource_path("main.exe")
            
            process = subprocess.Popen(
                [cpp_exe], 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            output, _ = process.communicate(input=input_data)
            
            self.result_text.delete("0.0", "end")
            lines = [line.strip() for line in output.strip().split('\n') if line.strip()]
            
            found_in_pairs = set()
            for line in lines:
                for state in line.split(): found_in_pairs.add(state)
            
            unique_states = [s for s in all_states if s not in found_in_pairs]
            
            res = ""
            if lines:
                res += "=== EQUIVALENT GROUPS ===\n" + "\n".join(f" -> {l}" for l in lines) + "\n\n"
            if unique_states:
                res += "=== UNIQUE STATES ===\n" + "\n".join(f" -> {s}" for s in unique_states)

            self.result_text.insert("0.0", res if res.strip() else "All states are distinct.")

        except Exception as e:
            self.result_text.delete("0.0", "end")
            self.result_text.insert("0.0", f"Error: {e}")

if __name__ == "__main__":
    app = FSMGui()
    app.mainloop()