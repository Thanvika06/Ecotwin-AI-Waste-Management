"""
Simulation Engine for the Digital Twin Ecosystem.
Simulates time dilation, dynamic waste generation rates, vehicle movement vector math,
bin collection, offloading at facilities, and scenario perturbations.
"""

import math
import random
from digital_twin.ecosystem import ecosystem_twin

class SimulationEngine:
    def __init__(self, twin=None):
        self.twin = twin or ecosystem_twin
        
    def set_speed(self, speed_multiplier):
        """Set simulation speed: 0.0 (pause), 1.0, 5.0, 15.0."""
        self.twin.sim_time_speed = float(speed_multiplier)
        return self.twin.sim_time_speed

    def inject_scenario(self, scenario_name):
        """Inject real-world operational scenarios."""
        self.twin.active_scenario = scenario_name
        
        if scenario_name == "Morning Rush Hour":
            # Commercial and Residential fill rates jump
            for b in self.twin.bins:
                if b["sector_id"] in ["SEC_1", "SEC_2"]:
                    b["current_fill_pct"] = min(99.0, b["current_fill_pct"] + random.uniform(15.0, 30.0))
                    b["fill_rate_lph"] *= 1.8
        elif scenario_name == "Festival Surge (Bayside)":
            for b in self.twin.bins:
                if b["sector_id"] == "SEC_4":
                    b["current_fill_pct"] = min(99.0, b["current_fill_pct"] + random.uniform(35.0, 55.0))
        elif scenario_name == "Heavy Rain Contamination Event":
            # Paper bins get damp and contaminated
            for b in self.twin.bins:
                if "Recyclable" in b["waste_type"]:
                    b["contamination_pct"] = min(65.0, b["contamination_pct"] + random.uniform(20.0, 35.0))
        elif scenario_name == "Reset to Normal":
            self.twin.reset()
            return self.twin.get_snapshot()
            
        return self.twin.get_snapshot()

    def step(self, delta_seconds=15):
        """
        Advance the simulation state by delta_seconds * speed_multiplier.
        """
        if self.twin.sim_time_speed <= 0.0:
            return self.twin.get_snapshot()
            
        effective_delta = delta_seconds * self.twin.sim_time_speed
        self.twin.sim_tick += 1
        
        # 1. Advance Bin fill rates
        self._step_bins(effective_delta)
        
        # 2. Advance Fleet Trucks (Movement & Collection)
        self._step_trucks(effective_delta)
        
        # 3. Check for automatic dynamic dispatch of idle trucks if critical bins exist
        self._check_auto_dispatch()
        
        return self.twin.get_snapshot()

    def _step_bins(self, delta_sec):
        """Increment bin fills based on fill rate in liters/hour."""
        hours = delta_sec / 3600.0
        for b in self.twin.bins:
            added_liters = b["fill_rate_lph"] * hours * random.uniform(0.9, 1.2)
            added_pct = (added_liters / max(1.0, b["capacity_liters"])) * 100.0
            
            b["current_fill_pct"] = min(100.0, round(b["current_fill_pct"] + added_pct, 1))
            
            # Subtle temperature & battery drift
            b["battery_pct"] = max(10.0, round(b["battery_pct"] - 0.001 * hours, 2))
            
            # Update status
            if b["current_fill_pct"] >= 85.0:
                b["status"] = "CRITICAL"
            elif b["current_fill_pct"] >= 70.0:
                b["status"] = "WARNING"
            else:
                b["status"] = "NORMAL"

    def _step_trucks(self, delta_sec):
        """Move trucks towards target coordinates and perform collections/offloads."""
        # Truck speed in pixels per second
        speed_pps = 18.0 * (self.twin.sim_time_speed)
        
        for truck in self.twin.trucks:
            if truck["status"] == "IDLE":
                continue
                
            # If returning to facility
            if truck["status"] == "RETURNING_TO_FACILITY":
                fac = next((f for f in self.twin.facilities if f["id"] == truck["assigned_facility"]), None)
                if not fac:
                    continue
                target_x, target_y = fac["coords"]["x"], fac["coords"]["y"]
                reached = self._move_towards(truck, target_x, target_y, speed_pps)
                if reached:
                    self._offload_truck_at_facility(truck, fac)
                continue
                
            # If truck has an active target bin
            target_bin_id = truck["target_bin_id"]
            if not target_bin_id and truck["route_queue"]:
                truck["target_bin_id"] = truck["route_queue"].pop(0)
                target_bin_id = truck["target_bin_id"]
                
            if not target_bin_id:
                # No more bins in queue, check load
                if truck["load_pct"] > 30.0:
                    truck["status"] = "RETURNING_TO_FACILITY"
                else:
                    truck["status"] = "IDLE"
                continue
                
            target_bin = next((b for b in self.twin.bins if b["id"] == target_bin_id), None)
            if not target_bin:
                truck["target_bin_id"] = None
                continue
                
            target_x, target_y = target_bin["coords"]["x"], target_bin["coords"]["y"]
            reached = self._move_towards(truck, target_x, target_y, speed_pps)
            
            if reached:
                # Collect waste from bin
                self._collect_bin(truck, target_bin)
                # Next bin or return to facility if full
                if truck["load_pct"] >= 85.0:
                    truck["status"] = "RETURNING_TO_FACILITY"
                    truck["target_bin_id"] = None
                elif truck["route_queue"]:
                    truck["target_bin_id"] = truck["route_queue"].pop(0)
                    truck["status"] = "EN_ROUTE"
                else:
                    truck["status"] = "RETURNING_TO_FACILITY"
                    truck["target_bin_id"] = None

    def _move_towards(self, truck, target_x, target_y, max_dist):
        """Vector interpolation towards target."""
        cx, cy = truck["coords"]["x"], truck["coords"]["y"]
        dx = target_x - cx
        dy = target_y - cy
        dist = math.hypot(dx, dy)
        
        if dist <= max_dist or dist < 2.0:
            truck["coords"]["x"] = target_x
            truck["coords"]["y"] = target_y
            truck["path_history"].append({"x": target_x, "y": target_y})
            if len(truck["path_history"]) > 20:
                truck["path_history"].pop(0)
            return True
            
        ratio = max_dist / dist
        new_x = round(cx + dx * ratio, 1)
        new_y = round(cy + dy * ratio, 1)
        truck["coords"]["x"] = new_x
        truck["coords"]["y"] = new_y
        
        # Decrement battery / fuel slightly
        truck["fuel_or_battery_pct"] = max(5.0, round(truck["fuel_or_battery_pct"] - 0.02, 2))
        return False

    def _collect_bin(self, truck, bin_obj):
        """Simulate physical emptying of a smart bin into compactor truck."""
        collected_pct = bin_obj["current_fill_pct"]
        collected_liters = (collected_pct / 100.0) * bin_obj["capacity_liters"]
        # Approximate density ~ 0.12 kg/L for mixed municipal waste
        collected_tons = round((collected_liters * 0.12) / 1000.0, 3)
        
        truck["current_load_tons"] = round(min(truck["capacity_tons"], truck["current_load_tons"] + collected_tons), 2)
        truck["load_pct"] = round((truck["current_load_tons"] / truck["capacity_tons"]) * 100.0, 1)
        
        # Reset bin
        bin_obj["current_fill_pct"] = 0.0
        bin_obj["status"] = "NORMAL"
        bin_obj["last_serviced_min_ago"] = 0
        self.twin.overflow_incidents_prevented += 1

    def _offload_truck_at_facility(self, truck, facility):
        """Offload collected waste at processing facility."""
        offloaded_tons = truck["current_load_tons"]
        truck["current_load_tons"] = 0.0
        truck["load_pct"] = 0.0
        truck["status"] = "IDLE"
        
        # Update macro stats
        self.twin.total_waste_collected_tons += offloaded_tons
        if facility["type"] != "Residual / WtE":
            self.twin.total_diverted_tons += offloaded_tons
            self.twin.total_carbon_mitigated_tco2 += offloaded_tons * 1.25
        else:
            self.twin.total_diverted_tons += offloaded_tons * 0.35 # Residual recovery
            self.twin.total_carbon_mitigated_tco2 += offloaded_tons * 0.40
            
        facility["current_stored_tons"] = round(facility["current_stored_tons"] + offloaded_tons, 1)

    def dispatch_truck_to_route(self, truck_id, bin_ids=None):
        """
        Dispatches a specific truck along an optimized route of critical bins.
        Uses Nearest-Neighbor CVRP optimization.
        """
        truck = next((t for t in self.twin.trucks if t["id"] == truck_id), None)
        if not truck:
            return {"success": False, "error": f"Truck {truck_id} not found"}
            
        if not bin_ids:
            # Auto-find critical or warning bins matching truck's specialty
            category = truck["service_category"]
            candidates = [
                b for b in self.twin.bins 
                if b["current_fill_pct"] >= 65.0 and (category in b["waste_type"] or category == "General / Landfill")
            ]
            if not candidates:
                # Fallback to any high bin
                candidates = [b for b in self.twin.bins if b["current_fill_pct"] >= 70.0]
                
            if not candidates:
                return {"success": False, "message": "No critical bins requiring collection currently."}
                
            # Nearest neighbor ordering starting from truck's current position
            ordered_route = []
            curr_x, curr_y = truck["coords"]["x"], truck["coords"]["y"]
            unvisited = list(candidates)
            
            while unvisited and len(ordered_route) < 4:
                unvisited.sort(key=lambda b: math.hypot(b["coords"]["x"] - curr_x, b["coords"]["y"] - curr_y))
                nearest = unvisited.pop(0)
                ordered_route.append(nearest["id"])
                curr_x, curr_y = nearest["coords"]["x"], nearest["coords"]["y"]
                
            bin_ids = ordered_route
            
        truck["route_queue"] = bin_ids
        truck["target_bin_id"] = truck["route_queue"].pop(0) if truck["route_queue"] else None
        truck["status"] = "EN_ROUTE"
        
        return {
            "success": True,
            "truck_id": truck_id,
            "target_bin": truck["target_bin_id"],
            "queued_bins": truck["route_queue"],
            "message": f"{truck['name']} dispatched along dynamic route for {len(bin_ids)} bins."
        }

    def _check_auto_dispatch(self):
        """Autonomous fleet intelligence: auto-dispatches idle trucks to prevent overflow."""
        critical_bins = [b for b in self.twin.bins if b["current_fill_pct"] >= 92.0]
        if not critical_bins:
            return
            
        idle_trucks = [t for t in self.twin.trucks if t["status"] == "IDLE" and t["load_pct"] < 75.0]
        for truck in idle_trucks:
            if not critical_bins:
                break
            # Find closest critical bin
            tx, ty = truck["coords"]["x"], truck["coords"]["y"]
            critical_bins.sort(key=lambda b: math.hypot(b["coords"]["x"] - tx, b["coords"]["y"] - ty))
            top_bin = critical_bins.pop(0)
            self.dispatch_truck_to_route(truck["id"], [top_bin["id"]])

# Global simulation engine
sim_engine = SimulationEngine()
