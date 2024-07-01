---
title: "HeteroExcept: A CPU-GPU Heterogeneous Algorithm to Accelerate Exception-aware Static Timing Analysis"
authors:
- Zizheng Guo
- Zuodong Zhang
- Wuxi Li
- Tsung-Wei Huang
- Xizhe Shi
- admin
- Yibo Lin
- Runsheng Wang
- Ru Huang
date: "2024-02-26T00:00:00Z"
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: "2024-06-20T"

# Publication type.
# Accepts a single type but formatted as a YAML list (for Hugo requirements).
# Enter a publication type from the CSL standard.
publication_types: ["conference"]

# Publication name and optional abbreviated publication name.
publication: "International Conference on Computer-Aided Design (Accepted)"
publication_short: "ICCAD24 (Accepted)"

abstract: Static timing analysis (STA) for large-scale modern circuits requires extensive handling of false paths, multi-cycle paths, and other types of path exceptions. Despite the linear nature of timing propagation, we show that exception-aware STA is NP-hard and thus requires a long runtime to solve using conventional CPU-based methods. To overcome this runtime challenge, we propose a general CPU-GPU heterogeneous algorithm, HeteroExcept, that can handle common types of path exceptions and efficiently generate an accurate path report. Our algorithm targets runtime efficiency at the scale of thousands of exception rules and millions of circuit elements. To further improve the performance, we optimize our GPU implementation by introducing a cost-effective data exchange strategy between CPU and GPU. Experimental results demonstrate up to 6.84× and 12.93× speed-up compared to industrial timers, PrimeTime and penSTA.

# Summary. An optional shortened abstract.
#summary: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis posuere tellus ac convallis placerat. Proin tincidunt magna sed ex sollicitudin condimentum.

tags:
- Timing Analysis
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
