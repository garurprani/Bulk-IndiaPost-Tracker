import requests
from bs4 import BeautifulSoup
import re

def track_india_post_consignment(tracking_number):
    url = "https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/trackconsignment.aspx"
    
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "www.indiapost.gov.in",
        "Origin": "https://www.indiapost.gov.in",
        "Referer": "https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/trackconsignment.aspx",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "X-MicrosoftAjax": "Delta=true",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    payload = {
        "ctl00$ScriptManager": "",
        "__REQUESTDIGEST": "",
        "__VIEWSTATE": "",
        "__VIEWSTATEGENERATOR": "",
        "__EVENTVALIDATION": "",
        "ctl00$PlaceHolderMain$ucNewLegacyControl$txtOrignlPgTranNo": tracking_number,
        "ctl00$PlaceHolderMain$ucNewLegacyControl$ucCaptcha1$txtCaptcha": "2",
        "__ASYNCPOST": "true",
        "ctl00$PlaceHolderMain$ucNewLegacyControl$btnSearch": "Search"
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        
        # Parse the response
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract basic consignment info
        consignment_number = soup.find(id="ctl00_PlaceHolderMain_ucNewLegacyControl_txtHomePgTranNo")['value']
        current_status = soup.find(id="ctl00_PlaceHolderMain_ucNewLegacyControl_lblInternationalCurrentstatusOER").text
        
        print(f"\nConsignment Number: {consignment_number}")
        print(f"Current Status: {current_status.replace('Current Status : ', '')}")
        print("\nBooking Details:")
        
        # Extract booking details table
        booking_table = soup.find('table', {'id': 'ctl00_PlaceHolderMain_ucNewLegacyControl_gvInternationalArticleTrackDetailsOER'})
        if booking_table:
            rows = booking_table.find_all('tr')
            headers = [th.text.strip() for th in rows[0].find_all('th')]
            data = [td.text.strip() for td in rows[1].find_all('td')]
            
            for header, value in zip(headers, data):
                print(f"{header}: {value}")
        
        # Extract event details
        print("\nEvent History:")
        events_table = soup.find('table', {'id': 'ctl00_PlaceHolderMain_ucNewLegacyControl_gvTrackInternationalArticleEvntOER'})
        if events_table:
            rows = events_table.find_all('tr')
            headers = [th.text.strip() for th in rows[0].find_all('th')]
            
            print("\n" + " | ".join(headers))
            print("-" * 100)
            
            for row in rows[1:]:
                cols = row.find_all('td')
                if cols:
                    event_data = [col.text.strip() for col in cols]
                    print(" | ".join(event_data))
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    except Exception as e:
        print(f"Error parsing response: {e}")

if __name__ == "__main__":
    tracking_number = input("Enter India Post consignment number: ").strip()
    track_india_post_consignment(tracking_number)