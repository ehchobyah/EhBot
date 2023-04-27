{%- if reply %}```{{reply}}```{% endif %}
{%- if sender -%}{{sender}}: {% endif %}{{content}}
{# дальше идут файлы #}
{%- if attachments -%}
  {% for attachment in attachments %}
    {{- attachment+"\n" -}}
  {% endfor %}
{% endif %}

