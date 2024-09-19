from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from websitescraping.scrape import thread_scrape

def home(request):
    year = datetime.now().year
    context = {
        'year': year,
    }
    return render(request, 'site/index.html', context)


def scrape_urls(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            try:
                scraped_urls = thread_scrape([url])
                response_data = {
                    'scraped_urls': scraped_urls,
                    'hour': datetime.now().strftime('%H:%M:%S'),
                    'date': datetime.now().strftime('%d/%m/%Y')
                }
                return JsonResponse(response_data)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'error': 'No URL provided'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
