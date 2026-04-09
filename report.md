# Medical Note Dictation AI – Final Report

## 1. Business Use Case
The selected workflow is **Dictation-to-Structured Medical Note Generation** in a clinical/hospital environment.  
Physicians, PAs, and NPs routinely dictate patient encounters (history, exam, assessment, plan) immediately after or during a visit. The spoken narrative must be turned into a clean, compliant SOAP note that can be directly inserted into an Electronic Health Record (EHR) such as Epic or Cerner.

**Input**: Raw spoken dictation (or voice-to-text output) + optional patient metadata.  
**Output**: Fully structured Markdown SOAP note ready for copy-paste or API insertion.  

This task is highly valuable to automate because documentation consumes up to 50 % of a clinician’s workday and is a leading driver of burnout. Even a 60–80 % reduction in note-writing time would free providers to see more patients and improve work–life balance while maintaining clinical accuracy and compliance.

## 2. Model Choice and Observations
We ultimately chose **Google Gemini 2.5 Flash** (`gemini-2.5-flash`).

**Reasoning**:
- Generous free tier (no credit card required for low-volume prototyping).
- Excellent structured-output performance on medical tasks.
- Fast and reliable for SOAP formatting.

**Brief comparison with other models tested**:
- **Claude 3.5 Sonnet**: Very strong clinical reasoning and safety, but we encountered immediate credit-balance errors even after purchasing credits.
- **GPT-4o-mini (OpenAI)**: Worked well but required switching due to the user’s preference for a free-tier solution.

Gemini provided the best balance of cost, speed, and output quality for this prototype.

## 3. Baseline vs. Final Prompt Iteration

**Initial Version (v1)** – Simple, basic instructions.  
**Revision 1 (v2)** – Added explicit Markdown headings and a strong anti-hallucination rule.  
**Revision 2 (v3 – Final)** – Further tightened formatting, added bullet-point guidance, and reinforced preservation of clinical uncertainty.

**Key changes and evidence**:
- The strongest improvement came in **Test Case 5** (ambiguous chest-pain / “rule out ACS”). The baseline prompt occasionally produced over-confident diagnoses. After Revision 1 and especially Revision 2, the model consistently preserved the exact uncertainty language (“rule out ACS”, “probably musculoskeletal”) without hallucinating a definitive diagnosis.
- Test Case 4 (disorganized dictation with fillers) showed cleaner removal of filler words and better self-correction handling after the revisions.
- Overall output became more visually consistent (proper **bold headings** and bullet points under Plan/Objective).

The prompt iterations demonstrably increased safety and formatting reliability without sacrificing conciseness.

## 4. Remaining Limitations & Human Review Needs
Even with the improved prompt, the prototype still requires human review in several situations:
- Highly ambiguous or contradictory dictations (the model may still smooth over contradictions instead of flagging them).
- Complex multi-problem visits or rare medical terminology not seen during training.
- Any note that will be used for billing, legal, or high-risk clinical decisions.
- Cases involving sensitive topics (psychiatry, abuse, end-of-life) where tone and nuance matter.

In production, a “human-in-the-loop” workflow (clinician reviews and signs off every note) is mandatory.

## 5. Deployment Recommendation
**Yes, I recommend deploying this workflow as a first-pass assistant**, but **only under strict conditions**:
- Always keep the clinician as the final reviewer and sign-off authority.
- Start with low-risk outpatient follow-up visits.
- Implement automatic flagging for uncertain language or missing required elements.
- Monitor outputs with the evaluation set on a regular basis and continue prompt tuning.
- Do **not** use the system for high-acuity, high-liability, or purely automated documentation without human oversight.

Under these guardrails, the tool can meaningfully reduce documentation burden and clinician burnout while maintaining (or even improving) note quality and safety.

**Conclusion**: This prototype successfully demonstrates a high-value, realistic automation target. With continued prompt refinement and proper human oversight, it is ready for pilot deployment in a controlled clinical environment.
