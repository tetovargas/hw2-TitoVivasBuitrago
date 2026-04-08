import os
import sys
import anthropic

# ==================== CONFIGURABLE SYSTEM PROMPT ====================
# Edit this anytime to change behavior
SYSTEM_PROMPT = """You are an expert medical scribe. 
Convert the clinician's raw spoken dictation into a clean, professional, structured medical note.
Use standard **SOAP format** (Subjective, Objective, Assessment, Plan).
Rules:
- Remove all filler words (um, uh, like, you know, etc.)
- Use proper medical terminology and abbreviations where appropriate
- Be concise, clear, and clinically accurate
- Never add information that was not in the dictation
- Output ONLY the structured Markdown note. No explanations."""

# Sample test cases from eval_set.md
TEST_CASES = {
    1: "Patient is a 62 year old male here for follow-up of type 2 diabetes. He says his sugars have been running between 110 and 140. He's compliant with metformin 1000 mg twice daily. No hypoglycemia. No neuropathy symptoms. A1c last month was 6.8. Exam shows normal foot exam. Assessment: type 2 diabetes mellitus well controlled. Plan: continue current meds, recheck A1c in three months, continue lifestyle modifications.",
    
    4: "Um so this is Mrs. Patel uh 55 year old female here for uh follow-up of hypertension and also she had some knee pain last time wait no that was two visits ago. Blood pressure today is 142 over 88. She's taking lisinopril. Actually make that 132 over 88 I misread it. No chest pain. Um plan is increase lisinopril to 20 mg and recheck in four weeks.",
    
    5: "Mr. Thompson 48 year old male with chest pain last week. EKG normal. Troponin negative. Family history of heart disease in father at age 50. Could be cardiac or maybe just musculoskeletal. Assessment hmm probably rule out ACS. Plan stress test and continue aspirin."
}

def generate_medical_note(dictation: str, model: str = "claude-3-5-sonnet-20241022") -> str:
    """Call Claude to turn raw dictation into structured SOAP note."""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    response = client.messages.create(
        model=model,
        max_tokens=800,
        temperature=0.0,          # deterministic output
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Convert this dictation into a structured medical note:\n\n{dictation}"}
        ]
    )
    return response.content[0].text.strip()

def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY environment variable is not set.")
        print("   1. Go to https://console.anthropic.com/settings/keys")
        print("   2. Create a new key")
        print("   3. Copy .env.example to .env and paste your key")
        sys.exit(1)

    # Choose test case from command line (default = Test Case 1)
    test_case_id = 1
    if len(sys.argv) > 1:
        try:
            test_case_id = int(sys.argv[1])
        except ValueError:
            print("Usage: python app.py [test_case_number]")
            print("Available: 1 (normal), 4 (edge), 5 (failure-prone)")
            sys.exit(1)

    dictation = TEST_CASES.get(test_case_id)
    if not dictation:
        print(f"⚠️ Test case {test_case_id} not found. Using Test Case 1.")
        dictation = TEST_CASES[1]

    print(f"🚀 Processing Test Case {test_case_id} with Claude...\n")
    print("Raw Dictation:")
    print("-" * 60)
    print(dictation[:400] + "..." if len(dictation) > 400 else dictation)
    print("\n" + "=" * 70)

    print("Calling Claude to generate structured medical note...\n")
    note = generate_medical_note(dictation)

    print("✅ STRUCTURED MEDICAL NOTE (SOAP)")
    print("=" * 70)
    print(note)

    # Save to file
    filename = f"medical_note_testcase_{test_case_id}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Medical Note - Test Case {test_case_id} (Claude)\n\n")
        f.write(note)

    print(f"\n💾 Note saved to → {filename}")

if __name__ == "__main__":
    main()
