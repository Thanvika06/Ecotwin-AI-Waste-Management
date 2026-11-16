"""
Comprehensive Material Database and Waste Taxonomy.
Defines classification rules, resin codes, recyclability statuses, 
citizen preparation guides, and contamination risk factors.
"""

TAXONOMY = {
    "Plastics": {
        "color": "#3B82F6",
        "bin_color": "Blue / Yellow",
        "icon": "bottle-water",
        "description": "Synthetic polymers including beverage bottles, food containers, jugs, and packaging.",
        "subtypes": {
            "PET_1": {
                "name": "PET (Polyethylene Terephthalate #1)",
                "common_items": ["Water bottles", "Soda bottles", "Cooking oil containers", "Fruit clamshells"],
                "recyclable": True,
                "recyclability_index": 95,
                "circular_product": "Polyester fleece fibers, carpet yarn, new food-grade bottles",
                "prep_instructions": "Empty liquid completely, rinse, keep plastic cap on or flatten.",
                "contamination_risks": ["Leftover sweetened liquids causing mold", "PVC shrink sleeves", "Food oils"]
            },
            "HDPE_2": {
                "name": "HDPE (High-Density Polyethylene #2)",
                "common_items": ["Milk jugs", "Detergent bottles", "Shampoo bottles", "Bleach containers"],
                "recyclable": True,
                "recyclability_index": 92,
                "circular_product": "Plastic lumber, drainage pipes, recycling bins, playground equipment",
                "prep_instructions": "Rinse thoroughly to remove soap/detergent residues, replace cap.",
                "contamination_risks": ["Chemical residue", "Hazardous pesticide containers"]
            },
            "LDPE_4": {
                "name": "LDPE (Low-Density Polyethylene #4)",
                "common_items": ["Grocery bags", "Bubble wrap", "Bread bags", "Flexible squeezy bottles"],
                "recyclable": "Conditional",
                "recyclability_index": 55,
                "circular_product": "Trash liners, composite lumber, shipping envelopes",
                "prep_instructions": "Do not mix with rigid plastics; take to designated retail film drop-offs.",
                "contamination_risks": ["Tangles in MRF sorting trommels and disc screens (high jam risk)"]
            },
            "PP_5": {
                "name": "PP (Polypropylene #5)",
                "common_items": ["Yogurt tubs", "Medicine bottles", "Bottle caps", "Syrup bottles"],
                "recyclable": True,
                "recyclability_index": 80,
                "circular_product": "Battery cases, ice scrapers, bicycle racks, storage bins",
                "prep_instructions": "Scrape food clean, lightly rinse, check for local MRF acceptance.",
                "contamination_risks": ["Food crust, dairy odor attraction for vermin"]
            },
            "PS_6": {
                "name": "Polystyrene / Styrofoam (#6)",
                "common_items": ["Styrofoam cups", "Egg cartons", "Takeout clamshells", "Foam packing peanuts"],
                "recyclable": False,
                "recyclability_index": 12,
                "circular_product": "Difficult to recycle mechanically; requires specialized densification.",
                "prep_instructions": "Dispose in Residual / Landfill bin unless drop-off foam station exists.",
                "contamination_risks": ["Crumbling microplastics contaminate paper pulping streams"]
            }
        }
    },
    "Paper & Cardboard": {
        "color": "#F59E0B",
        "bin_color": "Blue / Gray",
        "icon": "box",
        "description": "Cellulose fiber products including corrugated cartons, newsprint, office paper, and kraft bags.",
        "subtypes": {
            "OCC": {
                "name": "Old Corrugated Cardboard (OCC)",
                "common_items": ["Shipping boxes", "Delivery cartons", "Appliance packaging"],
                "recyclable": True,
                "recyclability_index": 98,
                "circular_product": "New corrugated medium, recycled cardboard boxes, paperboard",
                "prep_instructions": "Flatten completely to save bin volume, remove large plastic packing tapes.",
                "contamination_risks": ["Rain/water moisture weakening fiber", "Packing foam peanuts left inside"]
            },
            "Mixed_Paper": {
                "name": "Mixed Office Paper & Magazines",
                "common_items": ["Printer paper", "Magazines", "Catalogs", "Envelopes without plastic windows"],
                "recyclable": True,
                "recyclability_index": 90,
                "circular_product": "Tissue paper, paper towels, newsprint",
                "prep_instructions": "Keep clean and completely dry. Do not shred unless necessary.",
                "contamination_risks": ["Grease, laminated plastic coatings, foil stamping"]
            },
            "Food_Soiled_Paper": {
                "name": "Food-Soiled Cardboard (Pizza Boxes, Fast Food Wrappers)",
                "common_items": ["Greasy pizza boxes", "Used paper napkins", "Bakery paper bags"],
                "recyclable": False,
                "recyclability_index": 15,
                "circular_product": "Commercial composting (if certified unbleached/PFAS-free) or Anaerobic Digestion",
                "prep_instructions": "Tear off clean top lid for cardboard recycling; put greasy bottom half in Compost.",
                "contamination_risks": ["Oil & grease bind to cellulose fibers, ruining entire pulp batches"]
            }
        }
    },
    "Metals": {
        "color": "#10B981",
        "bin_color": "Yellow / Orange",
        "icon": "shield",
        "description": "Ferrous and non-ferrous infinitely recyclable metals including aluminum and tin cans.",
        "subtypes": {
            "Aluminum_Cans": {
                "name": "UBC Aluminum Beverage Cans",
                "common_items": ["Soda cans", "Beer cans", "Seltzer cans"],
                "recyclable": True,
                "recyclability_index": 100,
                "circular_product": "New aluminum beverage cans within 60 days (infinitely recyclable, saves 95% energy)",
                "prep_instructions": "Empty liquid completely. Do not crush if optical sorters use 3D shape identification.",
                "contamination_risks": ["Cigarette butts pushed into cans, liquid residues"]
            },
            "Steel_Tin_Cans": {
                "name": "Steel Food & Soup Cans",
                "common_items": ["Tomato sauce cans", "Tuna cans", "Pet food tins"],
                "recyclable": True,
                "recyclability_index": 96,
                "circular_product": "Reinforcing steel rebar, automobile frames, new tinplate cans",
                "prep_instructions": "Rinse food residue, push detached lid inside the can and squeeze slightly.",
                "contamination_risks": ["Dried food remnants attract pests at MRF sorting facilities"]
            }
        }
    },
    "Glass": {
        "color": "#06B6D4",
        "bin_color": "Cyan / Green",
        "icon": "glass-whiskey",
        "description": "Inorganic soda-lime container glass, bottles, and jars.",
        "subtypes": {
            "Container_Glass": {
                "name": "Soda-Lime Container Glass",
                "common_items": ["Wine bottles", "Pickle jars", "Beer bottles", "Sauce containers"],
                "recyclable": True,
                "recyclability_index": 98,
                "circular_product": "New glass bottles & jars (cullet), fiberglass insulation, water filtration sand",
                "prep_instructions": "Rinse food contents, discard metal or cork lids in respective bins.",
                "contamination_risks": ["Ceramics, porcelain, Pyrex / borosilicate glass (different melting points destroy batch)"]
            }
        }
    },
    "Organics": {
        "color": "#84CC16",
        "bin_color": "Green / Brown",
        "icon": "leaf",
        "description": "Biodegradable food scraps, garden trimmings, coffee grounds, and yard waste.",
        "subtypes": {
            "Food_Scraps": {
                "name": "Food Residues & Peelings",
                "common_items": ["Fruit peels", "Vegetable trimmings", "Coffee grounds", "Eggshells"],
                "recyclable": "Compostable",
                "recyclability_index": 96,
                "circular_product": "High-nutrient organic compost soil conditioner, Biogas (Methane) via Anaerobic Digestion",
                "prep_instructions": "Separate from any plastic stickers, bags, twist ties, or cling wrap.",
                "contamination_risks": ["Fruit PLU plastic stickers, plastic produce bags, cutlery"]
            }
        }
    },
    "E-Waste": {
        "color": "#8B5CF6",
        "bin_color": "Purple / Red",
        "icon": "microchip",
        "description": "Electrical and electronic items containing circuit boards, rare earth metals, or toxic elements.",
        "subtypes": {
            "Batteries_LiIon": {
                "name": "Lithium-Ion / Alkaline Batteries",
                "common_items": ["Phone batteries", "Laptop power cells", "AA/AAA batteries", "Vape devices"],
                "recyclable": "Special Drop-off",
                "recyclability_index": 88,
                "circular_product": "Cobalt, Lithium carbonate, Nickel, Copper recovery for EV battery gigafactories",
                "prep_instructions": "CRITICAL: Never put in standard bins. Tape lithium battery terminals with clear tape.",
                "contamination_risks": ["SEVERE FIRE HAZARD: Thermal runaway when crushed by compactor trucks"]
            },
            "Consumer_Electronics": {
                "name": "Small Electronics & Cables",
                "common_items": ["Smartphones", "Chargers", "Circuit boards", "Computer peripherals"],
                "recyclable": "Special Drop-off",
                "recyclability_index": 85,
                "circular_product": "Gold, Silver, Palladium, Copper, and high-impact engineering plastics",
                "prep_instructions": "Wipe personal data, bring to municipal e-waste depot or takeback depot.",
                "contamination_risks": ["Lead, mercury, and cadmium leaching into groundwater if landfilled"]
            }
        }
    },
    "Hazardous": {
        "color": "#EF4444",
        "bin_color": "Red / Hazard Orange",
        "icon": "triangle-exclamation",
        "description": "Toxic, corrosive, flammable, or bio-hazardous waste requiring specialized containment.",
        "subtypes": {
            "Chemicals_Paints": {
                "name": "Household Hazardous Chemicals & Solvents",
                "common_items": ["Paint cans", "Bleach bottles with residue", "Pesticides", "Motor oil containers"],
                "recyclable": False,
                "recyclability_index": 10,
                "circular_product": "Fuel blending for high-temperature cement kilns, neutralization",
                "prep_instructions": "Store in original sealed container, deliver to Hazardous Household Waste (HHW) depot.",
                "contamination_risks": ["Vapor explosions, poisoning sanitation workers, environmental toxicity"]
            }
        }
    },
    "Landfill / Residual": {
        "color": "#64748B",
        "bin_color": "Black / Dark Grey",
        "icon": "trash-can",
        "description": "Non-recyclable composite materials, hygiene products, and heavily contaminated waste.",
        "subtypes": {
            "Multi_Layer_Packaging": {
                "name": "Multi-layer Metallized Film & Pouches",
                "common_items": ["Potato chip bags", "Coffee foil pouches", "Candy wrappers", "Plastic straws"],
                "recyclable": False,
                "recyclability_index": 0,
                "circular_product": "Waste-to-Energy (incineration for district heat/electricity) or engineered fuel",
                "prep_instructions": "Dispose in residual bin. Strive to reduce consumption of single-use multi-materials.",
                "contamination_risks": ["Foil layer prevents optical sorting; melts incorrectly during polymer extrusion"]
            }
        }
    }
}

def get_material_info(primary_category, subtype=None):
    """Retrieve structured material information and instructions."""
    cat_data = TAXONOMY.get(primary_category)
    if not cat_data:
        return None
    if subtype and subtype in cat_data.get("subtypes", {}):
        subtype_data = cat_data["subtypes"][subtype]
        return {
            "category": primary_category,
            "color": cat_data["color"],
            "bin_color": cat_data["bin_color"],
            "subtype_key": subtype,
            **subtype_data
        }
    return {
        "category": primary_category,
        "color": cat_data["color"],
        "bin_color": cat_data["bin_color"],
        "description": cat_data["description"]
    }
