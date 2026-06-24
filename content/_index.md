---
# Leave the homepage title empty to use the site title
title: ''
date: 2022-10-24
type: landing

sections:
  - block: about.biography
    id: about
    content:
      title: Biography
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin

  - block: experience
    content:
      title: Experience
      # Date format for experience
      #   Refer to https://docs.hugoblox.com/customization/#date-format
      date_format: Jan 2006
      items:
        - title: Applied Scientist Intern
          company: Amazon Web Services (AWS)
          company_url: https://aws.amazon.com/
          company_logo: aws
          location: San Jose, California, United States
          date_start: '2026-06-01'
          date_end: ''
          description: |2-
            Multi-node, multi-GPU LLM serving optimization.
            Manager: Yida Wang.
        - title: Undergraduate Research Assistant
          company: The University of Texas at Austin
          company_url: https://www.utexas.edu/
          company_logo: utexas
          location: Austin, Texas, United States
          date_start: '2024-06-01'
          date_end: '2024-09-01'
          description: Differentiable chip physical design algorithm optimization.
    design:
      columns: '1'

  - block: collection
    id: featured
    content:
      title: Recent Publications
      filters:
        folders:
          - publication
        exclude_featured: true
    design:
      columns: '2'
      view: citation

  - block: portfolio
    id: posts
    content:
      title: Posts
      filters:
        folders:
          - post
    design:
      columns: '1'
      view: showcase
      flip_alt_rows: false

  - block: contact
    id: contact
    content:
      title: Contact
      email: nbsdyf at hotmail dot com
    design:
      columns: '2'

---
