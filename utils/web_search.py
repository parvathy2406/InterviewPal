import os, requests

SERPAPI_KEY = os.getenv('SERPAPI_KEY', '')

def serpapi_search(query, num=3):
    if not SERPAPI_KEY:
        return []
    params = {
        'engine': 'google',
        'q': query,
        'api_key': SERPAPI_KEY,
        'num': num
    }
    try:
        resp = requests.get('https://serpapi.com/search', params=params, timeout=8).json()
        results = []
        for r in resp.get('organic_results', [])[:num]:
            results.append({
                'title': r.get('title'),
                'snippet': r.get('snippet'),
                'link': r.get('link')
            })
        return results
    except Exception as e:
        return [{'title': 'search failed', 'snippet': str(e), 'link': ''}]
