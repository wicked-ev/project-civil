"""
Construction Cost Estimator Application
A modern, component-based GUI application for calculating construction costs.

Requirements:
pip install customtkinter
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from uuid import uuid4
import json
import csv

# ============================================================================
# DATA MODEL
# ============================================================================

@dataclass
class Material:
    """Base material with cost information"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    unit: str = ""
    unit_cost: float = 0.0
    quantity: float = 0.0

    def total_cost(self) -> float:
        return self.unit_cost * self.quantity

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'unit': self.unit,
            'unit_cost': self.unit_cost,
            'quantity': self.quantity
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Material':
        return cls(**data)

class Component(ABC):
    """Abstract base class for all construction components"""

    def __init__(self, name: str, component_id: Optional[str] = None):
        self.id = component_id or str(uuid4())
        self.name = name
        self.children: List[Component] = []
        self.materials: List[Material] = []

    @abstractmethod
    def calculate_cost(self) -> float:
        pass

    @abstractmethod
    def get_material_breakdown(self) -> Dict[str, float]:
        pass

    def add_child(self, component: 'Component'):
        self.children.append(component)

    def remove_child(self, component_id: str):
        self.children = [c for c in self.children if c.id != component_id]

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.__class__.__name__,
            'materials': [m.to_dict() for m in self.materials],
            'children': [c.to_dict() for c in self.children],
            'properties': self._get_properties()
        }

    @abstractmethod
    def _get_properties(self) -> Dict:
        """Get component-specific properties"""
        pass

