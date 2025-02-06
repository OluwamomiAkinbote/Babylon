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
