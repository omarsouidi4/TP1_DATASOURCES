from flask import Flask, request, redirect, session, render_template_string, url_for
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import requests
import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = os.urandom(24)


CLIENT_SECRETS_FILE = "C:\\Users\\omars\\OneDrive\\Bureau\\EPF 5A\\DATA_SOURCES\\json.json"

REDIRECT_URI = 'http://localhost:5000/callback'
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

@app.route('/')
def hello_world():
    variable = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TP5LRMBZ8T"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-TP5LRMBZ8T');
</script>"""
    return "<p>ALLEZ L'OM!</p>" + variable + '<a href="/login">Login with Google</a>'

@app.route('/login')
def login():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, 
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    
    session['state'] = state

    return redirect(authorization_url)

@app.route('/callback')
def callback():
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, 
        scopes=SCOPES, 
        state=state,
        redirect_uri=REDIRECT_URI
    )

    flow.fetch_token(authorization_response=request.url)

    
    creds_data = {
    'token': flow.credentials.token,
    'refresh_token': flow.credentials.refresh_token,
    'token_uri': flow.credentials.token_uri,
    'client_id': flow.credentials.client_id,
    'client_secret': flow.credentials.client_secret,
    'scopes': flow.credentials.scopes
    }
    session['credentials'] = creds_data


    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    

    return 'Logged in successfully.'

@app.route('/logger', methods=['GET', 'POST'])
def logger():
    if request.method == 'POST':
        log_mess = request.form.get('log_mess', 'No message provided')
        app.logger.info(log_mess)
        log_browser = f'<script>console.log("Log message from browser: {log_mess}");</script>'
        return log_browser + 'Logged Successfully! <a href="/logger">Go Back</a>'

    return render_template_string('''
    <form method="POST">
        Log Message: <input type="text" name="log_mess">
        <input type="submit" value="Log">
    </form>
    ''')

@app.route("/google_request")
def google_request():
    req = requests.get("https://www.google.com/")
    return req.cookies.get_dict()

@app.route('/fetch-analytics', methods=['GET'])
def fetch_google_analytics_data():

  
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\omars\\OneDrive\\Bureau\\EPF 5A\\DATA_SOURCES\\TP1\\myproject\\datasourcestp2-0a48555e151c.json'
    PROPERTY_ID = '364259683'
    starting_date = "8daysAgo"
    ending_date = "yesterday"

    client = BetaAnalyticsDataClient()
    def get_visitor_count(client, property_id):
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[{"start_date": starting_date, "end_date": ending_date}],
            metrics=[{"name": "activeUsers"}]
        )

        response = client.run_report(request)
        return response

    response = get_visitor_count(client, PROPERTY_ID)

    if response and response.row_count > 0:
        metric_value = response.rows[0].metric_values[0].value
    else:
        metric_value = "N/A"  

    return f'Number of visitors : {metric_value}'

if __name__ == '__main__':
    app.run(debug=True)
