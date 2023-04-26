{{sender}} {%- if brackets -%}({{brackets[0]}}:{{brackets[1]}}){% endif %}: {{content}}
{# дальше идут файлы #}
{%- if attachments -%}
  {% for attachment in attachments %}
    {{- attachment+"\n" -}}
  {% endfor %}
{% endif %}

