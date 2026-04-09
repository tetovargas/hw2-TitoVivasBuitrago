# Medical Note Dictation AI.  Video Link: https://youtu.be/4lqdzmahITg	

AI-powered workflow that converts a clinician’s **spoken dictation** into a clean, structured **SOAP medical note**.

## Workflow Chosen
**Dictation-to-Structured Medical Note Generation**  
Converts raw voice dictation from doctors into ready-to-use SOAP notes for EHR systems.

## Who the User Is
Busy clinicians (physicians, PAs, NPs) who spend 1–2 hours daily on documentation.

## Input → Output
- **Input**: Raw spoken dictation (text)
- **Output**: Clean, structured SOAP note in Markdown

## Project Structure
- `app.py` – Main app (run individual test cases)
- `eval.py` – Runs full evaluation on test cases
- `eval_set.md` – 6 test cases (normal + edge + failure-prone)
- `eval_output_testcase_*.md` – Generated notes from evaluation

## How to Run

### 1. Install dependencies
```bash
python3 -m pip install -r requirements.txt
