"""
Digital Twin Ecosystem State Models: Bins, Fleet Trucks, Facilities, and City Sectors.
Models the physical entities, IoT telemetry, coordinates, and operational constraints.
"""

import time
import random

CITY_SECTORS = {
    "SEC_1": {
        "id": "SEC_1",
        "name": "Downtown Commercial Hub",
        "type": "Commercial",
        "color": "#3B82F6",
        "center": {"x": 250, "y": 200},
        "fill_rate_mult": 1.4,
        "description": "High footfall, shopping plazas, high volume of beverage containers and coffee cups."
    },
    "SEC_2": {
        "id": "SEC_2",
        "name": "Oakwood Residential Suburb",
        "type": "Residential",
        "color": "#10B981",
        "center": {"x": 550, "y": 180},
        "fill_rate_mult": 1.0,
        "description": "Family neighborhoods, high organic food waste, mixed curbside paper and packaging."
    },
    "SEC_3": {
        "id": "SEC_3",
        "name": "CyberTech Innovation District",
        "type": "Tech & Office",
        "color": "#8B5CF6",
        "center": {"x": 220, "y": 420},
        "fill_rate_mult": 1.1,
        "description": "Corporate headquarters, university labs, high e-waste frequency and clean corrugated boxes."
    },
    "SEC_4": {
        "id": "SEC_4",
        "name": "Bayside Harbor & Fish Market",
        "type": "Waterfront",
        "color": "#06B6D4",
        "center": {"x": 620, "y": 420},
        "fill_rate_mult": 1.3,
        "description": "Tourist boardwalk, seafood markets, high moisture organic waste and beverage glass."
    },
    "SEC_5": {
        "id": "SEC_5",
        "name": "GreenValley Industrial Park",
        "type": "Industrial",
        "color": "#F59E0B",
        "center": {"x": 400, "y": 550},
        "fill_rate_mult": 1.2,
        "description": "Warehousing, manufacturing plants, heavy plastics, scrap metals, and hazardous solvents."
    }
}

FACILITIES = [
    {
        "id": "FAC_MRF",
        "name": "Apex Materials Recovery Facility (MRF)",
        "type": "MRF",
        "category": "Recyclables",
        "coords": {"x": 100, "y": 100},
        "capacity_tons_day": 350.0,
        "current_stored_tons": 182.4,
        "sorting_efficiency_pct": 94.2,
        "active_optical_sorters": 6,
        "color": "#3B82F6"
    },
    {
        "id": "FAC_COMPOST",
        "name": "BioCycle Anaerobic Digestion Plant",
        "type": "Composting & Biogas",
        "category": "Organics",
        "coords": {"x": 720, "y": 100},
        "capacity_tons_day": 200.0,
        "current_stored_tons": 115.8,
        "biogas_mwh_generated": 48.6,
        "fertilizer_tons_output": 72.3,
        "color": "#10B981"
    },
    {
        "id": "FAC_EWASTE",
        "name": "EcoVault Specialized E-Waste Depot",
        "type": "E-Waste & Hazmat",
        "category": "E-Waste / Hazmat",
        "coords": {"x": 100, "y": 560},
        "capacity_tons_day": 50.0,
        "current_stored_tons": 18.2,
        "lithium_cells_safely_isolated": 1420,
        "rare_earth_recovered_kg": 46.5,
        "color": "#8B5CF6"
    },
    {
        "id": "FAC_WTE",
        "name": "CleanThermal Waste-to-Energy (WtE)",
        "type": "Residual / WtE",
        "category": "Residual",
        "coords": {"x": 720, "y": 560},
        "capacity_tons_day": 280.0,
        "current_stored_tons": 194.0,
        "district_heat_mw": 32.4,
        "ash_recycling_pct": 89.0,
        "color": "#64748B"
    }
]

