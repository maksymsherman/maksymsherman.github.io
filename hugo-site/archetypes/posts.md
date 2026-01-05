---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
description: "Brief summary of the post (max 160 characters)"
---

<h1>{{ replace .Name "-" " " | title }}</h1>
<h5><time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date.Format "January 2nd, 2006" }}</time></h5>

<p>Your content here...</p>
