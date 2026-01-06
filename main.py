"""
Construction Cost Estimator Application
A modern, component-based GUI application for calculating construction costs.

Requirements:
pip install customtkinter
"""

import csv
import json
from tkinter import filedialog, messagebox
from typing import Optional
import customtkinter as ctk

from data_model import Building, Component, Floor, Project, Room, Foundation, Roof, Window, Door, ElectricalSystem, PlumbingSystem, HVACSystem, Flooring, Painting, Plastering, Staircase, Drainage, Road
from dialogs import FoundationDialog, DoorDialog, RoomDialog, RoofDialog, ElectricalDialog, FlooringDialog, WindowDialog, DrainageDialog, StaircaseDialog, PlumbingDialog, PlasteringDialog, PaintingDialog, RoadDialog, HVACDialog
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

        ctk.CTkLabel(
            menu_frame,
            text="Construction Cost Estimator",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            menu_frame, text="New Project", command=self._new_project, width=120
        ).pack(side="right", padx=5, pady=10)
        ctk.CTkButton(
            menu_frame, text="Save Project", command=self._save_project, width=120
        ).pack(side="right", padx=5, pady=10)
        ctk.CTkButton(
            menu_frame, text="Load Project", command=self._load_project, width=120
        ).pack(side="right", padx=5, pady=10)
        ctk.CTkButton(
            menu_frame, text="Export CSV", command=self._export_csv, width=120
        ).pack(side="right", padx=5, pady=10)

    def _create_layout(self):
        """Create main application layout"""
        # Main container
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel: Project builder
        left_panel = ctk.CTkFrame(main_container, width=400)
        left_panel.pack(side="left", fill="both", expand=False, padx=(0, 5))
        left_panel.pack_propagate(False)

        ctk.CTkLabel(
            left_panel, text="Project Builder", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        # Project info section
        self.project_name_var = ctk.StringVar(value="New Project")
        ctk.CTkLabel(left_panel, text="Project Name:").pack(pady=(10, 0))
        ctk.CTkEntry(left_panel, textvariable=self.project_name_var, width=350).pack(
            pady=5
        )

        # Quick add section
        quick_add_frame = ctk.CTkScrollableFrame(
            left_panel,
            height=200,        # fixed visible height
            width=300          # optional fixed width
        )
        
        quick_add_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(
            quick_add_frame,
            text="Quick Add Components",
            font=ctk.CTkFont(weight="bold"),
        ).pack(pady=5)

        ctk.CTkButton(
            quick_add_frame, text="+ Add Building", command=self._add_building
        ).pack(fill="x", pady=2)
        ctk.CTkButton(
            quick_add_frame, text="+ Add Floor", command=self._add_floor
        ).pack(fill="x", pady=2)
        ctk.CTkButton(quick_add_frame, text="+ Add Room", command=self._add_room).pack(
            fill="x", pady=2
        )

        ctk.CTkLabel(
            quick_add_frame, text="Structural", font=ctk.CTkFont(weight="bold")
        ).pack(pady=(10, 5))
        ctk.CTkButton(
            quick_add_frame, text="+ Add Foundation", command=self._add_foundation
        ).pack(fill="x", pady=2)
        ctk.CTkButton(quick_add_frame, text="+ Add Roof", command=self._add_roof).pack(
            fill="x", pady=2
        )
        ctk.CTkButton(
            quick_add_frame, text="+ Add Staircase", command=self._add_staircase
        ).pack(fill="x", pady=2)

        ctk.CTkLabel(
            quick_add_frame, text="Doors & Windows", font=ctk.CTkFont(weight="bold")
        ).pack(pady=(10, 5))
        ctk.CTkButton(quick_add_frame, text="+ Add Door", command=self._add_door).pack(
            fill="x", pady=2
        )
        ctk.CTkButton(
            quick_add_frame, text="+ Add Window", command=self._add_window
        ).pack(fill="x", pady=2)

        # MEP Systems
        ctk.CTkLabel(
            quick_add_frame, text="MEP Systems", font=ctk.CTkFont(weight="bold")
        ).pack(pady=(10, 5))
        ctk.CTkButton(
            quick_add_frame, text="+ Add Electrical", command=self._add_electrical
        ).pack(fill="x", pady=2)
        ctk.CTkButton(
            quick_add_frame, text="+ Add Plumbing", command=self._add_plumbing
        ).pack(fill="x", pady=2)
        ctk.CTkButton(quick_add_frame, text="+ Add HVAC", command=self._add_hvac).pack(
            fill="x", pady=2
        )

        # Finishing
        ctk.CTkLabel(
            quick_add_frame, text="Finishing", font=ctk.CTkFont(weight="bold")
        ).pack(pady=(10, 5))
        ctk.CTkButton(
            quick_add_frame, text="+ Add Painting", command=self._add_painting
        ).pack(fill="x", pady=2)
        ctk.CTkButton(
            quick_add_frame, text="+ Add Flooring", command=self._add_flooring
        ).pack(fill="x", pady=2)
        ctk.CTkButton(
            quick_add_frame, text="+ Add Plastering", command=self._add_plastering
        ).pack(fill="x", pady=2)

        # Infrastructure
        ctk.CTkLabel(
            quick_add_frame, text="Site Works", font=ctk.CTkFont(weight="bold")
        ).pack(pady=(10, 5))
        ctk.CTkButton(quick_add_frame, text="+ Add Road", command=self._add_road).pack(
            fill="x", pady=2
        )
        ctk.CTkButton(
            quick_add_frame, text="+ Add Drainage", command=self._add_drainage
        ).pack(fill="x", pady=2)
        # Component tree
        tree_frame = ctk.CTkFrame(left_panel)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(tree_frame, text="Project Structure").pack()

        self.tree_text = ctk.CTkTextbox(tree_frame, width=350)
        self.tree_text.pack(fill="both", expand=True, pady=5)

        # Selection menu for where to add components
        self.selection_var = ctk.StringVar(value="Use last (default)")
        self.selection_map = {}
        self.selection_menu = ctk.CTkOptionMenu(
            tree_frame,
            variable=self.selection_var,
            values=["Use last (default)"],
            width=350,
        )
        self.selection_menu.pack(pady=5)

        # Right panel: Cost summary
        right_panel = ctk.CTkFrame(main_container)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))

        ctk.CTkLabel(
            right_panel, text="Cost Summary", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        # Total cost display
        cost_display_frame = ctk.CTkFrame(right_panel, fg_color=("gray85", "gray25"))
        cost_display_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            cost_display_frame, text="Total Project Cost:", font=ctk.CTkFont(size=14)
        ).pack(pady=(10, 0))
        self.total_cost_label = ctk.CTkLabel(
            cost_display_frame, text="$0.00", font=ctk.CTkFont(size=32, weight="bold")
        )
        self.total_cost_label.pack(pady=(0, 10))

        # Material breakdown
        ctk.CTkLabel(
            right_panel,
            text="Material Breakdown",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(pady=(10, 5))

        self.breakdown_text = ctk.CTkTextbox(right_panel, height=400)
        self.breakdown_text.pack(fill="both", expand=True, padx=20, pady=5)

        # Calculate button
        ctk.CTkButton(
            right_panel,
            text="Calculate Costs",
            command=self._calculate_costs,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(fill="x", padx=20, pady=10)

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
        # Determine target floor based on selection UI if present
        target_floor = None

        sel = getattr(self, 'selection_var', None)
        if sel and sel.get() and sel.get() != "Use last (default)":
            target = self.selection_map.get(sel.get())
            if target:
                # If user selected a Floor directly
                if isinstance(target, Floor):
                    target_floor = target
                # If user selected a Room, add to its parent floor
                elif isinstance(target, Room):
                    parent = self._find_parent(self.current_project, target.id)
                    if isinstance(parent, Floor):
                        target_floor = parent
                # If user selected a Building, use its last floor
                elif isinstance(target, Building):
                    if target.children and isinstance(target.children[-1], Floor):
                        target_floor = target.children[-1]

        # Fallback: use last building -> last floor
        if target_floor is None:
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

            target_floor = floor

        dialog = RoomDialog(self.root)
        self.root.wait_window(dialog.dialog)

        if dialog.result:
            room = Room(
                dialog.result["name"],
                dialog.result["length"],
                dialog.result["width"],
                dialog.result["height"],
            )
            target_floor.add_child(room)
            self._update_displays()

    def _find_parent(self, root: Component, target_id: str):
        """Find parent of component with id `target_id` in tree rooted at `root`.
        Returns the parent component or None.
        """
        for child in root.children:
            if getattr(child, 'id', None) == target_id:
                return root
            found = self._find_parent(child, target_id)
            if found:
                return found
        return None

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
            # Update selection menu
            items = self._build_selection_items(self.current_project)
            values = ["Use last (default)"] + [d for d, _ in items]
            # rebuild mapping
            self.selection_map = {d: comp for d, comp in items}
            try:
                self.selection_menu.configure(values=values)
            except Exception:
                pass
            # keep current selection if still valid
            if self.selection_var.get() not in values:
                self.selection_var.set("Use last (default)")

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
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )

        if filename:
            try:
                with open(filename, "w") as f:
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
                with open(filename, "r") as f:
                    data = json.load(f)

                # Reconstruct full project graph from the saved dict
                try:
                    project = Project.from_dict(data)
                except Exception:
                    # Fallback: try wrapping inside Project if top-level was nested
                    project = Project.from_dict({
                        'id': data.get('id'),
                        'name': data.get('name', 'Loaded Project'),
                        'type': data.get('type', 'Project'),
                        'materials': data.get('materials', []),
                        'children': data.get('children', []),
                        'properties': data.get('properties', {})
                    })

                self.current_project = project
                self.project_name_var.set(self.current_project.name)
                self._update_displays()
                messagebox.showinfo("Success", "Project loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {str(e)}")

    def _add_foundation(self):
        """Add foundation to building"""
        if not self.current_project or not self.current_project.children:
            messagebox.showerror("Error", "Please add a building first!")
            return

        building = self.current_project.children[-1]
        dialog = FoundationDialog(self.root)
        self.root.wait_window(dialog.dialog)
        if dialog.result:
            foundation = Foundation(
                            dialog.result["name"],
                            dialog.result["foundation_type"],
                            dialog.result["area"],
                            dialog.result["soil_type"],
                        )
            building.add_child(foundation)
            self._update_displays()

    def _add_roof(self):
        """Add roof to building"""
        if not self.current_project or not self.current_project.children:
            messagebox.showerror("Error", "Please add a building first!")
            return
        
        building = self.current_project.children[-1]
        dialog = RoofDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            roof = Roof(
                dialog.result['name'],
                dialog.result['roof_type'],
                dialog.result['covering_type'],
                dialog.result['area']
            )
            building.add_child(roof)
            self._update_displays()
    
    def _add_door(self):
        """Add door to room"""
        if not self.current_project:
            messagebox.showerror("Error", "Please create a project first!")
            return
        
        dialog = DoorDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            door = Door(
                dialog.result['name'],
                dialog.result['door_type'],
                dialog.result['quantity'],
                dialog.result['material']
            )
            # Add to last room or floor
            self._add_to_last_room_or_floor(door)
        
    def _add_window(self):
        """Add window to room"""
        if not self.current_project:
            messagebox.showerror("Error", "Please create a project first!")
            return
        
        dialog = WindowDialog(self.root)
        self.root.wait_window(dialog.dialog)        
        if dialog.result:
            window = Window(
                dialog.result['name'],
                dialog.result['window_type'],
                dialog.result['quantity'],
                dialog.result['glass_type']
            )
            self._add_to_last_room_or_floor(window)
    
    def _add_electrical(self):
        """Add electrical system to room/floor"""
        if not self.current_project:
            messagebox.showerror("Error", "Please create a project first!")
            return
        
        dialog = ElectricalDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            electrical = ElectricalSystem(
                dialog.result['name'],
                dialog.result['area'],
                dialog.result['points'],
                dialog.result['load_kw']
            )
            self._add_to_last_room_or_floor(electrical)
            
    def _add_plumbing(self):
        """Add plumbing system"""
        if not self.current_project:
            messagebox.showerror("Error", "Please create a project first!")
            return
        
        dialog = PlumbingDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            plumbing = PlumbingSystem(
                dialog.result['name'],
                dialog.result['fixtures'],
                dialog.result['pipe_length'],
                dialog.result['hot_water']
            )
            self._add_to_last_room_or_floor(plumbing)
    
    def _add_hvac(self):
        """Add HVAC system"""
        if not self.current_project:
            messagebox.showerror("Error", "Please create a project first!")
            return
        
        dialog = HVACDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            hvac = HVACSystem(
                dialog.result['name'],
                dialog.result['area'],
                dialog.result['system_type']
            )
            self._add_to_last_room_or_floor(hvac)
    
    def _add_painting(self):
        """Add painting"""
        if not self.current_project:
            messagebox.showerror("Error", "Please create a project first!")
            return
        
        dialog = PaintingDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            painting = Painting(
                dialog.result['name'],
                dialog.result['area'],
                dialog.result['paint_type'],
                dialog.result['quality']
            )
            self._add_to_last_room_or_floor(painting)
    
    def _add_flooring(self):
        """Add flooring"""
        if not self.current_project:
            messagebox.showerror("Error", "Please create a project first!")
            return
        
        dialog = FlooringDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            flooring = Flooring(
                dialog.result['name'],
                dialog.result['area'],
                dialog.result['flooring_type']
            )
            self._add_to_last_room_or_floor(flooring)
    
    def _add_plastering(self):
        """Add plastering"""
        if not self.current_project:
            messagebox.showerror("Error", "Please create a project first!")
            return
        
        dialog = PlasteringDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            plastering = Plastering(
                dialog.result['name'],
                dialog.result['area'],
                dialog.result['thickness'],
                dialog.result['plaster_type']
            )
            self._add_to_last_room_or_floor(plastering)
    
    def _add_staircase(self):
        """Add staircase to building"""
        if not self.current_project or not self.current_project.children:
            messagebox.showerror("Error", "Please add a building first!")
            return
        
        building = self.current_project.children[-1]
        dialog = StaircaseDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            staircase = Staircase(
                dialog.result['name'],
                dialog.result['floor_height'],
                dialog.result['width'],
                dialog.result['material']
            )
            building.add_child(staircase)
            self._update_displays()
    
    def _add_road(self):
        """Add road to project"""
        if not self.current_project:
            messagebox.showerror("Error", "Please create a project first!")
            return
        
        dialog = RoadDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            road = Road(
                dialog.result['name'],
                dialog.result['length'],
                dialog.result['width'],
                dialog.result['road_type'],
                dialog.result['traffic_level']
            )
            self.current_project.add_child(road)
            self._update_displays()
    
    def _add_drainage(self):
        """Add drainage system"""
        if not self.current_project:
            messagebox.showerror("Error", "Please create a project first!")
            return
        
        dialog = DrainageDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            drainage = Drainage(
                dialog.result['name'],
                dialog.result['length'],
                dialog.result['pipe_diameter'],
                dialog.result['system_type']
            )
            self.current_project.add_child(drainage)
            self._update_displays()
    
    def _add_to_last_room_or_floor(self, component):
        """Helper to add component to last room or floor"""
        # If user selected a target in the UI, add there
        sel = getattr(self, 'selection_var', None)
        if sel and sel.get() and sel.get() != "Use last (default)":
            sel_display = sel.get()
            target = self.selection_map.get(sel_display)
            if target:
                try:
                    # If target is a Room/Floor/Building/Project, add directly
                    if isinstance(target, (Room, Floor, Building, Project)):
                        target.add_child(component)
                    else:
                        # generic fallback
                        target.add_child(component)
                    self._update_displays()
                    return
                except Exception:
                    # fall through to default behavior
                    pass

        # Default behavior: add to last building/floor/room as before
        if not self.current_project.children:
            messagebox.showerror("Error", "Please add a building first!")
            return

        building = self.current_project.children[-1]
        if not building.children:
            messagebox.showerror("Error", "Please add a floor first!")
            return

        floor = building.children[-1]
        room = None
        for child in reversed(floor.children):
            if isinstance(child, Room):
                room = child
                break

        if room is not None:
            room.add_child(component)
        else:
            floor.add_child(component)

        self._update_displays()

    def _build_selection_items(self, component: Component, path: str = ""):
        """Return list of (display, component) for selection menu."""
        items = []
        cur_path = f"{path}/{component.name}" if path else component.name
        display = f"{cur_path} ({component.__class__.__name__})"
        items.append((display, component))
        for child in component.children:
            items.extend(self._build_selection_items(child, cur_path))
        return items
    def _export_csv(self):
        """Export cost breakdown to CSV"""
        if not self.current_project:
            messagebox.showerror("Error", "No project to export!")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )

        if filename:
            try:
                breakdown = self.current_project.get_material_breakdown()
                with open(filename, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Material", "Quantity", "Total Cost"])

                    total_cost = self.current_project.calculate_cost()
                    for material, qty in sorted(breakdown.items()):
                        writer.writerow([material, f"{qty:.2f}", ""])

                    writer.writerow([])
                    writer.writerow(["Total Project Cost", "", f"${total_cost:,.2f}"])

                    messagebox.showinfo("Success", "Export completed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def run(self):
        """Start the application"""
        self.root.mainloop()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    app = ConstructionEstimatorApp()
    app.run()
