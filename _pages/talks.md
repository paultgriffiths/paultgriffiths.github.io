---
layout: page
permalink: /talks/
title: talks
description: Locations where I have given seminars and talks.
nav: true
nav_order: 4
---

<div id="talks-map" style="height: 500px; width: 100%; z-index: 1; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></div>

<div class="mt-4">
    <h3>talks List</h3>
    <div class="table-responsive">
        <table class="table table-sm table-borderless">
            {% for talk in site.data.talks_locations reversed %}
            <tr>
                <th scope="row" style="width: 15%;">{{ talk.year }}</th>
                <td>
                    <strong>{{ talk.title }}</strong>
                    {% if talk.description %}
                    <br>
                    <span style="font-size: 0.95em; color: #555;">{{ talk.description }}</span>
                    {% endif %}
                    <br>
                    <span class="text-muted"><i class="fas fa-map-marker-alt"></i> {{ talk.name }}</span>
                </td>
                <td style="text-align: right;">
                    {% if talk.url %}
                    <a href="{{ talk.url | relative_url }}" class="btn btn-sm z-depth-0" role="button">Page</a>
                    {% endif %}
                    {% if talk.pdf %}
                    <a href="{{ talk.pdf | relative_url }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="color: #d9230f;"><i class="fas fa-file-pdf"></i> PDF</a>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
</div>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

<script>
    var map = L.map('talks-map').setView([30.0, 10.0], 2);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    var talks = [
        {% for talk in site.data.talks_locations %}
        {
            "name": "{{ talk.name }}",
            "lat": {{ talk.lat }},
            "lng": {{ talk.lng }},
            "title": "{{ talk.title }}",
            "year": "{{ talk.year }}",
            "url": "{% if talk.url %}{{ talk.url | relative_url }}{% endif %}",
            "pdf": "{% if talk.pdf %}{{ talk.pdf | relative_url }}{% endif %}"
        }{% unless forloop.last %},{% endunless %}
        {% endfor %}
    ];

    talks.forEach(function(t) {
        var popupContent = "<b>" + t.title + " (" + t.year + ")</b><br>" + t.name + "<br><br>";
        
        if (t.url) {
            popupContent += '<a href="' + t.url + '" style="margin-right: 10px;">View Page</a>';
        }
        if (t.pdf) {
            popupContent += '<a href="' + t.pdf + '" target="_blank">Download PDF</a>';
        }

        var marker = L.marker([t.lat, t.lng]).addTo(map);
        marker.bindPopup(popupContent);
    });
</script>