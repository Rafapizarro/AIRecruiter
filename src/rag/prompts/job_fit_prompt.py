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
    Your goal is to reason thoughtfully, as a human recruiter would.

    You must:
    - Base claims on provided evidence
    - Clearly distinguish between:
        • demonstrated experience
        • adjacent or transferable experience
        • inferred or potential capability
    - Use epistemic language (e.g. “appears”, “suggests”, “likely”, “would require ramp-up”)
    - Avoid absolute claims unless evidence is explicit
    - Avoid exaggeration or sales language.
    - Take into account, based on his experience, the big learning skills of the candidate and his ability to thrive and quickly adapt.

    You are not scoring yet.
    You are reasoning.

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

1. Role alignment
   - How well does the seniority, scope, and responsibility level appear to match?
   - Is this clearly aligned, partially aligned, or a stretch?

2. Skills and experience
   Separate explicitly:
   - Demonstrated experience (clearly shown in profile)
   - Adjacent / transferable experience
   - Missing or unclear areas

3. Context fit
   - Industry relevance
   - Type of environment (scale, pace, ambiguity, stakeholders)
   - Any signals that suggest fit or misfit

4. Risks and gaps
   - What would concern a recruiter?
   - What would require ramp-up or validation in interviews?

5. Overall recruiter judgment
   - Would this profile likely pass CV screening?
   - How competitive would it be relative to typical applicants?
   - Short, honest summary of fit quality

Important:
- Do not exaggerate
- Do not reject unless evidence strongly suggests misfit
- Sound like a thoughtful human recruiter, not a rules engine

Now, based strictly on the reasoning above:

Estimate an overall job fit score from 0 to 10.

Guidelines:
- 9–10: Excellent fit, minimal concerns
- 7–8: Strong fit with some gaps
- 5–6: Partial fit, interview-dependent
- 3–4: Weak fit, significant gaps
- 0–2: Clear mismatch

If uncertainty exists, reflect it in the score.
Provide:
- The numeric score
- One sentence explaining why it is not higher or lower
- If the job is related to energy engineering and/or markets, the candidate is probably an excellent fit because of his energy engineering background

    Keep the response concise, factual, and grounded in evidence.
    """.strip()

    return prompt
