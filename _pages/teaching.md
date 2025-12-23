---
layout: page
permalink: /teaching/
title: teaching
description: Materials and courses.
nav: true
nav_order: 5
---


{% assign teaching = site.teaching | sort: 'date' | reverse %}

{% for post in teaching %}
<div class="card mt-3">
  <div class="card-body">
    <h3 class="card-title">
      {% if post.link %}
        <a href="{{ post.link }}">{{ post.title }}</a>
      {% else %}
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      {% endif %}
    </h3>
    
    <h6 class="card-subtitle mb-2 text-muted">
      {{ post.type }}
      {% if post.venue %}| {{ post.venue }}{% endif %}
      {% if post.date %}| {{ post.date | date: "%Y" }}{% endif %}
    </h6>

    <div class="card-text">
      {{ post.content | markdownify | truncatewords: 50 }}
    </div>
  </div>
</div>
{% endfor %}
