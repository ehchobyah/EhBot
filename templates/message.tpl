{%- if reply %}```{{reply}}```{% endif %}
{%- if sender -%}{{sender}}: {% endif %}{{content}}
{%- if attachments -%}
  {%- for attachment in attachments -%}
    {{- '\n'+attachment -}}
  {% endfor %}
{% endif %}

