import requests, json
from flask import Flask, render_template, request
from webScraper.courtScraper import fetch_case_data
from database.models import Base, engine, SessionLocal, QueryLog
from bs4 import BeautifulSoup

app = Flask(__name__)

Base.metadata.create_all(bind=engine)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        case_type = request.form['case_type']
        case_number = request.form['case_number']
        filing_year = request.form['filing_year']

        session = SessionLocal()

        try:
            result = fetch_case_data(case_type, case_number, filing_year)

            query_text = f"{case_type}/{case_number}/{filing_year}"
            raw_response = json.dumps(result['data'])

            log_entry = QueryLog(query_text=query_text, raw_response=raw_response)
            session.add(log_entry)
            session.commit()

            return render_template('result.html', data=result["data"])
        except Exception as e:
            return render_template('result.html', error=str(e))
    
    try:
        URL = "https://delhihighcourt.nic.in/app/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        caseYears = [opt['value'] for opt in soup.select('select#year option') if opt['value']]
        caseTypes = [opt['value'] for opt in soup.select('select#case_type option') if opt['value'].strip()]

        return render_template('index.html', case_types=caseTypes, case_years=caseYears)
    except Exception as e:
        return render_template('index.html', case_types=[], case_years=[], error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
