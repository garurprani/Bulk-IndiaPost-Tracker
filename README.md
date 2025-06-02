# 📦 IndiaPost Consignment Tracker — Vulnerability PoC

This Python script demonstrates a **vulnerability in the India Post consignment tracking system**. It allows tracking any valid consignment number by bypassing captcha and security mechanisms using **hardcoded cookies and hidden ASP.NET form parameters**.

---

## 🔍 Vulnerability Summary

The India Post tracking portal (`https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/trackconsignment.aspx`) relies on hidden ASP.NET fields such as:

- `__VIEWSTATE`
- `__EVENTVALIDATION`
- `__REQUESTDIGEST`

...to verify form integrity and session state. Normally, the system also uses a **captcha** and **session cookies** to prevent automation.

> However, with static values for these parameters (captured via browser dev tools), and by passing specific cookies, the site **accepts requests without human interaction** — meaning the captcha can be bypassed.

---

## 🛠 How the Script Works

The script uses `requests` and `BeautifulSoup` to simulate a browser request to India Post’s tracking service:

### Steps:

1. A POST request is made to the tracking endpoint.
2. Custom headers simulate a real browser, including `User-Agent`, `Referer`, `X-MicrosoftAjax`, and more.
3. The payload contains all hidden form fields necessary for a successful request:
   - `__VIEWSTATE`
   - `__EVENTVALIDATION`
   - `__REQUESTDIGEST`
   - `ctl00$ScriptManager`
   - Consignment number
4. The response is parsed for tracking status and returned.

---

## ⚠️ Required Setup

You need to **manually insert valid session values** (captured from your own browser). The script will not work with expired cookies or viewstate data.

### Required Headers/Cookies:

- You **must insert these manually** by visiting the [tracking page](https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/trackconsignment.aspx) and:
  1. Submitting a valid tracking number
  2. Using browser dev tools → Network → Form data & cookies

> **Never share your own cookies on GitHub!** They contain session-specific data and may allow impersonation.

---

### 🧾 Parameters You Need to Update:

Update these in the script before use:

```python
payload = {
    "__VIEWSTATE": "Your captured value",
    "__EVENTVALIDATION": "Your captured value",
    "__REQUESTDIGEST": "Your captured value",
    ...
}

headers = {
    "Cookie": "Insert your session cookies here",
    ...
}
