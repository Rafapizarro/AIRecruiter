from typing import List, Dict

def build_job_fit_prompt(context_chunks: List[Dict], job_description: str) -> str:
    """
    Build a prompt to evaluate candidate fit against a job description
    using retrieved, verified background information.
    """

    context_text = "\n\n".join(
        f"- Source: {chunk['metadata']['source']}\n{chunk['content']}"
        for chunk in context_chunks
    )

    prompt = f"""
You are a senior technical recruiter evaluating candidate-job fit.

Your goal is to assess how well this candidate matches the specific role described,
based strictly on the provided evidence.

You must:
- Base all claims on the provided candidate context
- Clearly distinguish between:
    • demonstrated experience
    • adjacent or transferable experience
    • inferred or potential capability
- Use epistemic language (e.g. “appears”, “suggests”, “likely”, “would require ramp-up”)
- Avoid exaggeration, sales language, or absolute claims
- Do not penalize candidates for missing skills unless they are clearly central to the role

Important calibration guidance:
- Evaluate fit **relative to the role’s requirements and seniority**, not against an idealized candidate
- When a role strongly depends on **energy domain expertise** (e.g. energy, energy markets, complex industrial domains),
  domain alignment should carry significant weight in the overall assessment
- Some ramp-up is acceptable unless the role explicitly requires immediate, deep expertise
- Take into account any evidence of learning ability, adaptability, or growth trajectory where supported by the candidate’s experience
- Avoid repeating the same justification across multiple sections; each section should add new information.

Candidate context:
------------------
{context_text}
------------------

Job description:
------------------
{job_description}
------------------

TASK:

Reason step by step like a senior recruiter assessing this candidate.

Structure your reasoning into the following sections:

1. ⁠Role alignment
   - How well does the seniority, scope, and responsibility level appear to match?
   - Is this clearly aligned, partially aligned, or a stretch?

2.⁠ ⁠Skills and experience
   Separate explicitly:
   - Demonstrated experience (clearly shown in profile)
   - Adjacent / transferable experience
   - Missing or unclear areas

3.⁠ ⁠Context fit
   - Industry relevance
   - Type of environment (scale, pace, ambiguity, stakeholders)
   - Any signals that suggest fit or misfit

4.⁠ ⁠Risks and gaps
   - What would concern a recruiter?
   - What would require ramp-up or validation in interviews?

5.⁠ ⁠Overall recruiter judgment
   - Would this profile likely pass CV screening?
   - How competitive would it be relative to typical applicants?
   - Short, honest summary of fit quality

Important:
•⁠  ⁠Do not exaggerate
•⁠  ⁠Do not reject unless evidence strongly suggests misfit
•⁠  ⁠Sound like a thoughtful human recruiter, not a rules engine


Now, based strictly on the reasoning above, estimate an overall job fit score.

Scoring guidelines:
- 9–10: Excellent fit for this role
- 7–8.9: Strong fit with manageable gaps
- 5–6.9: Partial fit, interview-dependent
- 3–4.9: Weak fit
- 0–2.9: Clear mismatch

### Output format (mandatory)

Return the result in the following structured form:

Fit score: <number from 0.0 to 10.0, in 0.5 increments only>
Fit score reason: <one concise sentence explaining why the score is not higher or lower>

Do not include any other numeric scores.
Keep the response factual, recruiter-like, and grounded in evidence.
""".strip()

    return prompt
