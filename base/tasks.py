from celery import shared_task
from PIL import Image, ImageDraw, ImageFont

from .models import Country, CountryMeta

@shared_task
def create_summary_image():
    c_meta = CountryMeta.objects.first()
    top_countries = Country.objects.order_by('-estimated_gdp')[:5]
    
    img = Image.new('RGB', (1000, 400), color='white')
    draw = ImageDraw.Draw(img)
    default_font = ImageFont.load_default()
    try:
        font_bold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size=20)
    except OSError:
        font_bold = default_font
    
    try:
        font_regular = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', size=18)
    except OSError:
        font_regular = default_font
    
    try:
        font_italic = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/UbuntuSans-Italic[wdth,wght].ttf', size=16)    
    except OSError:
        font_italic = default_font
        
    countries = []
    for i, c in enumerate(top_countries, 1):
        countries.append(
            (f"    {i}. {c.name} - {c.estimated_gdp}", font_regular, 'black')
        )
    
    lr = c_meta.last_refreshed_at.strftime("%b %d, %Y, %-I:%M%p")
    segments = [
        (f"Total Number of Countries: {c_meta.total_countries}", font_bold, 'black'),
        ("Top 5 Countries By Estimated GDP", font_bold, 'black'),
        *countries,
        (f"\nLast refreshed at: {lr}", font_italic, 'gray')
    ]
    x, y = 50, 80
    for text, font, color in segments:
        for line in text.split('\n'):
            if not line.strip():
                y += font.size
                continue
            draw.text((x, y), text, font=font, fill=color)
            y += font.size + 4

    from django.conf import settings
    path = settings.BASE_DIR / 'cache'
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    img.save(path / 'summary.png')