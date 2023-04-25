import streamlit as st
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Setzen Sie hier Ihre OAuth 2.0-Anmeldeinformationen ein
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "your_redirect_uri"

# OAuth 2.0 Flow
flow = InstalledAppFlow.from_client_info({
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uris": [REDIRECT_URI],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
    }
}, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])

# App Header
st.title("Google Search Console URL Index Checker")

# Textarea for input URLs
input_urls = st.text_area("Geben Sie die URLs ein, die überprüft werden sollen (eine URL pro Zeile):", height=200)

# Check URLs button
check_urls_button = st.button("Überprüfe URLs")

# Function to check if a URL is indexed
def is_url_indexed(service, url):
    response = service.urlInspection().get(url=url).execute()
    return response.get("indexStatus") == "URL_IS_ON_GOOGLE"

# Main app logic
if check_urls_button:
    if input_urls.strip():
        urls = input_urls.strip().split("\n")
        indexed_urls = []

        try:
            credentials = flow.run_local_server(port=0)
            service = build("searchconsole", "v1", credentials=credentials)

            for url in urls:
                if is_url_indexed(service, url):
                    indexed_urls.append(url)

            if indexed_urls:
                st.write("Die folgenden URLs sind indexiert:")
                st.write(indexed_urls)
            else:
                st.write("Keine der eingegebenen URLs ist indexiert.")
        except Exception as e:
            st.write("Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.")
            st.write(str(e))
    else:
        st.write("Bitte geben Sie die URLs ein, die überprüft werden sollen.")
