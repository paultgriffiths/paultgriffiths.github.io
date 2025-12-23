---
layout: page
permalink: /news/
title: news
description: 
nav: true
nav_order: 2
pagination:
  enabled: true
  collection: news
---

{% if site.news != blank %}
  {% assign news_size = site.news | size %}
  {% if news_size > 0 %}
    <div class="table-responsive">
      <table class="table table-sm table-borderless">
      {% assign news = site.news | reverse %}
      {% if page.pagination.enabled %}
        {% assign news = paginator.posts %}
      {% endif %}

      {% for item in news %}
        <tr>
          <th scope="row" style="width: 20%">{{ item.date | date: "%b %-d, %Y" }}</th>
          <td>
            {% if item.inline %}
              {{ item.content | remove: '<p>' | remove: '</p>' | emojify }}
            {% else %}
            <a class="news-title font-weight-bold" href="{{ item.url | relative_url }}">{{ item.title }}</a>
            <div class="news-excerpt text-muted mt-1">
              {{ item.excerpt }}
            </div>
          {% endif %}
          </td>
        </tr>
      {% endfor %}
      </table>
    </div>
  {% else %}
    <p>No news so far...</p>
  {% endif %}
{% endif %}

{% if page.pagination.enabled %}
  {% include pagination.liquid %}
{% endif %}
