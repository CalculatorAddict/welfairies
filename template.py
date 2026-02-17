# -------------------------
# HTML template
# -------------------------

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {
    font-family: "Comic Sans MS", "Comic Sans", sans-serif;
}

/* Each person is its own page flow */
.person {
    page-break-after: always;
}

/* Header repeats on overflow pages */
.header {
    position: running(header);
    font-size: 16pt;
    font-weight: bold;
    margin-top: 12px;
    margin-bottom: 8px;
    vertical-align: bottom;
}

.footer {
    position: running(footer);
    font-size: 12pt;
    margin-top: 12px;
    margin-bottom: 8px;
    vertical-align: bottom;
}

@page {    
    size: A6 landscape;
    margin: 1cm;
    @top-center {
        content: element(header);
    }
}

.name-line {
    position: relative;
    text-align: center;
    margin-bottom: 6px;
    font-weight: bold;
    font-size: 14pt;
}

.fairy-fill {
    display: block;
    white-space: nowrap;
    overflow: hidden;
    font-size: 12pt;
}

.name-text {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    background: white;      /* hides fairies behind text */
    padding: 0 6px;
}


.note {
    margin-bottom: 4px;
    font-size: 10pt;
}

.candy {
    margin-top: 8px;
    border-top: 1px solid #000;
    padding-top: 5px;
    font-size: 9pt;
    text-align: center;
}

ul {
    padding-left: 15px;
}

</style>
</head>
<body>

{% for person in people %}
<div class="person">

    <div class="header">
        🧚 {{ person.name }} 🧚
    </div>

    <ul>
    {% for note in person.notes %}
        <li><div class="note">{{ note }}</div></li>
    {% endfor %}
    </ul>

    <div class="candy">
        😋
        {% for candy, count in person.candy_counts.items() %}
            {{ candy }}: {{ count }} {% if loop.index< person.candy_counts.items() | length %} &emsp; {% endif %}
        {% endfor %}
        😋
    </div>

</div>
{% endfor %}

</body>
</html>
"""