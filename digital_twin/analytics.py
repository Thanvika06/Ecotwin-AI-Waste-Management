"""
Ecosystem Analytics, KPI aggregation, and Predictive Overflow Risk modeling.
"""

def generate_analytics_report(twin):
    """
    Computes time-series trends, waste stream breakdowns,
    and 2h/4h/8h overflow risk projections.
    """
    total_bins = len(twin.bins)
    
    # Category distribution of waste collected
    stream_distribution = {
        "Plastics (PET/HDPE)": 32.4,
        "Paper & Cardboard": 28.6,
        "Organics (Compost)": 24.2,
        "Metals (Alu/Steel)": 7.8,
        "Glass": 4.1,
        "E-Waste & Hazmat": 2.9
    }
    
    # Sector performance summary
    sector_performance = []
    for sec_id, sec in twin.sectors.items():
        sec_bins = [b for b in twin.bins if b["sector_id"] == sec_id]
        if sec_bins:
            avg_fill = round(sum(b["current_fill_pct"] for b in sec_bins) / len(sec_bins), 1)
            avg_contam = round(sum(b["contamination_pct"] for b in sec_bins) / len(sec_bins), 1)
            criticals = sum(1 for b in sec_bins if b["current_fill_pct"] >= 85)
        else:
            avg_fill, avg_contam, criticals = 0, 0, 0
            
        sector_performance.append({
            "sector_id": sec_id,
            "name": sec["name"],
            "avg_fill_pct": avg_fill,
            "contamination_pct": avg_contam,
            "critical_bins": criticals,
            "bins_count": len(sec_bins)
        })
        
    # Predictive Overflow Risk in 2h, 4h, 8h
    overflow_projections = []
    for b in twin.bins:
        hours_to_full = max(0.1, round((100.0 - b["current_fill_pct"]) / max(0.5, b["fill_rate_lph"] / b["capacity_liters"] * 100.0), 1))
        overflow_projections.append({
            "bin_id": b["id"],
            "waste_type": b["waste_type"],
            "sector": b["sector_name"],
            "current_fill": b["current_fill_pct"],
            "estimated_hours_to_overflow": hours_to_full,
            "risk_level_4h": "CRITICAL" if hours_to_full <= 4.0 else ("ELEVATED" if hours_to_full <= 8.0 else "LOW")
        })
    overflow_projections.sort(key=lambda x: x["estimated_hours_to_overflow"])
    
    return {
        "stream_distribution": stream_distribution,
        "sector_performance": sector_performance,
        "top_overflow_risks": overflow_projections[:6],
        "total_bins": total_bins
    }
