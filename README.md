# Delhi High Court Data Web Scraper

This project is a web application for fetching case details from the **Delhi High Court** website using web scraping techniques. It provides a user-friendly interface to search for case information by case type, number, and filing year.

---

## Court Chosen

- **Delhi High Court**  
  The application is specifically designed to fetch and display case data from the official Delhi High Court website.

---

## Setup Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/delhiCourtData-WebScrapping.git
   cd delhiCourtData-WebScrapping
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python3 -m venv venv
   
   # On Mac:
   source venv/bin/activate  

   # On Windows: 
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   flask run --debug
   ```
   The app will be available at [http://localhost:5000](http://localhost:5000).

---

## CAPTCHA Strategy

- **Current Approach:**  
  The Delhi High Court website uses a simple image-based CAPTCHA.  
  This project does **not** attempt to bypass or solve the CAPTCHA automatically.  
  Instead, the application is designed to work with endpoints or flows that do not require CAPTCHA, or it may prompt the user to solve the CAPTCHA manually if required.

- **Note:**  
  If the CAPTCHA becomes a blocking issue, you may need to manually solve it in the browser or explore legal and ethical alternatives.  
  **Automated CAPTCHA solving is not implemented in this project.**

---

## Directory Structure

``` bash
# This is the directory structure after setup
delhiCourtData-WebScrapping/
├── venv/
├── templates/
│   ├── index.html
│   └── result.html
├── webScraper/
│   ├── court-details-scraping.ipynb
│   └── courtScraper.py
├── app.py
├── requirements.txt
├── LICENSE
└── README.md
```