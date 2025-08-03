import requests, re, sys
from bs4 import BeautifulSoup
from utils.exception import CustomException

def fetch_case_data(case_type, case_number, filing_year):
    try:
        session = requests.Session()

        URL = "https://delhihighcourt.nic.in/app"
        home_res = session.get(URL)
        home_res.raise_for_status()
        soup = BeautifulSoup(home_res.text, "html.parser")

        scripts = soup.find_all("script")
        token = None
        for script in scripts:
            if script.string and "_token" in script.string:
                match = re.search(r'"_token"\s*:\s*"([^"]+)"', script.string)
                if match:
                    token = match.group(1)
                    break
        if not token:
            raise Exception("CSRF token not found.")

        captcha_span = soup.find('span', class_='captcha-code')
        if not captcha_span:
            raise Exception("Captcha code not found on the page.")
        captchaCode = captcha_span.text.strip()

        captcha_response = session.post(
            "https://delhihighcourt.nic.in/app/validateCaptcha",
            data={
                "_token": token,
                "captchaInput": captchaCode
            }
        )
        captcha_response.raise_for_status()
        captcha_json = captcha_response.json()

        if captcha_json.get("success"):
            headers = {
                "Referer": "https://delhihighcourt.nic.in/app/sitting-judge-wise",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0",
            }

            params = {
                "draw": 1,
                "columns[0][data]": "DT_RowIndex",
                "columns[0][name]": "DT_RowIndex",
                "columns[0][searchable]": "true",
                "columns[0][orderable]": "false",
                "columns[0][search][value]": "",
                "columns[0][search][regex]": "false",
                "columns[1][data]": "case_no_order_link",
                "columns[1][name]": "case_no_order_link",
                "columns[1][searchable]": "true",
                "columns[1][orderable]": "true",
                "columns[1][search][value]": "",
                "columns[1][search][regex]": "false",
                "columns[2][data][_]" : "order_date.display",
                "columns[2][data][sort]" : "order_date.timestamp",
                "columns[2][name]": "order_date.timestamp",
                "columns[2][searchable]": "true",
                "columns[2][orderable]": "true",
                "columns[2][search][value]": "",
                "columns[2][search][regex]": "false",
                "columns[3][data]": "corrigendum",
                "columns[3][name]": "corrigendum",
                "columns[3][searchable]": "true",
                "columns[3][orderable]": "true",
                "columns[3][search][value]": "",
                "columns[3][search][regex]": "false",
                "columns[4][data]": "hindi_order",
                "columns[4][name]": "hindi_order",
                "columns[4][searchable]": "true",
                "columns[4][orderable]": "true",
                "columns[4][search][value]": "",
                "columns[4][search][regex]": "false",
                "order[0][column]": 0,
                "order[0][dir]": "asc",
                "order[0][name]": "DT_RowIndex",
                "start": 0,
                "length": 50,
                "case_type": case_type,       # Fill if needed
                "case_number": case_number,     # Fill if needed
                "year": filing_year,            # Fill if needed
            }
            
            r = requests.get(URL, headers=headers, params=params)
            return r.json()
        else:
            print("❌ CAPTCHA failed")

        return 'done'
    except Exception as e:
        raise CustomException(e, sys)
