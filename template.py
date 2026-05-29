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

@page {
    size: A6 landscape;
    margin: 1cm;
    @top-center {
        content: element(header);
    }
    @bottom-center {
        content: element(footer);
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

.snack-count {
    font-size: 10pt;
    font-weight: normal;
    margin-left: 8px;
    color: #555;
}

.footer {
    position: running(footer);
    font-size: 10pt;
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

    <div class="footer">
        {{ term_name }} &emsp;🏴󠁧󠁢󠁷󠁬󠁳󠁿&emsp; {{ welsh_phrase }} &emsp;🏴󠁧󠁢󠁷󠁬󠁳󠁿&emsp;{% if person.snack_c or person.snack_s %} {{ person.snack_c }}C; {{ person.snack_s }}S{% endif %}
    </div>

    <div class="header">
        🧚 {{ person.name }} 🧚
    </div>

    <ul>
    {% for note in person.notes %}
        <li><div class="note">{{ note }}</div></li>
    {% endfor %}
    </ul>

</div>
{% endfor %}

</body>
</html>
"""