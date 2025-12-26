---
layout: page
permalink: /talks/
title: talks
description: Seminars, talks and meetings
nav: true
nav_order: 4
---

<div id="talks-map" style="height: 500px; width: 100%; z-index: 1; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></div>

<div class="mt-4">
    <h3>Seminars and meetings</h3>
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

    // 1. Define the Custom Icons
    var blueIcon = new L.Icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    var redIcon = new L.Icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    // 2. Load Data from Jekyll
    var talks = [
        {% for talk in site.data.talks_locations %}
        {
            "name": "{{ talk.name }}",
            "lat": {{ talk.lat }},
            "lng": {{ talk.lng }},
            "category": "{{ talk.category }}", 
            "title": "{{ talk.title }}",
            "year": "{{ talk.year }}",
            "url": "{% if talk.url %}{{ talk.url | relative_url }}{% endif %}",
            "pdf": "{% if talk.pdf %}{{ talk.pdf | relative_url }}{% endif %}"
        }{% unless forloop.last %},{% endunless %}
        {% endfor %}
    ];

    // 3. Loop and Assign Icons
    talks.forEach(function(t) {
        var popupContent = "<b>" + t.title + " (" + t.year + ")</b><br>" + t.name + "<br><br>";
        
        if (t.url) {
            popupContent += '<a href="' + t.url + '" style="margin-right: 10px;">View Page</a>';
        }
        if (t.pdf) {
            popupContent += '<a href="' + t.pdf + '" target="_blank">Download PDF</a>';
        }

        var chosenIcon = blueIcon; // Default (Seminar/Talk)
        if (t.category === 'meeting') {
            chosenIcon = redIcon;
        }

        var marker = L.marker([t.lat, t.lng], {icon: chosenIcon}).addTo(map);
        marker.bindPopup(popupContent);
    });

    // 4. Create the Legend
    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend');
        
        // Inline CSS for the legend box
        div.style.backgroundColor = "white";
        div.style.padding = "10px";
        div.style.border = "1px solid #ccc";
        div.style.borderRadius = "5px";
        div.style.boxShadow = "0 0 15px rgba(0,0,0,0.2)";
        div.style.fontSize = "14px";
        div.style.lineHeight = "20px";

        // Legend HTML content
        // We use the same image URLs as the markers but scale them down (height="20")
        div.innerHTML += '<div style="margin-bottom: 5px;"><img src="https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png" height="20" style="vertical-align: middle;"> <b>Conference</b></div>';
        div.innerHTML += '<div><img src="https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png" height="20" style="vertical-align: middle;"> <b>Seminar / Talk</b></div>';
        
        return div;
    };

    legend.addTo(map);
</script>
