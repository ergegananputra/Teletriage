"""
Clinical syndrome detection layer for production-grade triage.
Replaces direct symptom-to-triage mapping with syndrome-based reasoning.
"""

from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class SyndromeResult:
    """Clinical syndrome detection result."""
    name: str
    score: float
    reasons: List[str]
    
    def __str__(self):
        return f"{self.name} (score: {self.score:.2f})"

def detect_syndromes(data: Dict[str, Any]) -> List[SyndromeResult]:
    """
    Detect clinical syndromes from patient data.
    Returns sorted list by confidence score (highest first).
    """
    syndromes = []
    
    symptoms = [s.lower() for s in data.get("symptoms", [])]
    risk_factors = [r.lower() for r in data.get("risk_factors", [])]
    medications = [m.lower() for m in data.get("medications", [])]
    past_history = [h.lower() for h in data.get("past_medical_history", [])]
    
    # Extract vitals safely
    heart_rate = _safe_int(data.get("heart_rate"))
    blood_pressure = str(data.get("blood_pressure", "")).lower()
    
    # --- ACUTE CORONARY SYNDROME (ACS) ---
    acs_symptoms = ["nyeri dada", "nyeri dada berat", "nyeri dada menyebar", 
                    "nyeri dada seperti ditindih", "nyeri epigastrium", "nyeri ulu hati"]
    acs_risks = ["diabetes", "riwayat penyakit jantung", "hipertensi", "kolesterol tinggi"]
    
    if (any(sym in symptoms for sym in acs_symptoms) and 
        any(risk in risk_factors for risk in acs_risks)):
        reasons = []
        if any(sym in symptoms for sym in acs_symptoms):
            reasons.append("chest pain symptoms")
        if any(risk in risk_factors for risk in acs_risks):
            reasons.append("cardiac risk factors")
        
        syndromes.append(SyndromeResult(
            "ACS", 
            0.85, 
            reasons
        ))
    
    # --- SEPSIS ---
    sepsis_symptoms = ["bingung", "kebingungan", "perubahan perilaku", "delirium", 
                     "demam tinggi", "menggigil", "kulit pucat", "sianosis"]
    sepsis_risks = ["infeksi", "luka terbuka", "operasi baru", "imunokompromais"]
    
    if (any(sym in symptoms for sym in sepsis_symptoms) and 
        heart_rate and heart_rate > 100 and
        any(risk in risk_factors for risk in sepsis_risks)):
        reasons = []
        if any(sym in symptoms for sym in ["bingung", "kebingungan", "delirium"]):
            reasons.append("altered mental status")
        if heart_rate and heart_rate > 100:
            reasons.append("tachycardia")
        if any(risk in risk_factors for risk in sepsis_risks):
            reasons.append("infection risk")
        
        syndromes.append(SyndromeResult(
            "Sepsis", 
            0.90, 
            reasons
        ))
    
    # --- PULMONARY EMBOLISM (PE) ---
    pe_symptoms = ["sesak napas mendadak", "sesak napas berat", "nyeri dada pleuritik", 
                  "nyeri dada saat bernapas", "batuk darah", "hemoptisis"]
    pe_risks = ["obesitas", "immobilisasi", "operasi besar", "kontrasepsi oral", 
                "riwayat pembekuan darah", "kanker"]
    
    if (any(sym in symptoms for sym in pe_symptoms) and 
        any(risk in risk_factors for risk in pe_risks)):
        reasons = []
        if "sesak napas" in " ".join(symptoms):
            reasons.append("acute dyspnea")
        if any(sym in symptoms for sym in ["nyeri dada pleuritik", "nyeri dada saat bernapas"]):
            reasons.append("pleuritic chest pain")
        if any(risk in risk_factors for risk in pe_risks):
            reasons.append("PE risk factors")
        
        syndromes.append(SyndromeResult(
            "Pulmonary Embolism", 
            0.85, 
            reasons
        ))
    
    # --- ECTOPIC PREGNANCY ---
    if data.get("sex", "").lower() == "perempuan":
        ectopic_symptoms = ["nyeri perut bagian bawah", "nyeri perut satu sisi", 
                          "perdarahan vagina", "spotting", "pingsan", "syok"]
        ectopic_risks = ["hamil", "telat haid", "riwayat kehamilan ektopik", 
                       "kb spiral", "infeksi pelvik"]
        
        if (any(sym in symptoms for sym in ectopic_symptoms) and 
            any(risk in risk_factors for risk in ectopic_risks)):
            reasons = []
            if any(sym in symptoms for sym in ["nyeri perut bagian bawah", "nyeri perut satu sisi"]):
                reasons.append("lower abdominal pain")
            if any(sym in symptoms for sym in ["perdarahan vagina", "spotting"]):
                reasons.append("vaginal bleeding")
            if any(risk in risk_factors for risk in ["hamil", "telat haid"]):
                reasons.append("pregnancy status")
            
            syndromes.append(SyndromeResult(
                "Ectopic Pregnancy", 
                0.95, 
                reasons
            ))
    
    # --- DIABETIC KETOACIDOSIS (DKA) ---
    dka_symptoms = ["muntah berulang", "mual hebat", "nyeri perut", 
                   "napas cepat", "napas dalam", "bau aseton napas", "dehidrasi"]
    dka_medications = ["insulin", "metformin", "glibenklamid", "glimepiride"]
    dka_risks = ["diabetes", "diabetes tipe 1", "diabetes tipe 2"]
    
    if (any(sym in symptoms for sym in dka_symptoms) and 
        any(risk in risk_factors for risk in dka_risks)):
        reasons = []
        if any(sym in symptoms for sym in ["muntah berulang", "mual hebat"]):
            reasons.append("GI symptoms")
        if any(sym in symptoms for sym in ["napas cepat", "napas dalam"]):
            reasons.append("kussmaul breathing")
        if any(risk in risk_factors for risk in dka_risks):
            reasons.append("diabetes history")
        
        syndromes.append(SyndromeResult(
            "DKA", 
            0.90, 
            reasons
        ))
    
    # --- STROKE ---
    stroke_symptoms = ["lemah satu sisi", "lemah tangan", "lemah kaki", "wajah mencong", 
                      "bicara pelo", "sulit bicara", "penglihatan ganda", "pusing berat"]
    stroke_risks = ["hipertensi", "diabetes", "riwayat stroke", "fibrilasi atrial", 
                   "merokok", "obesitas"]
    
    if (any(sym in symptoms for sym in stroke_symptoms) and 
        any(risk in risk_factors for risk in stroke_risks)):
        reasons = []
        if any(sym in symptoms for sym in ["lemah satu sisi", "lemah tangan", "lemah kaki"]):
            reasons.append("focal weakness")
        if any(sym in symptoms for sym in ["wajah mencong", "bicara pelo", "sulit bicara"]):
            reasons.append("facial droop/speech changes")
        if any(risk in risk_factors for risk in stroke_risks):
            reasons.append("stroke risk factors")
        
        syndromes.append(SyndromeResult(
            "Stroke", 
            0.85, 
            reasons
        ))
    
    # --- APPENDICITIS ---
    appendicitis_symptoms = ["nyeri perut kanan bawah", "nyeri perut memburuk", 
                            "mual", "muntah", "demam", "nafsu makan hilang"]
    
    if (any(sym in symptoms for sym in appendicitis_symptoms) and 
        "nyeri perut kanan bawah" in " ".join(symptoms)):
        reasons = []
        reasons.append("RLQ pain")
        if any(sym in symptoms for sym in ["demam", "mual", "muntah"]):
            reasons.append("systemic symptoms")
        
        syndromes.append(SyndromeResult(
            "Appendicitis", 
            0.75, 
            reasons
        ))
    
    # Return sorted by confidence score (highest first)
    return sorted(syndromes, key=lambda x: x.score, reverse=True)

