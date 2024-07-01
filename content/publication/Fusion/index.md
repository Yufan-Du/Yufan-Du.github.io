---
title: "Fusion of Global Placement and Gate Sizing with Differentiable Optimization"
authors:
- admin
- Zizheng Guo
- Yibo Lin
- Runsheng Wang
- Ru Huang
date: "2024-2-26T"
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: "2024-6-20T"

# Publication type.
# Accepts a single type but formatted as a YAML list (for Hugo requirements).
# Enter a publication type from the CSL standard.
publication_types: ["conference"]

# Publication name and optional abbreviated publication name.
publication: "International Conference on ComputerAided Design (Accepted)"
publication_short: "ICCAD24 (Accepted)"

abstract: Gate sizing is critical in VLSI design because it significantly influ- ences final design quality. Traditional design flows typically treat gate sizing as a separate step due to its discreteness nature. How- ever, this approach not only undermines the optimization efforts of earlier stages like placement and routing, but also restricts the exploration space for gate sizing. To address these challenges, we introduce an innovative design flow that fuses gate sizing with the earlier global placement stage. Our method employs differentiable timing and leakage power objectives and leverages GPU-accelerated computation to enhance design quality directly and efficiently. Our experimental results demonstrate significant improvements in tim- ing and power metrics, with an average improvement of 77.1% in total negative slack (TNS) and 43.5% in worst negative slack (WNS), and meanwhile achieving a reduction in leakage power consump- tion by 1% in comparison with one of the most popular design tools, OpenROAD. Our method can accelerate the design process by up to 7×.

# Summary. An optional shortened abstract.
#summary: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis posuere tellus ac convallis placerat. Proin tincidunt magna sed ex sollicitudin condimentum.

tags:
- Optimization
featured: false

#links:
#- name: Custom Link
#  url: http://example.org
#url_pdf: http://arxiv.org/pdf/1512.04133v1
#url_code: 'https://github.com/HugoBlox/hugo-blox-builder'
#url_dataset: '#'
#url_poster: '#'
#url_project: ''
#url_slides: ''
#url_source: '#'
#url_video: '#'

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
image:
  caption: 'Algo Demo'
  focal_point: ""
  preview_only: false

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `internal-project` references `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
projects:
- internal-project

# Slides (optional).
#   Associate this publication with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides: "example"` references `content/slides/example/index.md`.
#   Otherwise, set `slides: ""`.
#slides: example
---

More Rich formatting such as including [code, math, and images](https://docs.hugoblox.com/content/writing-markdown-latex/) will be included here.