def generate_initial_bins():
    """Generates 24 smart IoT bins distributed across the 5 sectors."""
    bins = []
    bin_types = [
        {"type": "Recyclables", "color": "#3B82F6", "cap": 240},
        {"type": "Organics", "color": "#10B981", "cap": 180},
        {"type": "General / Landfill", "color": "#64748B", "cap": 240},
        {"type": "E-Waste", "color": "#8B5CF6", "cap": 120}
    ]
    
    bin_counter = 1
    for sec_id, sec in CITY_SECTORS.items():
        # Distribute 5 bins for SEC_1..4, 4 bins for SEC_5 = 24 bins
        count = 5 if sec_id in ["SEC_1", "SEC_2", "SEC_3", "SEC_4"] else 4
        cx = sec["center"]["x"]
        cy = sec["center"]["y"]
        
        for i in range(count):
            b_type = bin_types[i % len(bin_types)]
            # Sector specific preference
            if sec_id == "SEC_3" and i == 1:
                b_type = bin_types[3] # E-Waste
            elif sec_id == "SEC_2" and i == 0:
                b_type = bin_types[1] # Organics
            elif sec_id == "SEC_1" and i == 0:
                b_type = bin_types[0] # Recyclables
                
            angle = (i / count) * 6.28318
            radius = random.uniform(40, 85)
            bx = round(cx + radius * 0.9 * (1 if i % 2 == 0 else -1) * (0.8 + 0.4 * random.random()))
            by = round(cy + radius * 0.7 * (1 if i > 1 else -1) * (0.8 + 0.4 * random.random()))
            
            initial_fill = round(random.uniform(25.0, 78.0), 1)
            # Give one or two bins critical status initially for demonstration
            if bin_counter in [4, 12]:
                initial_fill = round(random.uniform(88.0, 96.0), 1)
                
            bins.append({
                "id": f"BIN-{bin_counter:02d}",
                "sector_id": sec_id,
                "sector_name": sec["name"],
                "waste_type": b_type["type"],
                "color": b_type["color"],
                "coords": {"x": max(40, min(760, bx)), "y": max(40, min(560, by))},
                "capacity_liters": b_type["cap"],
                "current_fill_pct": initial_fill,
                "fill_rate_lph": round(random.uniform(3.5, 9.2) * sec["fill_rate_mult"], 1), # liters per hour
                "battery_pct": round(random.uniform(82.0, 100.0), 1),
                "temperature_c": round(random.uniform(19.0, 24.5), 1),
                "contamination_pct": round(random.uniform(4.0, 28.0), 1),
                "tilt_degrees": round(random.uniform(0.1, 2.2), 1),
                "lid_open": False,
                "last_serviced_min_ago": random.randint(45, 320),
                "status": "CRITICAL" if initial_fill >= 85 else ("WARNING" if initial_fill >= 70 else "NORMAL")
            })
            bin_counter += 1
            
    return bins

def generate_initial_trucks():
    """Generates the 4 specialized municipal smart collection trucks."""
    return [
        {
            "id": "TRUCK-01",
            "name": "EcoHaul EV-Alpha",
            "type": "Electric Compactor",
            "service_category": "Recyclables",
            "coords": {"x": 120, "y": 140},
            "status": "IDLE", # IDLE, EN_ROUTE, COLLECTING, RETURNING_TO_FACILITY
            "capacity_tons": 8.0,
            "current_load_tons": 2.4,
            "load_pct": 30.0,
            "fuel_or_battery_pct": 91.0,
            "co2_saved_kg": 420.5,
            "target_bin_id": None,
            "route_queue": [],
            "path_history": [{"x": 100, "y": 100}, {"x": 120, "y": 140}],
            "color": "#3B82F6",
            "assigned_facility": "FAC_MRF"
        },
        {
            "id": "TRUCK-02",
            "name": "BioMover CNG-Bravo",
            "type": "Bio-CNG Heavy Truck",
            "service_category": "Organics",
            "coords": {"x": 680, "y": 130},
            "status": "IDLE",
            "capacity_tons": 10.0,
            "current_load_tons": 4.8,
            "load_pct": 48.0,
            "fuel_or_battery_pct": 84.0,
            "co2_saved_kg": 680.0,
            "target_bin_id": None,
            "route_queue": [],
            "path_history": [{"x": 720, "y": 100}, {"x": 680, "y": 130}],
            "color": "#10B981",
            "assigned_facility": "FAC_COMPOST"
        },
        {
            "id": "TRUCK-03",
            "name": "VoltRapid EV-Charlie",
            "type": "High-Agility Rapid EV",
            "service_category": "General / Landfill",
            "coords": {"x": 380, "y": 300},
            "status": "EN_ROUTE",
            "capacity_tons": 6.0,
            "current_load_tons": 5.1,
            "load_pct": 85.0,
            "fuel_or_battery_pct": 76.0,
            "co2_saved_kg": 310.2,
            "target_bin_id": "BIN-04",
            "route_queue": ["BIN-04", "BIN-12"],
            "path_history": [{"x": 720, "y": 560}, {"x": 500, "y": 420}, {"x": 380, "y": 300}],
            "color": "#F59E0B",
            "assigned_facility": "FAC_WTE"
        },
        {
            "id": "TRUCK-04",
            "name": "HazGuard Specialized",
            "type": "Hazmat & E-Waste Containment",
            "service_category": "E-Waste",
            "coords": {"x": 140, "y": 520},
            "status": "IDLE",
            "capacity_tons": 4.0,
            "current_load_tons": 0.8,
            "load_pct": 20.0,
            "fuel_or_battery_pct": 95.0,
            "co2_saved_kg": 890.4,
            "target_bin_id": None,
            "route_queue": [],
            "path_history": [{"x": 100, "y": 560}, {"x": 140, "y": 520}],
            "color": "#8B5CF6",
            "assigned_facility": "FAC_EWASTE"
        }
    ]

