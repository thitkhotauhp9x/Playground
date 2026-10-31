from googleapiclient.discovery import build

API_KEY = "AIzaSyA-cJs0adrJ4FujsxzgrchZgAdlja8pFFg"
CSE_ID = "37704ba35f8774758"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res.get("items", [])

results = google_search("CV12", API_KEY, CSE_ID, num=10)
for result in results:
    print(result["title"], result["link"])