def _safe_int(value: Any) -> int:
    """Safely convert value to int, return None if invalid."""
    try:
        if value is None or value == "":
            return None
        return int(float(str(value)))
    except (ValueError, TypeError):
        return None

# Test cases for validation
if __name__ == "__main__":
    # Test ACS case
    acs_case = {
        "symptoms": ["nyeri dada berat"],
        "risk_factors": ["diabetes", "hipertensi"],
        "medications": ["aspirin"],
        "past_medical_history": [],
        "heart_rate": 95,
        "blood_pressure": "140/90",
        "sex": "laki-laki"
    }
    
    # Test Ectopic case
    ectopic_case = {
        "symptoms": ["nyeri perut bagian bawah", "spotting"],
        "risk_factors": ["hamil"],
        "medications": [],
        "past_medical_history": [],
        "heart_rate": 100,
        "blood_pressure": "110/70",
        "sex": "perempuan"
    }
    
    # Test Sepsis case
    sepsis_case = {
        "symptoms": ["bingung", "demam tinggi"],
        "risk_factors": ["infeksi"],
        "medications": [],
        "past_medical_history": [],
        "heart_rate": 120,
        "blood_pressure": "90/60",
        "sex": "laki-laki"
    }
    
    print("=== SYNDROME ENGINE TEST RESULTS ===")
    for i, (case, name) in enumerate([(acs_case, "ACS"), (ectopic_case, "Ectopic"), (sepsis_case, "Sepsis")]):
        print(f"\n{name} Case:")
        syndromes = detect_syndromes(case)
        for syndrome in syndromes:
            print(f"  - {syndrome.name}: {syndrome.score:.2f} ({', '.join(syndrome.reasons)})")
