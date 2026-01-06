from typing import List, Dict, Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from uuid import uuid4


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

class Foundation(Component):
    """Foundation with footings and slabs"""
    FOUNDATION_TYPES = {
        'shallow': {'depth': 1.5, 'cost_multiplier': 1.0, 'description': 'Shallow strip footing'},
        'deep': {'depth': 3.0, 'cost_multiplier': 1.8, 'description': 'Deep foundation'},
        'pile': {'depth': 6.0, 'cost_multiplier': 2.5, 'description': 'Pile foundation'},
        'raft': {'depth': 0.6, 'cost_multiplier': 1.3, 'description': 'Raft foundation'}
    }
    
    def __init__(self, name: str, foundation_type: str, 
                 area: float, soil_type: str = "medium", component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.foundation_type = foundation_type
        self.area = area
        self.soil_type = soil_type
        self._calculate_materials()
    
    def _calculate_materials(self):
        spec = self.FOUNDATION_TYPES.get(self.foundation_type, self.FOUNDATION_TYPES['shallow'])
        volume = self.area * spec['depth']
        multiplier = spec['cost_multiplier']
        
        # Soil factor adjustment
        soil_factors = {'soft': 1.3, 'medium': 1.0, 'hard': 0.8}
        soil_multiplier = soil_factors.get(self.soil_type, 1.0)
        
        self.materials = [
            Material(name="Concrete M25", unit="m³", 
                    quantity=volume * multiplier, unit_cost=120.0),
            Material(name="Steel Reinforcement", unit="kg", 
                    quantity=volume * 80 * multiplier, unit_cost=1.2),
            Material(name="Formwork", unit="m²", 
                    quantity=self.area * 2, unit_cost=15.0),
            Material(name="Excavation", unit="m³", 
                    quantity=volume * 1.3 * soil_multiplier, unit_cost=8.0),
            Material(name="Compaction", unit="m³", 
                    quantity=volume * 0.5, unit_cost=12.0),
            Material(name="Waterproofing", unit="m²", 
                    quantity=self.area, unit_cost=18.0),
            Material(name="Labor", unit="hours", 
                    quantity=volume * 15, unit_cost=18.0)
        ]
    
    def calculate_cost(self) -> float:
        return sum(m.total_cost() for m in self.materials)
    
    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        return breakdown
    
    def _get_properties(self) -> Dict:
        return {
            'foundation_type': self.foundation_type,
            'area': self.area,
            'soil_type': self.soil_type
        }

# ============================================================================
# ROOFING COMPONENTS
# ============================================================================

class Roof(Component):
    """Roof with trusses, covering, and waterproofing"""
    ROOF_TYPES = {
        'flat': {'pitch': 0, 'material_factor': 1.0, 'description': 'Flat concrete roof'},
        'gable': {'pitch': 30, 'material_factor': 1.15, 'description': 'Gable roof'},
        'hip': {'pitch': 35, 'material_factor': 1.25, 'description': 'Hip roof'},
        'shed': {'pitch': 20, 'material_factor': 1.08, 'description': 'Shed roof'}
    }
    
    COVERING_TYPES = {
        'tiles': {'cost': 25.0, 'weight': 50, 'lifespan': 50},
        'metal': {'cost': 35.0, 'weight': 8, 'lifespan': 40},
        'shingles': {'cost': 18.0, 'weight': 12, 'lifespan': 25},
        'concrete': {'cost': 110.0, 'weight': 2400, 'lifespan': 100}
    }
    
    def __init__(self, name: str, roof_type: str, covering_type: str,
                 area: float, component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.roof_type = roof_type
        self.covering_type = covering_type
        self.area = area
        self._calculate_materials()
    
    def _calculate_materials(self):
        roof_spec = self.ROOF_TYPES.get(self.roof_type, self.ROOF_TYPES['flat'])
        covering_spec = self.COVERING_TYPES.get(self.covering_type, self.COVERING_TYPES['tiles'])
        
        adjusted_area = self.area * roof_spec['material_factor']
        
        self.materials = [
            Material(name=f"{self.covering_type.title()} Covering", unit="m²", 
                    quantity=adjusted_area, unit_cost=covering_spec['cost']),
            Material(name="Wooden Trusses", unit="linear_m", 
                    quantity=adjusted_area * 0.5, unit_cost=35.0),
            Material(name="Waterproofing Membrane", unit="m²", 
                    quantity=adjusted_area * 1.1, unit_cost=12.0),
            Material(name="Insulation", unit="m²", 
                    quantity=adjusted_area, unit_cost=18.0),
            Material(name="Gutters & Downspouts", unit="linear_m", 
                    quantity=adjusted_area ** 0.5 * 4, unit_cost=22.0),
            Material(name="Ridge Caps", unit="linear_m", 
                    quantity=adjusted_area ** 0.5, unit_cost=15.0),
            Material(name="Carpentry Labor", unit="hours", 
                    quantity=adjusted_area * 2, unit_cost=20.0)
        ]
    
    def calculate_cost(self) -> float:
        return sum(m.total_cost() for m in self.materials)
    
    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        return breakdown
    
    def _get_properties(self) -> Dict:
        return {
            'roof_type': self.roof_type,
            'covering_type': self.covering_type,
            'area': self.area
        }

# ============================================================================
# DOORS AND WINDOWS
# ============================================================================

class Door(Component):
    """Door with frame and hardware"""
    DOOR_TYPES = {
        'standard': {'width': 0.9, 'height': 2.1, 'cost': 150, 'description': 'Standard interior door'},
        'double': {'width': 1.8, 'height': 2.1, 'cost': 280, 'description': 'Double door'},
        'main': {'width': 1.2, 'height': 2.4, 'cost': 450, 'description': 'Main entrance door'},
        'security': {'width': 1.0, 'height': 2.1, 'cost': 650, 'description': 'Security steel door'},
        'sliding': {'width': 2.4, 'height': 2.1, 'cost': 580, 'description': 'Sliding door'}
    }
    
    def __init__(self, name: str, door_type: str, 
                 quantity: int = 1, material: str = "wood", component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.door_type = door_type
        self.quantity = quantity
        self.material = material
        self._calculate_materials()
    
    def _calculate_materials(self):
        spec = self.DOOR_TYPES.get(self.door_type, self.DOOR_TYPES['standard'])
        
        # Material multiplier
        material_multipliers = {'wood': 1.0, 'steel': 1.4, 'aluminum': 1.6, 'upvc': 1.3}
        multiplier = material_multipliers.get(self.material, 1.0)
        
        self.materials = [
            Material(name=f"{self.material.title()} {self.door_type.title()} Door", 
                    unit="units", quantity=self.quantity, 
                    unit_cost=spec['cost'] * multiplier),
            Material(name="Door Frame", unit="units", 
                    quantity=self.quantity, unit_cost=80.0),
            Material(name="Door Hardware (Handles, Locks)", unit="sets", 
                    quantity=self.quantity, unit_cost=45.0),
            Material(name="Installation Labor", unit="hours", 
                    quantity=self.quantity * 3, unit_cost=18.0)
        ]
    
    def calculate_cost(self) -> float:
        return sum(m.total_cost() for m in self.materials)
    
    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        return breakdown
    
    def _get_properties(self) -> Dict:
        return {
            'door_type': self.door_type,
            'quantity': self.quantity,
            'material': self.material
        }

class Window(Component):
    """Window with frame and glass"""
    WINDOW_TYPES = {
        'single': {'width': 1.2, 'height': 1.5, 'cost': 180, 'description': 'Single casement'},
        'double': {'width': 2.4, 'height': 1.5, 'cost': 320, 'description': 'Double casement'},
        'bay': {'width': 3.0, 'height': 1.8, 'cost': 650, 'description': 'Bay window'},
        'sliding': {'width': 2.0, 'height': 1.5, 'cost': 280, 'description': 'Sliding window'},
        'fixed': {'width': 1.5, 'height': 1.5, 'cost': 150, 'description': 'Fixed window'}
    }
    
    def __init__(self, name: str, window_type: str, 
                 quantity: int = 1, glass_type: str = "single", component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.window_type = window_type
        self.quantity = quantity
        self.glass_type = glass_type  # single, double, triple
        self._calculate_materials()
    
    def _calculate_materials(self):
        spec = self.WINDOW_TYPES.get(self.window_type, self.WINDOW_TYPES['single'])
        area = spec['width'] * spec['height'] * self.quantity
        
        # Glass multiplier
        glass_multipliers = {'single': 1.0, 'double': 1.8, 'triple': 2.5, 'tempered': 2.0}
        glass_multiplier = glass_multipliers.get(self.glass_type, 1.0)
        
        self.materials = [
            Material(name=f"{self.window_type.title()} Window Frame", 
                    unit="units", quantity=self.quantity, unit_cost=spec['cost'] * 0.4),
            Material(name=f"{self.glass_type.title()} Glass Panes", 
                    unit="m²", quantity=area, unit_cost=55.0 * glass_multiplier),
            Material(name="Window Hardware", unit="sets", 
                    quantity=self.quantity, unit_cost=35.0),
            Material(name="Sealant & Weatherstripping", unit="meters", 
                    quantity=self.quantity * 5, unit_cost=4.0),
            Material(name="Installation Labor", unit="hours", 
                    quantity=self.quantity * 2.5, unit_cost=18.0)
        ]
    
    def calculate_cost(self) -> float:
        return sum(m.total_cost() for m in self.materials)
    
    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        return breakdown
    
    def _get_properties(self) -> Dict:
        return {
            'window_type': self.window_type,
            'quantity': self.quantity,
            'glass_type': self.glass_type
        }

# ============================================================================
# MEP SYSTEMS
# ============================================================================

class ElectricalSystem(Component):
    """Complete electrical system"""
    
    def __init__(self, name: str, area: float, 
                 points: int = 10, load_kw: float = 5.0, component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.area = area
        self.points = points  # outlets + switches
        self.load_kw = load_kw
        self._calculate_materials()
    
    def _calculate_materials(self):
        cable_length = self.area * 3  # 3m cable per m² floor area
        conduit_length = cable_length * 0.8
        
        self.materials = [
            Material(name="Electrical Cable (2.5mm²)", unit="meters", 
                    quantity=cable_length * 0.7, unit_cost=2.5),
            Material(name="Electrical Cable (4mm²)", unit="meters", 
                    quantity=cable_length * 0.3, unit_cost=3.8),
            Material(name="Outlets & Switches", unit="units", 
                    quantity=self.points, unit_cost=8.0),
            Material(name="Circuit Breakers", unit="units", 
                    quantity=max(2, self.points // 5), unit_cost=25.0),
            Material(name="Distribution Box", unit="units", 
                    quantity=1, unit_cost=120.0),
            Material(name="Conduit Pipes (PVC)", unit="meters", 
                    quantity=conduit_length, unit_cost=3.5),
            Material(name="Junction Boxes", unit="units", 
                    quantity=int(self.points / 3), unit_cost=12.0),
            Material(name="Light Fixtures", unit="units", 
                    quantity=int(self.area / 10), unit_cost=45.0),
            Material(name="Electrician Labor", unit="hours", 
                    quantity=self.points * 2 + self.area * 0.5, unit_cost=25.0)
        ]
    
    def calculate_cost(self) -> float:
        return sum(m.total_cost() for m in self.materials)
    
    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        return breakdown
    
    def _get_properties(self) -> Dict:
        return {'area': self.area, 'points': self.points, 'load_kw': self.load_kw}

class PlumbingSystem(Component):
    """Complete plumbing system"""
    
    def __init__(self, name: str, fixtures: int = 5, 
                 pipe_length: float = 50, hot_water: bool = True, 
                 component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.fixtures = fixtures
        self.pipe_length = pipe_length
        self.hot_water = hot_water
        self._calculate_materials()
    
    def _calculate_materials(self):
        self.materials = [
            Material(name="PVC Pipes (Cold Water)", unit="meters", 
                    quantity=self.pipe_length, unit_cost=4.5),
            Material(name="CPVC/Copper Pipes (Hot Water)", unit="meters", 
                    quantity=self.pipe_length * 0.4 if self.hot_water else 0, 
                    unit_cost=12.0),
            Material(name="Drainage Pipes", unit="meters", 
                    quantity=self.pipe_length * 0.8, unit_cost=6.5),
            Material(name="Plumbing Fixtures", unit="units", 
                    quantity=self.fixtures, unit_cost=180.0),
            Material(name="Fittings & Valves", unit="sets", 
                    quantity=self.fixtures * 2, unit_cost=15.0),
            Material(name="Water Heater", unit="units", 
                    quantity=1 if self.hot_water else 0, unit_cost=450.0),
            Material(name="Water Tank", unit="units", 
                    quantity=1, unit_cost=350.0),
            Material(name="Plumber Labor", unit="hours", 
                    quantity=self.pipe_length * 0.5 + self.fixtures * 3, 
                    unit_cost=22.0)
        ]
    
    def calculate_cost(self) -> float:
        return sum(m.total_cost() for m in self.materials)
    
    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        return breakdown
    
    def _get_properties(self) -> Dict:
        return {
            'fixtures': self.fixtures,
            'pipe_length': self.pipe_length,
            'hot_water': self.hot_water
        }

class HVACSystem(Component):
    """Heating, Ventilation, Air Conditioning"""
    
    def __init__(self, name: str, area: float, 
                 system_type: str = "split", component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.area = area
        self.system_type = system_type  # split, central, ductless
        self._calculate_materials()
    
    def _calculate_materials(self):
        # Calculate tonnage (1 ton per 100-120 sq ft)
        tonnage = self.area / 10  # Simplified for metric
        
        system_costs = {
            'split': 600 * tonnage,
            'central': 900 * tonnage,
            'ductless': 700 * tonnage,
            'vrf': 1200 * tonnage
        }
        
        base_cost = system_costs.get(self.system_type, 600 * tonnage)
        
        self.materials = [
            Material(name=f"{self.system_type.title()} AC Unit", unit="units", 
                    quantity=max(1, int(tonnage / 2)), unit_cost=base_cost),
            Material(name="Refrigerant Piping", unit="meters", 
                    quantity=self.area * 0.3, unit_cost=15.0),
            Material(name="Air Ducts", unit="meters", 
                    quantity=self.area * 0.4 if self.system_type == 'central' else 0, 
                    unit_cost=22.0),
            Material(name="Insulation", unit="m²", 
                    quantity=self.area * 0.2, unit_cost=12.0),
            Material(name="Thermostat Controls", unit="units", 
                    quantity=max(1, int(self.area / 100)), unit_cost=85.0),
            Material(name="HVAC Installation Labor", unit="hours", 
                    quantity=tonnage * 8, unit_cost=30.0)
        ]
    
    def calculate_cost(self) -> float:
        return sum(m.total_cost() for m in self.materials)
    
    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        return breakdown
    
    def _get_properties(self) -> Dict:
        return {'area': self.area, 'system_type': self.system_type}

# ============================================================================
# FINISHING COMPONENTS
# ============================================================================

class Painting(Component):
    """Interior/exterior painting"""
    
    def __init__(self, name: str, area: float, 
                 paint_type: str = "interior", quality: str = "standard", 
                 component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.area = area
        self.paint_type = paint_type
        self.quality = quality
        self._calculate_materials()
    
    def _calculate_materials(self):
        # 1 liter covers ~10m² with 2 coats
        paint_liters = (self.area / 10) * 2
        
        type_multiplier = 1.5 if self.paint_type == "exterior" else 1.0
        quality_multipliers = {'economy': 0.7, 'standard': 1.0, 'premium': 1.8}
        quality_multiplier = quality_multipliers.get(self.quality, 1.0)
        
        self.materials = [
            Material(name=f"{self.quality.title()} {self.paint_type.title()} Paint", 
                    unit="liters", quantity=paint_liters, 
                    unit_cost=15.0 * type_multiplier * quality_multiplier),
            Material(name="Primer", unit="liters", 
                    quantity=paint_liters * 0.8, unit_cost=12.0),
            Material(name="Putty & Filler", unit="kg", 
                    quantity=self.area * 0.2, unit_cost=3.0),
            Material(name="Sandpaper & Supplies", unit="sets", 
                    quantity=int(self.area / 50) + 1, unit_cost=15.0),
            Material(name="Painter Labor", unit="hours", 
                    quantity=self.area * 0.3, unit_cost=15.0)
        ]
    
    def calculate_cost(self) -> float:
        return sum(m.total_cost() for m in self.materials)
    
    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        return breakdown
    
    def _get_properties(self) -> Dict:
        return {'area': self.area, 'paint_type': self.paint_type, 'quality': self.quality}

class Plastering(Component):
    """Wall plastering"""
    
    def __init__(self, name: str, area: float, 
                 thickness: float = 0.015, plaster_type: str = "cement", 
                 component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.area = area
        self.thickness = thickness
        self.plaster_type = plaster_type
        self._calculate_materials()
    
    def _calculate_materials(self):
        volume = self.area * self.thickness
        
        plaster_specs = {
            'cement': {'cement_bags': 15, 'sand_m3': 1.2, 'cost': 1.0},
            'gypsum': {'cement_bags': 0, 'sand_m3': 0, 'cost': 1.4},
            'lime': {'cement_bags': 8, 'sand_m3': 1.5, 'cost': 0.9}
        }
        
        spec = plaster_specs.get(self.plaster_type, plaster_specs['cement'])
        
        materials_list = []
        
        if spec['cement_bags'] > 0:
            materials_list.append(
                Material(name=f"{self.plaster_type.title()} Plaster Cement", 
                        unit="bags", quantity=volume * spec['cement_bags'], 
                        unit_cost=7.5 * spec['cost'])
            )
        
        if spec['sand_m3'] > 0:
            materials_list.append(
                Material(name="Plaster Sand", unit="m³", 
                        quantity=volume * spec['sand_m3'], unit_cost=22.0)
            )
        
        if self.plaster_type == 'gypsum':
            materials_list.append(
                Material(name="Gypsum Plaster", unit="kg", 
                        quantity=self.area * 8, unit_cost=0.8)
            )
        
        materials_list.extend([
            Material(name="Plaster Mesh/Wire", unit="m²", 
                    quantity=self.area * 0.1, unit_cost=4.0),
            Material(name="Mason Labor", unit="hours", 
                    quantity=self.area * 0.5, unit_cost=16.0)
        ])
        
        self.materials = materials_list
    
    def calculate_cost(self) -> float:
        return sum(m.total_cost() for m in self.materials)
    
    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        return breakdown
    
    def _get_properties(self) -> Dict:
        return {
            'area': self.area,
            'thickness': self.thickness,
            'plaster_type': self.plaster_type
        }

class Flooring(Component):
    """Floor finishing"""
    
    FLOORING_TYPES = {
        'ceramic': {'cost': 20.0, 'description': 'Ceramic tiles'},
        'porcelain': {'cost': 35.0, 'description': 'Porcelain tiles'},
        'marble': {'cost': 85.0, 'description': 'Marble flooring'},
        'granite': {'cost': 95.0, 'description': 'Granite flooring'},
        'hardwood': {'cost': 65.0, 'description': 'Hardwood flooring'},
        'laminate': {'cost': 25.0, 'description': 'Laminate flooring'},
        'vinyl': {'cost': 18.0, 'description': 'Vinyl flooring'},
        'carpet': {'cost': 22.0, 'description': 'Carpet'}
    }
    
    def __init__(self, name: str, area: float, 
                 flooring_type: str = "ceramic", component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.area = area
        self.flooring_type = flooring_type
        self._calculate_materials()
    
    def _calculate_materials(self):
        spec = self.FLOORING_TYPES.get(self.flooring_type, self.FLOORING_TYPES['ceramic'])
        
        # Add 10% for wastage
        material_area = self.area * 1.1
        
        self.materials = [
            Material(name=spec['description'], unit="m²", 
                    quantity=material_area, unit_cost=spec['cost']),
            Material(name="Adhesive/Mortar", unit="bags", 
                    quantity=self.area * 0.5, unit_cost=12.0),
            Material(name="Grout", unit="kg", 
                    quantity=self.area * 0.3, unit_cost=3.5),
            Material(name="Skirting/Baseboards", unit="linear_m", 
                    quantity=self.area ** 0.5 * 4, unit_cost=8.0),
            Material(name="Installation Labor", unit="hours", 
                    quantity=self.area * 0.8, unit_cost=18.0)
        ]
    
    def calculate_cost(self) -> float:
        return sum(m.total_cost() for m in self.materials)
    
    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        return breakdown
    
    def _get_properties(self) -> Dict:
        return {'area': self.area, 'flooring_type': self.flooring_type}

# ============================================================================
# STRUCTURAL COMPONENTS
# ============================================================================

class Staircase(Component):
    """Staircase between floors"""
    
    def __init__(self, name: str, floor_height: float, 
                 width: float = 1.2, material: str = "concrete", 
                 component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.floor_height = floor_height
        self.width = width
        self.material = material
        self._calculate_materials()
    
    def _calculate_materials(self):
        # Standard stair dimensions: 17cm riser, 28cm tread
        steps = max(1, int(self.floor_height / 0.17))
        total_length = steps * 0.28
        
        if self.material == "concrete":
            volume = total_length * self.width * 0.15
            
            self.materials = [
                Material(name="Concrete M20", unit="m³", 
                        quantity=volume, unit_cost=110.0),
                Material(name="Steel Reinforcement", unit="kg", 
                        quantity=volume * 100, unit_cost=1.2),
                Material(name="Formwork", unit="m²", 
                        quantity=total_length * self.width * 2.5, unit_cost=18.0),
                Material(name="Stair Railing (Steel)", unit="meters", 
                        quantity=total_length, unit_cost=85.0),
                Material(name="Tiles/Nosing", unit="m²", 
                        quantity=steps * self.width * 0.35, unit_cost=22.0),
                Material(name="Mason Labor", unit="hours", 
                        quantity=volume * 30, unit_cost=18.0)
            ]
        else:  # wooden stairs
            self.materials = [
                Material(name="Wooden Treads", unit="units", 
                        quantity=steps, unit_cost=45.0),
                Material(name="Wooden Risers", unit="units", 
                        quantity=steps, unit_cost=25.0),
                Material(name="Stringers", unit="units", 
                        quantity=3, unit_cost=120.0),
                Material(name="Wooden Railing", unit="meters", 
                        quantity=total_length, unit_cost=65.0),
                Material(name="Hardware & Fasteners", unit="sets", 
                        quantity=1, unit_cost=85.0),
                Material(name="Carpentry Labor", unit="hours", 
                        quantity=steps * 2, unit_cost=22.0)
            ]
    
    def calculate_cost(self) -> float:
        return sum(m.total_cost() for m in self.materials)
    
    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        return breakdown
    
    def _get_properties(self) -> Dict:
        return {
            'floor_height': self.floor_height,
            'width': self.width,
            'material': self.material
        }

# ============================================================================
# SITE INFRASTRUCTURE
# ============================================================================

class Road(Component):
    """Road with multiple layers"""
    
    def __init__(self, name: str, length: float, width: float,
                 road_type: str = "asphalt", traffic_level: str = "medium",
                 component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.length = length
        self.width = width
        self.road_type = road_type
        self.traffic_level = traffic_level
        self._calculate_materials()
    
    def _calculate_materials(self):
        area = self.length * self.width
        
        # Traffic level affects layer thickness
        thickness_factors = {'light': 0.8, 'medium': 1.0, 'heavy': 1.3}
        factor = thickness_factors.get(self.traffic_level, 1.0)
        
        # Layer volumes
        asphalt_volume = area * 0.05 * factor      # 5cm asphalt
        base_volume = area * 0.20 * factor         # 20cm base
        subbase_volume = area * 0.30 * factor      # 30cm subbase
        
        self.materials = [
            Material(name="Asphalt/Bitumen", unit="tons", 
                    quantity=asphalt_volume * 2.4, unit_cost=85.0),
            Material(name="Crushed Stone Base", unit="m³", 
                    quantity=base_volume, unit_cost=35.0),
            Material(name="Gravel Subbase", unit="m³", 
                    quantity=subbase_volume, unit_cost=25.0),
            Material(name="Geotextile Fabric", unit="m²", 
                    quantity=area, unit_cost=3.5),
            Material(name="Road Marking Paint", unit="liters", 
                    quantity=self.length * 0.15, unit_cost=45.0),
            Material(name="Edge Curbs", unit="linear_m", 
                    quantity=self.length * 2, unit_cost=22.0),
            Material(name="Compaction & Paving Labor", unit="hours", 
                    quantity=area * 0.4, unit_cost=30.0)
        ]
    
    def calculate_cost(self) -> float:
        return sum(m.total_cost() for m in self.materials)
    
    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        return breakdown
    
    def _get_properties(self) -> Dict:
        return {
            'length': self.length,
            'width': self.width,
            'road_type': self.road_type,
            'traffic_level': self.traffic_level
        }

class Drainage(Component):
    """Drainage system with pipes and manholes"""
    
    def __init__(self, name: str, length: float, 
                 pipe_diameter: float = 0.3, system_type: str = "surface",
                 component_id: Optional[str] = None):
        super().__init__(name, component_id)
        self.length = length
        self.pipe_diameter = pipe_diameter
        self.system_type = system_type
        self._calculate_materials()
    
    def _calculate_materials(self):
        # Excavation volume
        trench_depth = 1.2 if self.system_type == "surface" else 2.0
        trench_volume = self.length * 0.6 * trench_depth
        
        # Manholes every 30-40m
        manhole_count = max(2, int(self.length / 35))
        
        self.materials = [
            Material(name=f"Drainage Pipes (Ø{int(self.pipe_diameter*1000)}mm)", 
                    unit="meters", quantity=self.length, unit_cost=25.0),
            Material(name="Gravel Bedding", unit="m³", 
                    quantity=trench_volume * 0.25, unit_cost=22.0),
            Material(name="Concrete Manholes", unit="units", 
                    quantity=manhole_count, unit_cost=350.0),
            Material(name="Manhole Covers", unit="units", 
                    quantity=manhole_count, unit_cost=120.0),
            Material(name="Catch Basins", unit="units", 
                    quantity=int(self.length / 50), unit_cost=280.0),
            Material(name="Excavation", unit="m³", 
                    quantity=trench_volume, unit_cost=10.0),
            Material(name="Backfill Material", unit="m³", 
                    quantity=trench_volume * 0.6, unit_cost=15.0),
            Material(name="Labor", unit="hours", 
                    quantity=self.length * 1.2, unit_cost=18.0)
        ]
    
    def calculate_cost(self) -> float:
        return sum(m.total_cost() for m in self.materials)
    
    def get_material_breakdown(self) -> Dict[str, float]:
        breakdown = {}
        for material in self.materials:
            key = f"{material.name} ({material.unit})"
            breakdown[key] = breakdown.get(key, 0) + material.quantity
        return breakdown
    
    def _get_properties(self) -> Dict:
        return {
            'length': self.length,
            'pipe_diameter': self.pipe_diameter,
            'system_type': self.system_type
        }


# Component deserialization helpers
_COMPONENT_REGISTRY = {
    'Wall': Wall,
    'Room': Room,
    'Floor': Floor,
    'Building': Building,
    'Project': Project,
    'Foundation': Foundation,
    'Roof': Roof,
    'Door': Door,
    'Window': Window,
    'ElectricalSystem': ElectricalSystem,
    'PlumbingSystem': PlumbingSystem,
    'HVACSystem': HVACSystem,
    'Painting': Painting,
    'Plastering': Plastering,
    'Flooring': Flooring,
    'Staircase': Staircase,
    'Road': Road,
    'Drainage': Drainage
}


def component_from_dict(data: Dict) -> Component:
    """Reconstruct a Component (and its children) from a dict produced by `to_dict()`.

    This deliberately bypasses __init__ and restores attributes so deserialization
    recreates the original state without triggering default material calculations.
    """
    if data is None:
        return None

    type_name = data.get('type')
    cls = _COMPONENT_REGISTRY.get(type_name)

    # Fallback to generic Component if unknown type
    if cls is None:
        inst = object.__new__(Component)
    else:
        inst = object.__new__(cls)

    # Basic attributes
    inst.id = data.get('id')
    inst.name = data.get('name', '')

    # Restore properties onto the instance
    properties = data.get('properties', {}) or {}
    for k, v in properties.items():
        setattr(inst, k, v)

    # Restore materials
    inst.materials = [Material.from_dict(m) for m in data.get('materials', [])]

    # Recursively restore children
    inst.children = [component_from_dict(c) for c in data.get('children', [])]

    return inst


@classmethod
def project_from_dict(cls, data: Dict) -> 'Project':
    inst = component_from_dict(data)
    if not isinstance(inst, Project):
        raise ValueError('Data does not represent a Project')
    return inst

# Attach as a classmethod to Project for convenience
Project.from_dict = project_from_dict