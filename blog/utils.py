from bs4 import BeautifulSoup
from django.utils.safestring import mark_safe
from advert.models import AdCategory
import re
import spacy


def generate_ad_html(ad_banner):
    ad_html = ''
    if ad_banner.video:
        ad_html = f'''
            <div class="ad-banner-container">
                <a href="{ad_banner.link}" rel="sponsored" target="_blank" class="ad-video">
                    <video autoplay muted loop class="ad-video-element">
                        <source src="{ad_banner.video.url}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                </a>
            </div>
        '''
    else:
        image_large_url = ad_banner.image_large.url if ad_banner.image_large else ''
        image_small_url = ad_banner.image_small.url if ad_banner.image_small else ''
        
        ad_html = f'''
            <div class="ad-banner-container flex justify-center items-center overflow-hidden w-70 h">
                <a href="{ad_banner.link}" target="_blank" class="ad-image">
                    <picture>
                        <source srcset="{image_large_url}" media="(min-width: 768px)">
                        <source srcset="{image_small_url}" media="(min-width: 448px)">
                        <img src="{image_small_url}" alt="Ad Banner" class="ad-image-element">
                    </picture>
                </a>
            </div>
        '''
    return mark_safe(ad_html)

def insert_ad_banner(content, ads):
    soup = BeautifulSoup(content, 'html.parser')
    paragraphs = soup.find_all('p')

    for ad_banner in ads:
        if ad_banner.category == AdCategory.INLINE and ad_banner.active:  # Ensure only active inline ads
            ad_html = generate_ad_html(ad_banner)
            positions = ad_banner.paragraph_positions
            
            if isinstance(positions, int):
                positions = [positions]
            elif not isinstance(positions, (list, tuple)):
                print(f"Unexpected type for positions: {type(positions)}")
                continue

            for position in sorted(positions, reverse=True):
                if position > 0 and position <= len(paragraphs):
                    target_paragraph = paragraphs[position - 1]
                    ad_soup = BeautifulSoup(ad_html, 'html.parser')
                    target_paragraph.insert_after(ad_soup)

    return str(soup)



def inject_banner(html_content):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_content, "html.parser")
    paragraphs = soup.find_all('p')

    if len(paragraphs) >= 2:
        # Create banner HTML with centered image and small spacing
        banner_html = '''
        <div class="web-banner" style="margin:5px auto;padding:0;line-height:0;text-align:center;">
            <a href="https://maxonex-system.vercel.app/" rel="sponsored" target="_blank" style="display:inline-block;margin:0;padding:0;">
                <img src="https://boltzmann.s3.us-east-1.amazonaws.com/Abstract/Inline-web-banner.png" 
                     alt="Ad Banner" 
                     style="display:block;max-width:100%;height:auto;margin:0 auto;padding:0;border:0;">
            </a>
        </div>
        '''.strip()

        # Parse the banner HTML
        banner_soup = BeautifulSoup(banner_html, "html.parser")
        banner_div = banner_soup.find('div')
        
        if not banner_div:
            return str(soup)  # Return original if banner couldn't be created

        # Insert after the target paragraph
        target_paragraph = paragraphs[1]
        target_paragraph.insert_after(banner_div)

        # Clean up surrounding whitespace (safer method)
        for sibling in [banner_div.next_sibling, banner_div.previous_sibling]:
            if sibling and isinstance(sibling, str) and sibling.strip() == '':
                sibling.extract()

    return str(soup)



# Load SpaCy model (load this once at module level)
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text, min_keywords=3, max_keywords=10):
    """Extract important keywords using SpaCy with minimum keyword guarantee"""
    doc = nlp(text)
    keywords = []
    
    # First pass: Extract nouns and proper nouns
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop:
            keywords.append(token.text)
    
    # Get unique keywords sorted by frequency
    keyword_counts = {}
    for kw in keywords:
        keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
    
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
    result_keywords = [kw[0] for kw in sorted_keywords[:max_keywords]]
    
    # If we don't have enough keywords, fall back to important words
    if len(result_keywords) < min_keywords:
        fallback_words = [token.text for token in doc 
                         if not token.is_stop 
                         and not token.is_punct 
                         and len(token.text) > 2]
        
        # Add unique fallback words until we reach min_keywords
        for word in fallback_words:
            if word not in result_keywords:
                result_keywords.append(word)
                if len(result_keywords) >= min_keywords:
                    break
    
    return result_keywords[:max_keywords]

def inject_internal_links(content_html, current_post, related_posts, max_links=10, readmore_links=2):
    soup = BeautifulSoup(content_html, 'html.parser')
    links_added = 0
    used_keywords = set()

    # Process keyword-based links first (existing functionality)
    for related in related_posts:
        if links_added >= max_links:
            break

        keywords = extract_keywords(related.title)
        if not keywords:
            continue

        try:
            url = related.get_absolute_url()
            if not url:
                continue
        except Exception:
            continue

        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            if len(keyword) < 3 or keyword_lower in used_keywords:
                continue

            for text_node in soup.find_all(string=True):
                if links_added >= max_links:
                    break

                parent = text_node.parent
                if parent.name == 'a' or not text_node.strip():
                    continue

                pattern = re.compile(rf'\b{re.escape(keyword)}\b', flags=re.IGNORECASE)
                if pattern.search(text_node):
                    link_html = f'<a href="{url}" style="color: green; text-decoration: underline;">{keyword}</a>'
                    new_text = pattern.sub(link_html, text_node, count=1)
                    new_soup = BeautifulSoup(new_text, 'html.parser')
                    text_node.replace_with(new_soup)
                    
                    links_added += 1
                    used_keywords.add(keyword_lower)
                    break

    # Add READ MORE section to second-to-last paragraph
    paragraphs = soup.find_all('p')
    if len(paragraphs) >= 2 and readmore_links > 0:
        # Get the most relevant related posts
        relevant_posts = sorted(
            related_posts,
            key=lambda p: len(set(extract_keywords(p.title)) & set(extract_keywords(current_post.title))),
            reverse=True
        )[:readmore_links]

        # Create the READ MORE section
        readmore_div = soup.new_tag('div', style="margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-left: 4px solid green;")
        readmore_title = soup.new_tag('h3', style="margin-top: 0; color: #2c3e50;")
        readmore_title.string = "READ MORE"
        readmore_div.append(readmore_title)

        ul = soup.new_tag('ul', style="list-style-type: none; padding-left: 0;")
        
        for post in relevant_posts:
            li = soup.new_tag('li', style="margin-bottom: 8px;")
            a = soup.new_tag('a', href=post.get_absolute_url(), style="color: green; text-decoration: underline;")
            a.string = post.title
            li.append(a)
            ul.append(li)
        
        readmore_div.append(ul)

        # Insert before last paragraph
        paragraphs[-2].insert_after(readmore_div)

    return str(soup)