class Wall(Component):
    def __init__(self, name: str, length: float, height: float,
                 thickness: float = 0.23, component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.length = length
        self.height = height
        self.thickness = thickness
        self._calculate_materials()

    def _calculate_materials(self):
        volume = self.length * self.height * self.thickness
        brick_count = volume * 500
        cement_bags = volume * 8
        sand_cubic_meters = volume * 1.2

        self.materials = [
            Material(name="Brick", unit="pieces", quantity=brick_count, unit_cost=0.5),
            Material(name="Cement", unit="bags", quantity=cement_bags, unit_cost=8.0),
            Material(name="Sand", unit="m³", quantity=sand_cubic_meters, unit_cost=25.0),
            Material(name="Labor", unit="hours", quantity=volume * 10, unit_cost=15.0)
        ]

    def calculate_cost(self) -> float:
        material_cost = sum(m.total_cost() for m in self.materials)
        children_cost = sum(c.calculate_cost() for c in self.children)
        return material_cost + children_cost

    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        for child in self.children:
            child_breakdown = child.get_material_breakdown()
            for key, qty in child_breakdown.items():
                breakdown[key] = breakdown.get(key, 0) + qty
        return breakdown

    def _get_properties(self) -> Dict:
        return {'length': self.length, 'height': self.height, 'thickness': self.thickness}

class Room(Component):
    def __init__(self, name: str, length: float, width: float,
                 height: float = 3.0, component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.length = length
        self.width = width
        self.height = height
        self._create_default_structure()

    def _create_default_structure(self):
        self.add_child(Wall(f"{self.name} - North Wall", self.length, self.height))
        self.add_child(Wall(f"{self.name} - South Wall", self.length, self.height))
        self.add_child(Wall(f"{self.name} - East Wall", self.width, self.height))
        self.add_child(Wall(f"{self.name} - West Wall", self.width, self.height))

        floor_area = self.length * self.width
        self.materials = [
            Material(name="Floor Tiles", unit="m²", quantity=floor_area, unit_cost=20.0),
            Material(name="Floor Cement", unit="bags", quantity=floor_area * 0.5, unit_cost=8.0)
        ]

    def calculate_cost(self) -> float:
        material_cost = sum(m.total_cost() for m in self.materials)
        children_cost = sum(c.calculate_cost() for c in self.children)
        return material_cost + children_cost

    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        for child in self.children:
            child_breakdown = child.get_material_breakdown()
            for key, qty in child_breakdown.items():
                breakdown[key] = breakdown.get(key, 0) + qty
        return breakdown

    def _get_properties(self) -> Dict:
        return {'length': self.length, 'width': self.width, 'height': self.height}

class Floor(Component):
    def __init__(self, name: str, floor_number: int, component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.floor_number = floor_number

    def calculate_cost(self) -> float:
        return sum(c.calculate_cost() for c in self.children)

    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for child in self.children:
            child_breakdown = child.get_material_breakdown()
            for key, qty in child_breakdown.items():
                breakdown[key] = breakdown.get(key, 0) + qty
        return breakdown

    def _get_properties(self) -> Dict:
        return {'floor_number': self.floor_number}

class Building(Component):
    def __init__(self, name: str, building_type: str = "Residential",
                 component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.building_type = building_type

    def calculate_cost(self) -> float:
        return sum(c.calculate_cost() for c in self.children)

    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for child in self.children:
            child_breakdown = child.get_material_breakdown()
            for key, qty in child_breakdown.items():
                breakdown[key] = breakdown.get(key, 0) + qty
        return breakdown

    def _get_properties(self) -> Dict:
        return {'building_type': self.building_type}

class Project(Component):
    def __init__(self, name: str, description: str = "",
                 component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.description = description

    def calculate_cost(self) -> float:
        return sum(c.calculate_cost() for c in self.children)

    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for child in self.children:
            child_breakdown = child.get_material_breakdown()
            for key, qty in child_breakdown.items():
                breakdown[key] = breakdown.get(key, 0) + qty
        return breakdown

    def _get_properties(self) -> Dict:
        return {'description': self.description}

# ============================================================================
# GUI APPLICATION
# ============================================================================

class ConstructionEstimatorApp:
    def __init__(self):
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.root = ctk.CTk()
        self.root.title("Construction Cost Estimator")
        self.root.geometry("1200x800")

        # Initialize data
        self.current_project: Optional[Project] = None

        # Setup GUI
        self._create_menu()
        self._create_layout()

    def _create_menu(self):
        """Create top menu bar"""
        menu_frame = ctk.CTkFrame(self.root, height=50)
        menu_frame.pack(fill="x", padx=10, pady=(10, 0))

        ctk.CTkLabel(menu_frame, text="Construction Cost Estimator",
                    font=ctk.CTkFont(size=20, weight="bold")).pack(side="left", padx=20)

        ctk.CTkButton(menu_frame, text="New Project", command=self._new_project,
                     width=120).pack(side="right", padx=5, pady=10)
        ctk.CTkButton(menu_frame, text="Save Project", command=self._save_project,
                     width=120).pack(side="right", padx=5, pady=10)
        ctk.CTkButton(menu_frame, text="Load Project", command=self._load_project,
                     width=120).pack(side="right", padx=5, pady=10)
        ctk.CTkButton(menu_frame, text="Export CSV", command=self._export_csv,
                     width=120).pack(side="right", padx=5, pady=10)

    def _create_layout(self):
        """Create main application layout"""
        # Main container
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel: Project builder
        left_panel = ctk.CTkFrame(main_container, width=400)
        left_panel.pack(side="left", fill="both", expand=False, padx=(0, 5))
        left_panel.pack_propagate(False)

        ctk.CTkLabel(left_panel, text="Project Builder",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        # Project info section
        self.project_name_var = ctk.StringVar(value="New Project")
        ctk.CTkLabel(left_panel, text="Project Name:").pack(pady=(10, 0))
        ctk.CTkEntry(left_panel, textvariable=self.project_name_var,
                    width=350).pack(pady=5)

        # Quick add section
        quick_add_frame = ctk.CTkFrame(left_panel)
        quick_add_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(quick_add_frame, text="Quick Add Components",
                    font=ctk.CTkFont(weight="bold")).pack(pady=5)

        ctk.CTkButton(quick_add_frame, text="+ Add Building",
                     command=self._add_building).pack(fill="x", pady=2)
        ctk.CTkButton(quick_add_frame, text="+ Add Floor",
                     command=self._add_floor).pack(fill="x", pady=2)
        ctk.CTkButton(quick_add_frame, text="+ Add Room",
                     command=self._add_room).pack(fill="x", pady=2)

        # Component tree
        tree_frame = ctk.CTkFrame(left_panel)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(tree_frame, text="Project Structure").pack()

        self.tree_text = ctk.CTkTextbox(tree_frame, width=350)
        self.tree_text.pack(fill="both", expand=True, pady=5)

        # Right panel: Cost summary
        right_panel = ctk.CTkFrame(main_container)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))

        ctk.CTkLabel(right_panel, text="Cost Summary",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        # Total cost display
        cost_display_frame = ctk.CTkFrame(right_panel, fg_color=("gray85", "gray25"))
        cost_display_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(cost_display_frame, text="Total Project Cost:",
                    font=ctk.CTkFont(size=14)).pack(pady=(10, 0))
        self.total_cost_label = ctk.CTkLabel(cost_display_frame, text="$0.00",
                                             font=ctk.CTkFont(size=32, weight="bold"))
        self.total_cost_label.pack(pady=(0, 10))

        # Material breakdown
        ctk.CTkLabel(right_panel, text="Material Breakdown",
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))

        self.breakdown_text = ctk.CTkTextbox(right_panel, height=400)
        self.breakdown_text.pack(fill="both", expand=True, padx=20, pady=5)

        # Calculate button
        ctk.CTkButton(right_panel, text="Calculate Costs",
                     command=self._calculate_costs, height=40,
                     font=ctk.CTkFont(size=14, weight="bold")).pack(fill="x",
                                                                    padx=20, pady=10)

        # Initialize empty project
        self._new_project()

    def _new_project(self):
        """Create a new project"""
        project_name = self.project_name_var.get() or "New Project"
        self.current_project = Project(project_name, "Construction project")
        self._update_displays()
        messagebox.showinfo("Success", f"New project '{project_name}' created!")

    def _add_building(self):
        """Add a building to the project"""
        if not self.current_project:
            messagebox.showerror("Error", "Please create a project first!")
            return

        dialog = ctk.CTkInputDialog(text="Building Name:", title="Add Building")
        name = dialog.get_input()
        if name:
            building = Building(name, "Residential")
            self.current_project.add_child(building)
            self._update_displays()

    def _add_floor(self):
        """Add a floor to the last building"""
        if not self.current_project or not self.current_project.children:
            messagebox.showerror("Error", "Please add a building first!")
            return

        building = self.current_project.children[-1]
        if not isinstance(building, Building):
            messagebox.showerror("Error", "Last component is not a building!")
            return

        floor_num = len(building.children) + 1
        floor = Floor(f"Floor {floor_num}", floor_num)
        building.add_child(floor)
        self._update_displays()

    def _add_room(self):
        """Add a room to the last floor"""
        if not self.current_project or not self.current_project.children:
            messagebox.showerror("Error", "Please add a building and floor first!")
            return

        building = self.current_project.children[-1]
        if not building.children:
            messagebox.showerror("Error", "Please add a floor first!")
            return

        floor = building.children[-1]
        if not isinstance(floor, Floor):
            messagebox.showerror("Error", "Last component is not a floor!")
            return

        dialog = RoomDialog(self.root)
        self.root.wait_window(dialog.dialog)

        if dialog.result:
            room = Room(dialog.result['name'], dialog.result['length'],
                       dialog.result['width'], dialog.result['height'])
            floor.add_child(room)
            self._update_displays()

    def _update_displays(self):
        """Update all display components"""
        self._update_tree()
        self._calculate_costs()

    def _update_tree(self):
        """Update the component tree display"""
        self.tree_text.delete("1.0", "end")
        if self.current_project:
            tree_str = self._build_tree_string(self.current_project, 0)
            self.tree_text.insert("1.0", tree_str)

    def _build_tree_string(self, component: Component, level: int) -> str:
        """Recursively build tree string"""
        indent = "  " * level
        result = f"{indent}├─ {component.name} ({component.__class__.__name__})\n"
        for child in component.children:
            result += self._build_tree_string(child, level + 1)
        return result

    def _calculate_costs(self):
        """Calculate and display costs"""
        if not self.current_project:
            return

        total_cost = self.current_project.calculate_cost()
        self.total_cost_label.configure(text=f"${total_cost:,.2f}")

        breakdown = self.current_project.get_material_breakdown()
        self.breakdown_text.delete("1.0", "end")

        breakdown_str = "Material                          Quantity\n"
        breakdown_str += "─" * 55 + "\n"

        for material, qty in sorted(breakdown.items()):
            breakdown_str += f"{material:<35} {qty:>15,.2f}\n"

        self.breakdown_text.insert("1.0", breakdown_str)

    def _save_project(self):
        """Save project to JSON file"""
        if not self.current_project:
            messagebox.showerror("Error", "No project to save!")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.current_project.to_dict(), f, indent=2)
                messagebox.showinfo("Success", "Project saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")

    def _load_project(self):
        """Load project from JSON file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                # Note: Full deserialization would need more implementation
                messagebox.showinfo("Info", "Load functionality requires full deserialization implementation")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {str(e)}")

    def _export_csv(self):
        """Export cost breakdown to CSV"""
        if not self.current_project:
            messagebox.showerror("Error", "No project to export!")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filename:
            try:
                breakdown = self.current_project.get_material_breakdown()
                with open(filename, 'w', newline='') as f:
                          writer = csv.writer(f)
                          writer.writerow(['Material', 'Quantity', 'Total Cost'])

                          total_cost = self.current_project.calculate_cost()
                          for material, qty in sorted(breakdown.items()):
                              writer.writerow([material, f"{qty:.2f}", ""])

                          writer.writerow([])
                          writer.writerow(['Total Project Cost', '', f"${total_cost:,.2f}"])

                          messagebox.showinfo("Success", "Export completed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def run(self):
        """Start the application"""
        self.root.mainloop()

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
        ctk.CTkLabel(self.dialog, text="Room Details",
        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)

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

        ctk.CTkButton(button_frame, text="Cancel",
                           command=self.dialog.destroy).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Add Room",
                           command=self._submit).pack(side="right", padx=5)

    def _submit(self):
        """Submit the form"""
        try:
            self.result = {
                      'name': self.name_entry.get(),
                      'length': float(self.length_entry.get()),
                      'width': float(self.width_entry.get()),
                      'height': float(self.height_entry.get())
                  }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for dimensions!")

      # ============================================================================
      # MAIN
      # ============================================================================

if __name__ == "__main__":
    app = ConstructionEstimatorApp()
    app.run()
