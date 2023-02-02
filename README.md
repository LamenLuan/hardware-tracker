# hardware-tracker
This python script is built to track a product price in the three biggest brazilian hardware e-commerces (Kabum, Pichau, Terabyteshop), storing that information on a google spreadsheet, and notificating me when price hit a new minimun. This is my first experience with python, don't expect much from it 🙂

## Screenshot
<p align="center">
  <img src="https://github.com/LamenLuan/hardware-tracker/blob/main/screenshot.png">
</p>

## Tutorial to run
### 1. Install with pip
- beautifulsoup4
- cloudscraper
- gspread
- win10toast
- cx_Freeze (if you want to create an executable)
### 2. Configure Google Cloud Platform APIs
I learned that configuration in this [video](https://youtu.be/bu5wXjz2KvU):
- In a project, enable Google Drive and Google Sheets APIs
- Generate a client email in Sheets API screen
- Create a JSON private key from this client
- Put this JSON in a directory called "gspread" in "price_tracker" directory
- Give edit permission in a sheet called "tracking-sheet" to the client by its
 email
- Rename work sheet as "BestPrice"
### 3. Put your product links in a JSON
- Create a JSON names "sites.json" in "price_tracker" directory
- Put all links you want te script to track in the string list
- Links from other sites will be just ignored
