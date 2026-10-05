# Study material

Everything you need to revise after (or alongside) the hands-on lessons.

| File | What it is | Use it when |
|---|---|---|
| [study-guide.pdf](study-guide.pdf) | every lesson on a page or less (concept, diagram, commands, recap), the DevOps workflow, troubleshooting method, command reference, capstone, glossary and interview questions, as one printable PDF (built by `study/tools/build_pdf.py`) | you want to revise offline, print or annotate |
| [glossary.md](glossary.md) | every term used in the course in plain words, with the lesson that explains it | a word in a lesson is unclear |
| [interview-questions.md](interview-questions.md) | 35 questions with model answers, from "Git vs GitHub" to supply-chain security and release pipelines | before an interview, or to test yourself |
| [../docs/command-reference.md](../docs/command-reference.md) | every command by purpose, linked to its lesson | you know what you want to do, not the command |

## How to study

1. Take the lessons in order, typing every command. Do the **Break it** part every time: it is where most of the
   learning happens.
2. Finish each module with its `assessment.md`. Not sure about a quiz answer? Re-run the lesson's lab and look.
3. After modules 09, 16 and 22, do a [project](../23-projects/README.md) without looking at the reference solution.
4. Revise with the study guide: for each lesson, explain the recap out loud, then check the full lesson if you could
   not.
5. End with the [capstone](../24-capstone/README.md) and the [final exam](../24-capstone/final-exam/README.md).

A suggested pace: one module per study session (1–2 hours), about five weeks part-time for the whole course.

## Rebuild the PDF

```text
pip install markdown
python study/tools/build_pdf.py        (uses a headless Chrome or Edge to print the PDF)
```
