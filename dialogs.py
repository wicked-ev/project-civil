import customtkinter as ctk
from tkinter import messagebox

class FoundationDialog:
    def __init__(self, parent):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Foundation")
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Name
        ctk.CTkLabel(self.dialog, text="Foundation Name:").pack(pady=(20, 0))
        self.name_entry = ctk.CTkEntry(self.dialog, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Main Foundation")
        
        # Type
        ctk.CTkLabel(self.dialog, text="Foundation Type:").pack(pady=(10, 0))
        self.type_var = ctk.StringVar(value="shallow")
        types = ['shallow', 'deep', 'pile', 'raft']
        self.type_menu = ctk.CTkOptionMenu(self.dialog, variable=self.type_var, 
                                           values=types, width=300)
        self.type_menu.pack(pady=5)
        
        # Area
        ctk.CTkLabel(self.dialog, text="Area (m²):").pack(pady=(10, 0))
        self.area_entry = ctk.CTkEntry(self.dialog, width=300)
        self.area_entry.pack(pady=5)
        self.area_entry.insert(0, "100")
        
        # Soil type
        ctk.CTkLabel(self.dialog, text="Soil Type:").pack(pady=(10, 0))
        self.soil_var = ctk.StringVar(value="medium")
        soils = ['soft', 'medium', 'hard']
        self.soil_menu = ctk.CTkOptionMenu(self.dialog, variable=self.soil_var, 
                                           values=soils, width=300)
        self.soil_menu.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=20)
        ctk.CTkButton(button_frame, text="Cancel", 
                     command=self.dialog.destroy).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Add", 
                     command=self._submit).pack(side="right", padx=5)
    
    def _submit(self):
        try:
            self.result = {
                'name': self.name_entry.get(),
                'foundation_type': self.type_var.get(),
                'area': float(self.area_entry.get()),
                'soil_type': self.soil_var.get()
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

class DoorDialog:
    def __init__(self, parent):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Door")
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        ctk.CTkLabel(self.dialog, text="Door Name:").pack(pady=(20, 0))
        self.name_entry = ctk.CTkEntry(self.dialog, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Main Door")
        
        ctk.CTkLabel(self.dialog, text="Door Type:").pack(pady=(10, 0))
        self.type_var = ctk.StringVar(value="standard")
        types = ['standard', 'double', 'main', 'security', 'sliding']
        self.type_menu = ctk.CTkOptionMenu(self.dialog, variable=self.type_var, 
                                           values=types, width=300)
        self.type_menu.pack(pady=5)
        
        ctk.CTkLabel(self.dialog, text="Quantity:").pack(pady=(10, 0))
        self.qty_entry = ctk.CTkEntry(self.dialog, width=300)
        self.qty_entry.pack(pady=5)
        self.qty_entry.insert(0, "1")
        
        ctk.CTkLabel(self.dialog, text="Material:").pack(pady=(10, 0))
        self.material_var = ctk.StringVar(value="wood")
        materials = ['wood', 'steel', 'aluminum', 'upvc']
        self.material_menu = ctk.CTkOptionMenu(self.dialog, variable=self.material_var, 
                                               values=materials, width=300)
        self.material_menu.pack(pady=5)
        
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=20)
        ctk.CTkButton(button_frame, text="Cancel", 
                     command=self.dialog.destroy).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Add", 
                     command=self._submit).pack(side="right", padx=5)
    
    def _submit(self):
        try:
            self.result = {
                'name': self.name_entry.get(),
                'door_type': self.type_var.get(),
                'quantity': int(self.qty_entry.get()),
                'material': self.material_var.get()
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

class RoomDialog:
    """Dialog for adding a room with dimensions"""

    def __init__(self, parent):
        self.result = None

        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Room")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"+{x}+{y}")

        # Form
        ctk.CTkLabel(
            self.dialog, text="Room Details", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)

        form_frame = ctk.CTkFrame(self.dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Name
        ctk.CTkLabel(form_frame, text="Room Name:").pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Living Room")

        # Length
        ctk.CTkLabel(form_frame, text="Length (meters):").pack(pady=(10, 0))
        self.length_entry = ctk.CTkEntry(form_frame, width=300)
        self.length_entry.pack(pady=5)
        self.length_entry.insert(0, "5.0")

        # Width
        ctk.CTkLabel(form_frame, text="Width (meters):").pack(pady=(10, 0))
        self.width_entry = ctk.CTkEntry(form_frame, width=300)
        self.width_entry.pack(pady=5)
        self.width_entry.insert(0, "4.0")

        # Height
        ctk.CTkLabel(form_frame, text="Height (meters):").pack(pady=(10, 0))
        self.height_entry = ctk.CTkEntry(form_frame, width=300)
        self.height_entry.pack(pady=5)
        self.height_entry.insert(0, "3.0")

        # Buttons
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(button_frame, text="Cancel", command=self.dialog.destroy).pack(
            side="right", padx=5
        )
        ctk.CTkButton(button_frame, text="Add Room", command=self._submit).pack(
            side="right", padx=5
        )

    def _submit(self):
        """Submit the form"""
        try:
            self.result = {
                "name": self.name_entry.get(),
                "length": float(self.length_entry.get()),
                "width": float(self.width_entry.get()),
                "height": float(self.height_entry.get()),
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for dimensions!")

class RoofDialog:
    def __init__(self, parent):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Roof")
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(self.dialog, text="Roof Details", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self.dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="Roof Name:").pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Main Roof")
        
        # Roof Type
        ctk.CTkLabel(form_frame, text="Roof Type:").pack(pady=(10, 0))
        self.type_var = ctk.StringVar(value="gable")
        types = ['flat', 'gable', 'hip', 'shed']
        self.type_menu = ctk.CTkOptionMenu(form_frame, variable=self.type_var, 
                                            values=types, width=300)
        self.type_menu.pack(pady=5)
        
        # Covering Type
        ctk.CTkLabel(form_frame, text="Covering Type:").pack(pady=(10, 0))
        self.covering_var = ctk.StringVar(value="tiles")
        coverings = ['tiles', 'metal', 'shingles', 'concrete']
        self.covering_menu = ctk.CTkOptionMenu(form_frame, variable=self.covering_var, 
                                                values=coverings, width=300)
        self.covering_menu.pack(pady=5)
        
        # Area
        ctk.CTkLabel(form_frame, text="Area (m²):").pack(pady=(10, 0))
        self.area_entry = ctk.CTkEntry(form_frame, width=300)
        self.area_entry.pack(pady=5)
        self.area_entry.insert(0, "120")
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(button_frame, text="Cancel", 
                        command=self.dialog.destroy).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Add Roof", 
                        command=self._submit).pack(side="right", padx=5)
        
    def _submit(self):
        try:
            self.result = {
                'name': self.name_entry.get(),
                'roof_type': self.type_var.get(),
                'covering_type': int(self.covering_var.get()),
                'area': float(self.area_entry.get())
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
            
class WindowDialog:

    def __init__(self, parent):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Window")
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(self.dialog, text="Window Details", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self.dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="Window Name:").pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Living Room Window")
        
        # Window Type
        ctk.CTkLabel(form_frame, text="Window Type:").pack(pady=(10, 0))
        self.type_var = ctk.StringVar(value="single")
        types = ['single', 'double', 'bay', 'sliding', 'fixed']
        self.type_menu = ctk.CTkOptionMenu(form_frame, variable=self.type_var, 
                                           values=types, width=300)
        self.type_menu.pack(pady=5)
        
        # Quantity
        ctk.CTkLabel(form_frame, text="Quantity:").pack(pady=(10, 0))
        self.qty_entry = ctk.CTkEntry(form_frame, width=300)
        self.qty_entry.pack(pady=5)
        self.qty_entry.insert(0, "2")
        
        # Glass Type
        ctk.CTkLabel(form_frame, text="Glass Type:").pack(pady=(10, 0))
        self.glass_var = ctk.StringVar(value="single")
        glass_types = ['single', 'double', 'triple', 'tempered']
        self.glass_menu = ctk.CTkOptionMenu(form_frame, variable=self.glass_var, 
                                            values=glass_types, width=300)
        self.glass_menu.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(button_frame, text="Cancel", 
                     command=self.dialog.destroy).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Add Window", 
                     command=self._submit).pack(side="right", padx=5)

    def _submit(self):
            try:
                self.result = {
                    'name': self.name_entry.get(),
                    'window_type': self.type_var.get(),
                    'quantity': int(self.qty_entry.get()),
                    'glass_type': self.glass_var.get()
                }
                self.dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers!")

class ElectricalDialog:

    def __init__(self, parent):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Electrical System")
        self.dialog.geometry("400x380")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (380 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(self.dialog, text="Electrical System Details", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self.dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="System Name:").pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Floor Electrical System")
        
        # Area
        ctk.CTkLabel(form_frame, text="Coverage Area (m²):").pack(pady=(10, 0))
        self.area_entry = ctk.CTkEntry(form_frame, width=300)
        self.area_entry.pack(pady=5)
        self.area_entry.insert(0, "80")
        
        # Points (outlets + switches)
        ctk.CTkLabel(form_frame, text="Number of Points (outlets + switches):").pack(pady=(10, 0))
        self.points_entry = ctk.CTkEntry(form_frame, width=300)
        self.points_entry.pack(pady=5)
        self.points_entry.insert(0, "15")
        
        # Load
        ctk.CTkLabel(form_frame, text="Electrical Load (kW):").pack(pady=(10, 0))
        self.load_entry = ctk.CTkEntry(form_frame, width=300)
        self.load_entry.pack(pady=5)
        self.load_entry.insert(0, "5.0")
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(button_frame, text="Cancel", 
                     command=self.dialog.destroy).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Add System", 
                     command=self._submit).pack(side="right", padx=5)
    def _submit(self):
        try:
            self.result = {
                'name': self.name_entry.get(),
                'area': float(self.area_entry.get()),
                'points': int(self.points_entry.get()),
                'load_kw': float(self.load_entry.get())
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
    
class PlumbingDialog:

    def __init__(self, parent):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Plumbing System")
        self.dialog.geometry("400x380")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (380 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(self.dialog, text="Plumbing System Details", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self.dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="System Name:").pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Floor Plumbing System")
        
        # Fixtures
        ctk.CTkLabel(form_frame, text="Number of Fixtures:").pack(pady=(10, 0))
        self.fixtures_entry = ctk.CTkEntry(form_frame, width=300)
        self.fixtures_entry.pack(pady=5)
        self.fixtures_entry.insert(0, "5")
        
        # Pipe Length
        ctk.CTkLabel(form_frame, text="Total Pipe Length (meters):").pack(pady=(10, 0))
        self.pipe_entry = ctk.CTkEntry(form_frame, width=300)
        self.pipe_entry.pack(pady=5)
        self.pipe_entry.insert(0, "50")
        
        # Hot Water
        ctk.CTkLabel(form_frame, text="Include Hot Water System:").pack(pady=(10, 0))
        self.hot_water_var = ctk.StringVar(value="Yes")
        self.hot_water_check = ctk.CTkSwitch(form_frame, text="Yes", 
                                            variable=self.hot_water_var,
                                            onvalue="Yes", offvalue="No")
        self.hot_water_check.pack(pady=5)
        self.hot_water_check.select()
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(button_frame, text="Cancel", 
                    command=self.dialog.destroy).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Add System", 
                    command=self._submit).pack(side="right", padx=5)
    def _submit(self):
        try:
            self.result = {
                'name': self.name_entry.get(),
                'fixtures': int(self.fixtures_entry.get()),
                'pipe_length': float(self.pipe_entry.get()),
                'hot_water': self.hot_water_var.get() == "Yes"
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

class HVACDialog:

    def __init__(self, parent):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add HVAC System")
        self.dialog.geometry("400x330")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (330 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(self.dialog, text="HVAC System Details", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self.dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="System Name:").pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Central HVAC System")
        
        # Area
        ctk.CTkLabel(form_frame, text="Coverage Area (m²):").pack(pady=(10, 0))
        self.area_entry = ctk.CTkEntry(form_frame, width=300)
        self.area_entry.pack(pady=5)
        self.area_entry.insert(0, "100")
        
        # System Type
        ctk.CTkLabel(form_frame, text="System Type:").pack(pady=(10, 0))
        self.type_var = ctk.StringVar(value="split")
        types = ['split', 'central', 'ductless', 'vrf']
        self.type_menu = ctk.CTkOptionMenu(form_frame, variable=self.type_var, 
                                           values=types, width=300)
        self.type_menu.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(button_frame, text="Cancel", 
                     command=self.dialog.destroy).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Add System", 
                     command=self._submit).pack(side="right", padx=5)
    def _submit(self):
        try:
            self.result = {
                'name': self.name_entry.get(),
                'area': float(self.area_entry.get()),
                'system_type': self.type_var.get()
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

class PaintingDialog: 
    def __init__(self, parent):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Painting")
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(self.dialog, text="Painting Details", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self.dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="Painting Name:").pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Interior Painting")
        
        # Area
        ctk.CTkLabel(form_frame, text="Area (m²):").pack(pady=(10, 0))
        self.area_entry = ctk.CTkEntry(form_frame, width=300)
        self.area_entry.pack(pady=5)
        self.area_entry.insert(0, "150")
        
        # Paint Type
        ctk.CTkLabel(form_frame, text="Paint Type:").pack(pady=(10, 0))
        self.type_var = ctk.StringVar(value="interior")
        types = ['interior', 'exterior']
        self.type_menu = ctk.CTkOptionMenu(form_frame, variable=self.type_var, 
                                           values=types, width=300)
        self.type_menu.pack(pady=5)
        
        # Quality
        ctk.CTkLabel(form_frame, text="Quality:").pack(pady=(10, 0))
        self.quality_var = ctk.StringVar(value="standard")
        qualities = ['economy', 'standard', 'premium']
        self.quality_menu = ctk.CTkOptionMenu(form_frame, variable=self.quality_var, 
                                              values=qualities, width=300)
        self.quality_menu.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(button_frame, text="Cancel", 
                     command=self.dialog.destroy).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Add Painting", 
                     command=self._submit).pack(side="right", padx=5)
    
    def _submit(self):
        try:
            self.result = {
                'name': self.name_entry.get(),
                'area': float(self.area_entry.get()),
                'paint_type': self.type_var.get(),
                'quality': self.quality_var.get()
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
    
class FlooringDialog: 
    def __init__(self, parent):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Flooring")
        self.dialog.geometry("400x320")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (320 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(self.dialog, text="Flooring Details", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self.dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="Flooring Name:").pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Living Room Flooring")
        
        # Area
        ctk.CTkLabel(form_frame, text="Area (m²):").pack(pady=(10, 0))
        self.area_entry = ctk.CTkEntry(form_frame, width=300)
        self.area_entry.pack(pady=5)
        self.area_entry.insert(0, "40")
        
        # Flooring Type
        ctk.CTkLabel(form_frame, text="Flooring Type:").pack(pady=(10, 0))
        self.type_var = ctk.StringVar(value="ceramic")
        types = ['ceramic', 'porcelain', 'marble', 'granite', 'hardwood', 'laminate', 'vinyl', 'carpet']
        self.type_menu = ctk.CTkOptionMenu(form_frame, variable=self.type_var, 
                                           values=types, width=300)
        self.type_menu.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(button_frame, text="Cancel", 
                     command=self.dialog.destroy).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Add Flooring", 
                     command=self._submit).pack(side="right", padx=5)
    def _submit(self):
        try:
            self.result = {
                'name': self.name_entry.get(),
                'area': float(self.area_entry.get()),
                'flooring_type': self.type_var.get()
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

class PlasteringDialog: 
    def __init__(self, parent):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Plastering")
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(self.dialog, text="Plastering Details", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self.dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="Plastering Name:").pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Wall Plastering")
        
        # Area
        ctk.CTkLabel(form_frame, text="Area (m²):").pack(pady=(10, 0))
        self.area_entry = ctk.CTkEntry(form_frame, width=300)
        self.area_entry.pack(pady=5)
        self.area_entry.insert(0, "100")
        
        # Thickness
        ctk.CTkLabel(form_frame, text="Thickness (meters):").pack(pady=(10, 0))
        self.thickness_entry = ctk.CTkEntry(form_frame, width=300)
        self.thickness_entry.pack(pady=5)
        self.thickness_entry.insert(0, "0.015")
        
        # Plaster Type
        ctk.CTkLabel(form_frame, text="Plaster Type:").pack(pady=(10, 0))
        self.type_var = ctk.StringVar(value="cement")
        types = ['cement', 'gypsum', 'lime']
        self.type_menu = ctk.CTkOptionMenu(form_frame, variable=self.type_var, 
                                           values=types, width=300)
        self.type_menu.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(button_frame, text="Cancel", 
                     command=self.dialog.destroy).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Add Plastering", 
                     command=self._submit).pack(side="right", padx=5)
    def _submit(self):
        try:
            self.result = {
                'name': self.name_entry.get(),
                'area': float(self.area_entry.get()),
                'thickness': float(self.thickness_entry.get()),
                'plaster_type': self.type_var.get()
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")    
        
class StaircaseDialog:
    def __init__(self, parent) -> None:
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Staircase")
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(self.dialog, text="Staircase Details", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self.dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="Staircase Name:").pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Main Staircase")
        
        # Floor Height
        ctk.CTkLabel(form_frame, text="Floor Height (meters):").pack(pady=(10, 0))
        self.height_entry = ctk.CTkEntry(form_frame, width=300)
        self.height_entry.pack(pady=5)
        self.height_entry.insert(0, "3.0")
        
        # Width
        ctk.CTkLabel(form_frame, text="Width (meters):").pack(pady=(10, 0))
        self.width_entry = ctk.CTkEntry(form_frame, width=300)
        self.width_entry.pack(pady=5)
        self.width_entry.insert(0, "1.2")
        
        # Material
        ctk.CTkLabel(form_frame, text="Material:").pack(pady=(10, 0))
        self.material_var = ctk.StringVar(value="concrete")
        materials = ['concrete', 'wood']
        self.material_menu = ctk.CTkOptionMenu(form_frame, variable=self.material_var, 
                                               values=materials, width=300)
        self.material_menu.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(button_frame, text="Cancel", 
                     command=self.dialog.destroy).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Add Staircase", 
                                          command=self._submit).pack(side="right", padx=5)
                         
    def _submit(self):
        try:
            self.result = {
                'name': self.name_entry.get(),
                'floor_height': float(self.height_entry.get()),
                'width': float(self.width_entry.get()),
                'material': self.material_var.get()
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
class DrainageDialog:
    """Dialog for adding drainage system"""
    
    def __init__(self, parent):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Drainage System")
        self.dialog.geometry("400x380")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (380 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(self.dialog, text="Drainage System Details", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self.dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="Drainage Name:").pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Main Drainage System")
        
        # Length
        ctk.CTkLabel(form_frame, text="Total Length (meters):").pack(pady=(10, 0))
        self.length_entry = ctk.CTkEntry(form_frame, width=300)
        self.length_entry.pack(pady=5)
        self.length_entry.insert(0, "150")
        
        # Pipe Diameter
        ctk.CTkLabel(form_frame, text="Pipe Diameter (meters):").pack(pady=(10, 0))
        self.diameter_entry = ctk.CTkEntry(form_frame, width=300)
        self.diameter_entry.pack(pady=5)
        self.diameter_entry.insert(0, "0.3")
        
        # System Type
        ctk.CTkLabel(form_frame, text="System Type:").pack(pady=(10, 0))
        self.type_var = ctk.StringVar(value="surface")
        types = ['surface', 'subsurface', 'combined']
        self.type_menu = ctk.CTkOptionMenu(form_frame, variable=self.type_var, 
                                            values=types, width=300)
        self.type_menu.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(button_frame, text="Cancel", 
                        command=self.dialog.destroy).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Add Drainage", 
                        command=self._submit).pack(side="right", padx=5)
    
    def _submit(self):
        try:
            self.result = {
                'name': self.name_entry.get(),
                'length': float(self.length_entry.get()),
                'pipe_diameter': float(self.diameter_entry.get()),
                'system_type': self.type_var.get()
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

class RoadDialog:
    """Dialog for adding road"""
    
    def __init__(self, parent):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Road")
        self.dialog.geometry("400x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(self.dialog, text="Road Details", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self.dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="Road Name:").pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Main Access Road")
        
        # Length
        ctk.CTkLabel(form_frame, text="Length (meters):").pack(pady=(10, 0))
        self.length_entry = ctk.CTkEntry(form_frame, width=300)
        self.length_entry.pack(pady=5)
        self.length_entry.insert(0, "100")
        
        # Width
        ctk.CTkLabel(form_frame, text="Width (meters):").pack(pady=(10, 0))
        self.width_entry = ctk.CTkEntry(form_frame, width=300)
        self.width_entry.pack(pady=5)
        self.width_entry.insert(0, "6.0")
        
        # Road Type
        ctk.CTkLabel(form_frame, text="Road Type:").pack(pady=(10, 0))
        self.type_var = ctk.StringVar(value="asphalt")
        types = ['asphalt', 'concrete', 'gravel']
        self.type_menu = ctk.CTkOptionMenu(form_frame, variable=self.type_var, 
                                           values=types, width=300)
        self.type_menu.pack(pady=5)
        
        # Traffic Level
        ctk.CTkLabel(form_frame, text="Traffic Level:").pack(pady=(10, 0))
        self.traffic_var = ctk.StringVar(value="medium")
        levels = ['light', 'medium', 'heavy']
        self.traffic_menu = ctk.CTkOptionMenu(form_frame, variable=self.traffic_var, 
                                              values=levels, width=300)
        self.traffic_menu.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(button_frame, text="Cancel", 
                     command=self.dialog.destroy).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Add Road", 
                     command=self._submit).pack(side="right", padx=5)
    def _submit(self):
        try:
            self.result = {
                'name': self.name_entry.get(),
                'length': float(self.length_entry.get()),
                'width': float(self.width_entry.get()),
                'road_type': self.type_var.get(),
                'traffic_level': self.traffic_var.get()
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

# Add similar dialogs for: Window, Roof, Electrical, Plumbing, HVAC,
# Painting, Flooring, Plastering, Staircase, Road, Drainage