---
title: "PowPrediCT: Cross-Stage Power Prediction with Circuit-Transformation-Aware Learning"
authors:
- admin †
- Zizheng Guo †
- Xun Jiang
- Zhuomin Chai
- Yuxiang Zhao
- Yibo Lin
- Runsheng Wang
- Ru Huang
date: "2024-02-26T00:00:00Z"
doi: "10.1145/3649329.3657349"

# Schedule page publish date (NOT publication's date).
publishDate: "2024-01-20T"

# Publication type.
# Accepts a single type but formatted as a YAML list (for Hugo requirements).
# Enter a publication type from the CSL standard.
publication_types: ["conference"]

# Publication name and optional abbreviated publication name.
publication: "Submitted to Design Automation Conference (Accepted)"
publication_short: "DAC24 (Accepted)"

abstract: Accurate and efficient power analysis at early VLSI design stages is critical for effective power optimization. It is a promising yet challenging task to model the circuit power at early design stages, especially during placement with the clock tree and final signal routing unavailable. Additionally, optimization-induced circuit transformations like circuit restructuring and gate sizing can invalidatefine-grained power supervision. Addressing these difficulties, we introduce the first circuit-transformation-aware power prediction model at placement stage with robust generalization capabilities. Our technology includes a dedicated clock tree model and an innovative train-and-calibrate scheme that effectively integrates topological and layout features. Compared to the cutting-edge commercial IC engine Innovus, we have significantly reduced the cross-stage power analysis error between placement and detailed routing.

# Summary. An optional shortened abstract.
#summary: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis posuere tellus ac convallis placerat. Proin tincidunt magna sed ex sollicitudin condimentum.

tags:
- Power Analysis
- ML for EDA
- GNNs
featured: false

links:
#- name: Custom Link
#  url: http://example.org
url_pdf: uploads/227_Camera_Ready_Paper.pdf
url_doi: https://doi.org/10.1145/3649329.3657349
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