class WasteEcosystemTwin:
    """
    Main stateful container for the Digital Twin Ecosystem.
    Maintains all bins, fleet, processing centers, and city-wide telemetry.
    """
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.sectors = CITY_SECTORS
        self.facilities = [dict(f) for f in FACILITIES]
        self.bins = generate_initial_bins()
        self.trucks = generate_initial_trucks()
        
        self.sim_tick = 0
        self.sim_time_speed = 1.0 # 0.0 (paused), 1.0, 5.0, 15.0
        self.active_scenario = "Normal Operations"
        
        # Macro ecosystem KPIs
        self.total_waste_collected_tons = 124.6
        self.total_diverted_tons = 98.2
        self.total_landfill_avoided_tons = 98.2
        self.total_carbon_mitigated_tco2 = 142.8
        self.purity_index_pct = 91.4
        self.overflow_incidents_prevented = 46
        self.active_alerts = []
        self._check_alerts()
        
    def _check_alerts(self):
        alerts = []
        for b in self.bins:
            if b["current_fill_pct"] >= 90:
                alerts.append({
                    "id": f"ALT-{b['id']}-CRIT",
                    "level": "CRITICAL",
                    "title": f"Overflow Imminent: {b['id']}",
                    "message": f"{b['id']} ({b['waste_type']}) at {b['sector_name']} reached {b['current_fill_pct']}%. Immediate dispatch needed.",
                    "bin_id": b["id"],
                    "timestamp": time.strftime("%H:%M:%S")
                })
            elif b["contamination_pct"] >= 25.0:
                alerts.append({
                    "id": f"ALT-{b['id']}-CONTAM",
                    "level": "WARNING",
                    "title": f"High Contamination: {b['id']}",
                    "message": f"{b['id']} ({b['waste_type']}) has {b['contamination_pct']}% contamination index. Citizen nudge suggested.",
                    "bin_id": b["id"],
                    "timestamp": time.strftime("%H:%M:%S")
                })
        self.active_alerts = alerts[:6]

    def get_snapshot(self):
        """Returns JSON-serializable snapshot of digital twin state."""
        self._check_alerts()
        
        # Compute summary stats
        avg_fill = round(sum(b["current_fill_pct"] for b in self.bins) / len(self.bins), 1)
        critical_bins = [b for b in self.bins if b["current_fill_pct"] >= 85]
        warning_bins = [b for b in self.bins if 70 <= b["current_fill_pct"] < 85]
        diversion_rate = round((self.total_diverted_tons / max(1.0, self.total_waste_collected_tons)) * 100.0, 1)
        
        return {
            "sim_tick": self.sim_tick,
            "sim_speed": self.sim_time_speed,
            "active_scenario": self.active_scenario,
            "kpis": {
                "total_collected_tons": round(self.total_waste_collected_tons, 1),
                "total_diverted_tons": round(self.total_diverted_tons, 1),
                "diversion_rate_pct": diversion_rate,
                "carbon_mitigated_tco2": round(self.total_carbon_mitigated_tco2, 1),
                "purity_index_pct": self.purity_index_pct,
                "overflows_prevented": self.overflow_incidents_prevented,
                "avg_bin_fill_pct": avg_fill,
                "critical_bin_count": len(critical_bins),
                "warning_bin_count": len(warning_bins),
                "total_bin_count": len(self.bins),
                "active_truck_count": sum(1 for t in self.trucks if t["status"] != "IDLE")
            },
            "sectors": list(self.sectors.values()),
            "facilities": self.facilities,
            "bins": self.bins,
            "trucks": self.trucks,
            "alerts": self.active_alerts
        }

# Global digital twin instance
ecosystem_twin = WasteEcosystemTwin()
