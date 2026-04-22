"""
Disease-specific recommended actions for clinical triage system.
Generates structured, syndrome-specific action plans with safety guidelines.
"""

from typing import Dict, List, Union

def generate_action_plan(syndrome: str) -> Dict[str, Union[List[str], str]]:
    """
    Generate syndrome-specific action plan with immediate actions, 
    hospital procedures, and specialist recommendations.
    
    SAFETY RULES:
    - NO drug dosages
    - NO invasive instructions  
    - Use safe language: "pertimbangkan", "akan dilakukan di RS", "perlu evaluasi"
    """
    
    plans = {
        "DKA": {
            "immediate": [
                "Segera ke IGD",
                "Hentikan sementara SGLT2 inhibitor",
                "Jika memungkinkan, pertahankan hidrasi (jika tidak muntah berat)"
            ],
            "hospital": [
                "Cek gas darah (asidosis metabolik)",
                "Cek keton darah/urin",
                "Monitoring elektrolit (terutama kalium)",
                "Terapi cairan intravena dan insulin (sesuai protokol)"
            ],
            "specialist": "Sp.PD (Endokrinologi/Metabolik)"
        },

        "ACS": {
            "immediate": [
                "Segera ke IGD",
                "Hindari aktivitas fisik",
                "Pertimbangkan aspirin jika tidak ada kontraindikasi"
            ],
            "hospital": [
                "EKG serial",
                "Pemeriksaan troponin",
                "Monitoring jantung kontinu"
            ],
            "specialist": "Sp.JP (Kardiologi)"
        },

        "Pulmonary Embolism": {
            "immediate": [
                "Segera ke IGD",
                "Hindari aktivitas berat"
            ],
            "hospital": [
                "D-dimer atau CT Pulmonary Angiography",
                "Evaluasi kebutuhan antikoagulan"
            ],
            "specialist": "Sp.P / Sp.PD"
        },

        "Ectopic Pregnancy": {
            "immediate": [
                "Segera ke IGD",
                "Jangan menunda jika ada nyeri hebat atau pusing"
            ],
            "hospital": [
                "USG transvaginal",
                "Pemeriksaan beta-hCG serial",
                "Evaluasi kemungkinan ruptur"
            ],
            "specialist": "Sp.OG"
        },

        "Sepsis": {
            "immediate": [
                "Segera ke IGD",
                "Pantau kesadaran dan tanda vital"
            ],
            "hospital": [
                "Kultur darah/urin",
                "Pemberian antibiotik empiris",
                "Resusitasi cairan"
            ],
            "specialist": "Sp.PD"
        },

        "Stroke": {
            "immediate": [
                "Segera ke IGD",
                "Catat waktu onset gejala"
            ],
            "hospital": [
                "CT scan kepala",
                "Evaluasi trombolisis jika memenuhi kriteria"
            ],
            "specialist": "Sp.S"
        },

        "Appendicitis": {
            "immediate": [
                "Segera ke IGD",
                "Puasa (hindari makan/minum)"
            ],
            "hospital": [
                "USG/CT abdomen",
                "Evaluasi tindakan bedah"
            ],
            "specialist": "Sp.B"
        }
    }

    # Default plan for unknown syndromes or critical vital signs
    return plans.get(syndrome, {
        "immediate": ["Evaluasi dokter lebih lanjut"],
        "hospital": [],
        "specialist": "Dokter umum"
    })

def get_action_summary(action_plan: Dict[str, Union[List[str], str]]) -> str:
    """
    Get human-readable summary of action plan.
    """
    immediate = action_plan.get("immediate", [])
    specialist = action_plan.get("specialist", "Dokter umum")
    
    if immediate:
        return f"Immediate: {', '.join(immediate[:2])} | Specialist: {specialist}"
    else:
        return f"Evaluasi dokter | Specialist: {specialist}"

def validate_action_plan_safety(action_plan: Dict[str, Union[List[str], str]]) -> bool:
    """
    Validate that action plan follows safety guidelines.
    """
    # Check for drug dosages (should not contain numbers with mg, mcg, etc.)
    all_actions = []
    all_actions.extend(action_plan.get("immediate", []))
    all_actions.extend(action_plan.get("hospital", []))
    
    for action in all_actions:
        action_lower = action.lower()
        # Check for dosage patterns
        if any(pattern in action_lower for pattern in ["mg", "mcg", "iu", "ml", "tablet", "kapsul"]):
            if any(char.isdigit() for char in action):
                return False
        
        # Check for invasive procedures
        if any(procedure in action_lower for procedure in ["insert", "tusuk", "catheter", "intubasi"]):
            return False
    
    return True

# Test cases for validation
if __name__ == "__main__":
    print("=== TREATMENT ENGINE TEST RESULTS ===")
    
    # Test all syndromes
    test_syndromes = ["DKA", "ACS", "Pulmonary Embolism", "Ectopic Pregnancy", 
                     "Sepsis", "Stroke", "Appendicitis", "Unknown Syndrome"]
    
    for syndrome in test_syndromes:
        print(f"\n{syndrome}:")
        plan = generate_action_plan(syndrome)
        
        print(f"  Immediate: {', '.join(plan['immediate'])}")
        print(f"  Hospital: {', '.join(plan['hospital'])}")
        print(f"  Specialist: {plan['specialist']}")
        
        # Safety validation
        is_safe = validate_action_plan_safety(plan)
        print(f"  Safety: {'PASS' if is_safe else 'FAIL'}")
        
        # Summary
        summary = get_action_summary(plan)
        print(f"  Summary: {summary}")
