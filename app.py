import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# ==================== CONFIGURABLE SYSTEM PROMPT ====================
SYSTEM_PROMPT = """You are an expert medical scribe. 
Turn the clinician’s raw spoken dictation into a clean, professional SOAP medical note ready for EHR use.

**Output format (use these exact headings):**
- **Subjective**
- **Objective**
- **Assessment**
- **Plan**

**Strict rules:**
- Remove every filler word (um, uh, like, you know, actually, etc.)
- Use correct medical terminology and common abbreviations
- Be concise, clear, and factually accurate
- Never add, infer, or hallucinate any facts, diagnoses, or orders
- Preserve uncertainty exactly as spoken (e.g., keep “rule out ACS” or “probably musculoskeletal”)
- Use bullet points under Plan and Objective when multiple items are mentioned
- Output ONLY the Markdown note. No explanations, introductions, or closing text."""

# Sample test cases from eval_set.md
TEST_CASES = {
    1: "Patient is a 62 year old male here for follow-up of type 2 diabetes. He says his sugars have been running between 110 and 140. He's compliant with metformin 1000 mg twice daily. No hypoglycemia. No neuropathy symptoms. A1c last month was 6.8. Exam shows normal foot exam. Assessment: type 2 diabetes mellitus well controlled. Plan: continue current meds, recheck A1c in three months, continue lifestyle modifications.",
    
    4: "Um so this is Mrs. Patel uh 55 year old female here for uh follow-up of hypertension and also she had some knee pain last time wait no that was two visits ago. Blood pressure today is 142 over 88. She's taking lisinopril. Actually make that 132 over 88 I misread it. No chest pain. Um plan is increase lisinopril to 20 mg and recheck in four weeks.",
    
    5: "Mr. Thompson 48 year old male with chest pain last week. EKG normal. Troponin negative. Family history of heart disease in father at age 50. Could be cardiac or maybe just musculoskeletal. Assessment hmm probably rule out ACS. Plan stress test and continue aspirin."
}

def generate_medical_note(dictation: str, model_name: str = "gemini-2.5-flash") -> str:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=SYSTEM_PROMPT
    )
    
    response = model.generate_content(
        f"Convert this dictation into a structured medical note:\n\n{dictation}"
    )
    return response.text.strip()

def main():
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable is not set.")
        print("   1. Go to https://aistudio.google.com/app/apikey")
        print("   2. Create a new API key")
        print("   3. Paste it in your .env file as GEMINI_API_KEY=...")
        sys.exit(1)

    test_case_id = 1
    if len(sys.argv) > 1:
        try:
            test_case_id = int(sys.argv[1])
        except ValueError:
            print("Usage: python3 app.py [test_case_number]")
            print("Available: 1 (normal), 4 (edge), 5 (failure-prone)")
            sys.exit(1)

    dictation = TEST_CASES.get(test_case_id)
    if not dictation:
        dictation = TEST_CASES[1]

    print(f"🚀 Processing Test Case {test_case_id} with Google Gemini...\n")
    print("Raw Dictation:")
    print("-" * 60)
    print(dictation[:400] + "..." if len(dictation) > 400 else dictation)
    print("\n" + "=" * 70)

    print("Calling Gemini to generate structured medical note...\n")
    note = generate_medical_note(dictation)

    print("✅ STRUCTURED MEDICAL NOTE (SOAP)")
    print("=" * 70)
    print(note)

    filename = f"medical_note_testcase_{test_case_id}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Medical Note - Test Case {test_case_id} (Gemini)\n\n")
        f.write(note)

    print(f"\n💾 Note saved to → {filename}")

if __name__ == "__main__":
    main()