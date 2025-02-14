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

  - block: collection
    id: featured
    content:
      title: Recent Publications
      #text: |-
      #  {{% callout note %}}
      #  Quickly discover relevant content by [filtering publications](./publication/).
      #  {{% /callout %}}
      filters:
        folders:
          - publication
        exclude_featured: true
    design:
      columns: '2'
      view: citation

#  - block: portfolio
#    id: posts
#    content:
#      title: Posts
#      filters:
#        folders:
#          - post
#    design:
      # Choose how many columns the section has. Valid values: '1' or '2'.
#      columns: '1'
#      view: showcase
      # For Showcase view, flip alternate rows?
#      flip_alt_rows: false

#  - block: portfolio
#    id: projects
#    content:
#      title: Projects
#      filters:
#        folders:
#          - project
      # Default filter index (e.g. 0 corresponds to the first `filter_button` instance below).
#      default_button_index: 0
      # Filter toolbar (optional).
      # Add or remove as many filters (`filter_button` instances) as you like.
      # To show all items, set `tag` to "*".
      # To filter by a specific tag, set `tag` to an existing tag name.
      # To remove the toolbar, delete the entire `filter_button` block.
      #buttons:
      #  - name: All
      #  - name: All
      #    tag: '*'
      #  - name: Artificial Intelligence
      #    tag: Artificial Intelligence
      #  - name: Hardware Design
      #    tag: Hardware Design
      #  - name: Other
      #    tag: Demo
#    design:
      # Choose how many columns the section has. Valid values: '1' or '2'.
#      columns: '1'
#      view: showcase
      # For Showcase view, flip alternate rows?
#      flip_alt_rows: false
    
#  - block: portfolio
#    id: researches
#    content:
#      title: Researches
#      filters:
#        folders:
#          - research
      # Default filter index (e.g. 0 corresponds to the first `filter_button` instance below).
#      default_button_index: 0
      # Filter toolbar (optional).
      # Add or remove as many filters (`filter_button` instances) as you like.
      # To show all items, set `tag` to "*".
      # To filter by a specific tag, set `tag` to an existing tag name.
      # To remove the toolbar, delete the entire `filter_button` block.
#      buttons:
#        - name: All
#          tag: '*'
      #  - name: Other
      #    tag: Demo
#    design:
      # Choose how many columns the section has. Valid values: '1' or '2'.
#      columns: '1'
#      view: showcase
      # For Showcase view, flip alternate rows?
#      flip_alt_rows: false



  - block: contact
    id: contact
    content:
      title: Contact
      #subtitle:
      #text: |-
      #  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam mi diam, venenatis ut magna et, vehicula efficitur enim.
      # Contact (add or remove contact options as necessary)
      email: nbsdyf at hotmail dot com
      # Choose a map provider in `params.yaml` to show a map from these coordinates
      #coordinates:
      #  latitude: '37.4275'
      #  longitude: '-122.1697'  
      #contact_links:
      # Automatically link email and phone or display as text?
      #autolink: true
      # Email form provider
      #form:
      #  provider: netlify
      #  formspree:
      #    id:
      #  netlify:
          # Enable CAPTCHA challenge to reduce spam?
       #   captcha: false
    design:
      columns: '2'

---
