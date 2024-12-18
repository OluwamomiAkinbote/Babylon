from bs4 import BeautifulSoup
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def first_letter_richtext(content):
    soup = BeautifulSoup(content, 'html.parser')

    if soup.p:
        first_letter = soup.p.text[0]
        rest_of_content = soup.p.text[1:]

        soup.p.string = ''  # Clear the text inside <p>
        soup.p.append(BeautifulSoup(f'<span class="first-letter">{first_letter}</span>{rest_of_content}', 'html.parser'))

    return mark_safe(str(soup))






