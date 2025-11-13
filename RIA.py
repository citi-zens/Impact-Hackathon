import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class SystemDetail:
    def __init__(self, system_name: str, system_description: str):
        if not system_name:
            raise ValueError("System Name cannot be empty.")
        self.system_name = system_name
        self.system_description = system_description

    def __repr__(self):
        return f"SystemDetail(name=: '{self.system_name}', desc= '{self.system_description}')"

class RapidImpactAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("RIA (Rapid Impact Analyzer)")
        master.geometry("800x500")

        self.system_inventory: list = []
        self._load_initial_inventory()

        # Main frame for the application
        main_frame = tk.Frame(master, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Section-1: IMPACT ANALYZER MANAGEMENT
        impact_analyzer_frame = ttk.LabelFrame(main_frame, text="IMPACT ANALYZER MANAGEMENT", padding="10 10 10 10")
        impact_analyzer_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # System selection
        tk.Label(impact_analyzer_frame, text="SELECT SYSTEM").grid(row=0, column=0, sticky="w", pady=5)
        self.system_names = [sys.system_name for sys in self.system_inventory]
        self.selected_system_name = tk.StringVar(impact_analyzer_frame)
        self.system_dropdown = ttk.Combobox(impact_analyzer_frame, textvariable=self.selected_system_name, values=self.system_names, state="readonly")
        self.system_dropdown.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.system_dropdown.bind("<<ComboboxSelected>>", self._on_system_selected)

        # System description
        tk.Label(impact_analyzer_frame, text="System Description").grid(row=1, column=0, sticky="nw", pady=5)
        self.system_desc_text = tk.Text(impact_analyzer_frame, height=5, width=40, state="disabled", wrap=tk.WORD)
        self.system_desc_text.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # File upload
        tk.Button(impact_analyzer_frame, text="Upload or Browse files", command=self._upload_files).grid(row=2, column=0, columnspan=2, pady=10)
        self.uploaded_files_label = tk.Label(impact_analyzer_frame, text="No files selected.")
        self.uploaded_files_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)

        # Start Analyzer Button
        tk.Button(impact_analyzer_frame, text="Start Analyzer", command=self._start_analyzer).grid(row=4, column=0, columnspan=2, pady=10)

        # Output List Placeholder
        output_label_frame = ttk.LabelFrame(impact_analyzer_frame, text="Analysis Output", padding="5 5 5 5")
        output_label_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=10)
        tk.Label(output_label_frame, text="1. Direct impact with Accuracy").pack(anchor="w")
        tk.Label(output_label_frame, text="2. Indirect impact with Accuracy").pack(anchor="w")
        tk.Label(output_label_frame, text="3. DB Direct List").pack(anchor="w")
        tk.Label(output_label_frame, text="4. Templates Impact list").pack(anchor="w")
        tk.Label(output_label_frame, text="5. Others...").pack(anchor="w")

        # Section-2 INVENTORY MANAGEMENT
        inventory_frame = ttk.LabelFrame(main_frame, text="INVENTORY", padding="10 10 10 10")
        inventory_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # System selection inventory frame
        tk.Label(inventory_frame, text="SELECT SYSTEM").grid(row=0, column=0, sticky="w", pady=5)
        self.system_names_inv_frame = [sys.system_name for sys in self.system_inventory]
        self.selected_system_name_inv_frame = tk.StringVar(inventory_frame)
        self.system_dropdown = ttk.Combobox(inventory_frame, textvariable=self.selected_system_name_inv_frame, values=self.system_names_inv_frame, state="readonly")
        self.system_dropdown.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.system_dropdown.bind("<<ComboboxSelected>>", self._on_system_selected)

        # System description inventory frame
        tk.Label(inventory_frame, text="System Description").grid(row=1, column=0, sticky="w", pady=5)
        self.system_desc_text_inv_frame = tk.Text(inventory_frame, height=5, width=40, state="disabled", wrap=tk.WORD)
        self.system_desc_text_inv_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        tk.Button(inventory_frame, text="Add/Update Inventory", command=self._add_update_inventory).grid(row=2, column=0, columnspan=2, pady=10)
        self.inventory_status_label = tk.Label(inventory_frame, text="", fg="green")
        self.inventory_status_label.grid(row=3, column=0, columnspan=2, pady=5)

        # Configure Grid weights to make frame expandable
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        impact_analyzer_frame.grid_columnconfigure(1, weight=1)
        inventory_frame.grid_columnconfigure(1, weight=1)

    def _load_initial_inventory(self):
        """Load system inventory."""
        self.system_inventory.append(SystemDetail("Account Opening","An account opening system is a software-based process for creating new customer accounts workflow. It collects customer information, verifies identities to complete the account setup"))
        self.system_inventory.append(SystemDetail("Payment System", "These systems facilitate financial transactions, using methods like cash, checks, credit cards, and electronic funds transfers, and are crucial for the efficient functioning of economies."))
        self.system_inventory.append(SystemDetail("Notifications", "A notification is an alert or message that provides timely information to a user from an application or system, appearing on a device even when the app is not open."))
        self.system_inventory.append(SystemDetail("Credit Cards", "A credit card issuer system is a financial institution that provides credit cards to consumers, manages their accounts, and processes transactions."))

    def _update_system_dropdown(self):
        """Refresh system dropdown."""
        self.system_names = [sys.system_name for sys in self.system_inventory]
        self.system_dropdown['values'] = self.system_names

        if self.selected_system_name.get() not in self.system_names:
            self.selected_system_name.set("")
            self._update_system_description("")
        self.system_dropdown.set("")


    def _on_system_selected(self, event=None):
        """Update the description when select the system in drop down"""
        selected_name = self.selected_system_name.get()
        if selected_name:
            for sys in self.system_inventory:
                if sys.system_name == selected_name:
                    self._update_system_description(sys.system_description)
                    return
        self._update_system_description("") # clear if no system selected or found


    def _update_system_description(self, description: str):
        """Update the description of the system"""
        self.system_desc_text.config(state="normal")
        self.system_desc_text.delete(1.0, tk.END)
        self.system_desc_text.insert(tk.END, description)
        self.system_desc_text.config(state="disabled")


    def _upload_files(self):
        """Simulate file upload functionality"""
        file_path = filedialog.askopenfilename(
            title="Select files for analysis",
            filetypes=(("All files", "*.*"), ("Text Files", "*.txt"), ("CSV files", "*.csv"))
        )
        if file_path:
            self.uploaded_files_label.config(text=f"Selected {len(file_path)} file(s).")
            messagebox.showinfo("File Upload", f"Successfully selected {len(file_path)} files.")
            print(f"Files selected: {file_path}")
        else:
            self.uploaded_files_label.config(text="No files selected.")
            print("No files selected")


    def _start_analyzer(self):
        """Simulate analysis functionality"""
        selected_system = self.selected_system_name.get()
        if not selected_system:
            messagebox.showwarning("Analysis Error", "Please select a system first")
            return
        if self.uploaded_files_label.cget("text") == "No files selected.":
            messagebox.showwarning("Analysis Error", "Please upload files for analysis")
            return

        messagebox.showinfo("Analysis started", f"Analysis started for '{selected_system}' files.")
        print(f"Analysis started for '{selected_system}' files.")
        # placeholder for actual impact analysis logic
        # This is where the application would process files and generate impacts


    def _add_update_inventory(self):
        """Add a new system or update as existing inventory."""
        system_name = self.system_dropdown.get().strip()
        system_description = self.system_desc_text_inv_frame.get("1.0", tk.END).strip()

        if not system_name:
            messagebox.showwarning("Input Error", "System name cannot be empty.")
            return

        # Check if system already exists
        found = False
        for sys in self.system_inventory:
            if sys.system_name == system_name:
                sys.system_description = system_description
                found = True
                messagebox.showinfo("Inventory Update", f"System '{system_name}' updated successfully.")
                self.inventory_status_label.config(text=f"System '{system_name}' updated successfully.")
                break

            if not found:
                try:
                    new_system = SystemDetail(system_name, system_description)
                    self.system_inventory.append(new_system)
                    messagebox.showinfo("Inventory Update", f"System '{system_name}' added successfully.")
                    self.inventory_status_label.config(text=f"System '{system_name}' added successfully.")
                except ValueError as e:
                    messagebox.showerror("Inventory Error", str(e))
                    self.inventory_status_label.config(text=f"Error: {e}", fg="red")
                    return

            # Clear the inputs
            self.system_dropdown.delete(0, tk.END)
            self.system_dropdown.delete("1.0", tk.END)
            self._update_system_description()  # Refresh the dropdown

if __name__ == "__main__":
    root = tk.Tk()
    app = RapidImpactAnalyzerApp(root)
    root.mainloop()


