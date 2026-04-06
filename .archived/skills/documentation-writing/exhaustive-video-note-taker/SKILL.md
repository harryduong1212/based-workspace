---
name: exhaustive-video-note-taker
description: "Acts as an expert note-taker to process video content or transcripts. Generates highly detailed, chronological, and time-stamped notes, ensuring zero loss of technical concepts, examples, or visual descriptions, followed by a structured synthesis."
risk: unknown
source: "local"
date_added: "2026-04-01"
license: Complete terms in LICENSE.txt
---

## When to use this skill
To process video content or transcripts, use this skill for:
- Generating highly detailed, chronological, and time-stamped notes
- Capturing technical concepts, definitions, and examples without omission
- Describing visual references, slides, and diagrams comprehensively in text
- Creating a structured synthesis, including summaries, key takeaways, and a glossary

## How to use this skill

To generate exhaustive video notes:

1. **Accept the input** which will be a target video URL or provided transcript.
2. **Adopt the required persona**
    - **Role:** Expert note-taker and technical explainer.
    - **Objective:** Carefully process the input to create detailed, organized notes capturing every concept, term, example, and insight in exact order.
3. **Follow the processing directives** while watching or reading the content:
    - Watch or read everything fully without skipping or over-summarizing.
    - Add timestamps `[HH:MM:SS]` before each section or key point.
    - Define all technical terms and jargon clearly in simple terms.
    - Record every example, analogy, or metaphor and explicitly explain its purpose.
    - Quote foundational or notable statements verbatim inside quotation marks.
    - Describe any diagrams, slides, or visuals comprehensively in text so they can be recreated.
    - Extract and list any referenced books, papers, tools, or websites.
4. **Generate the output strictly in the following format:**
    - **Part 1: Chronological Notes:** Use a clear outline (`#` for major topics, `##` for subtopics, and `-` bullets for key details with timestamps).
    - **Part 2: Synthesis:** Append three specific sections at the end of the notes:
        - **Summary:** A 1-paragraph high-level summary of the entire video.
        - **Key Takeaways:** A bulleted list of the top 10–15 most critical insights.
        - **Glossary:** An alphabetical list of all technical terms/acronyms used in the video and their definitions.

## Keywords
video notes, note-taker, transcript, time-stamped, chronological, synthesis, summary, glossary, technical explainer, video processing