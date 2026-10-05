# LinkedIn package

| File | Use |
|---|---|
| `post.md` | Post text |
| `carousel/carousel.pdf` | **Recommended:** upload as a *Document* post. LinkedIn shows it as a swipeable carousel |
| `carousel/slide-01.png` … `slide-11.png` | The same slides as images (1080×1350), for a multi-image post |
| `carousel/slides.html` | Source of the slides; re-render a slide with a headless browser (`slides.html?s=N`) |
| `carousel/qr-repo.svg`, `qr-portfolio.svg` | The QR codes used on the last slide |
| `project-image.png` | Single overview image (1200×627), from `project-image.html` |
| `project-summary.md` | Short technical summary |
| `hashtags.txt` | Hashtags |

## The slides (one picture per idea)

| # | Visual | Message |
|---|---|---|
| 1 | A branch graph and three numbers: 98 lessons, 18 labs, 1,308 tested blocks | What it is |
| 2 | Four panels: conflict, lost work, rejected push, committed secret | The pain |
| 3 | The ten-step method with Break / Troubleshoot / Fix highlighted | The method |
| 4 | Working directory → staging area → repository → remote | Concept: where changes live |
| 5 | reset --soft / --mixed / --hard as a table | Concept: reset |
| 6 | A real reflog output and the recovery | Concept: reflog |
| 7 | Six real error messages from the troubleshooting labs | Failures you meet at work |
| 8 | Branch → PR → review → checks → merge → tag → Actions → GHCR → Helm → Kubernetes, with the real workflow result | The capstone |
| 9 | Tiles: lessons, assessments, labs, projects, videos, PDF | What is inside |
| 10 | A test annotation and the sandbox | Every command tested |
| 11 | QR codes to the course and the portfolio, and a question | Links |

## How to post

1. Create a post, choose **Add a document**, upload `carousel/carousel.pdf` and give it the title
   "Git & GitHub, from beginner to advanced".
2. Paste `post.md` as the text (the hashtags are at the end).
3. Reply to comments within the first hour.
