---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
description: "Brief summary of the post (max 160 characters)"
---

# {{ replace .Name "-" " " | title }}

##### <time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date.Format "January 2nd, 2006" }}</time>

Your content here...
