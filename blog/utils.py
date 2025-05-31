from bs4 import BeautifulSoup
from django.utils.safestring import mark_safe
from advert.models import AdCategory

def generate_ad_html(ad_banner):
    ad_html = ''
    if ad_banner.video:
        ad_html = f'''
            <div class="ad-banner-container">
                <a href="{ad_banner.link}" target="_blank" class="ad-video">
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
            <a href="https://maxonex-system.vercel.app/" target="_blank" style="display:inline-block;margin:0;padding:0;">
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


