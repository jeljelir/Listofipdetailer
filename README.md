# Quick and Simple IP Scanner

## Get Virus Total API Key
Get the [VT API key](https://www.virustotal.com/gui/user/aliin/apikey) and add it to the file.
```python
vt_apis = [
    ''
]
```
Bear in mind that the free VT API key has limitations: 4 IPs per minute and 500 per day.
So, you can add multiple API keys to the app.

## Run the App
First set the list of IPs
```python
# List of IPs
ip_list = """
1.1.1.1
"""
```
Then run the script
```python
python app.py
```

## To-do List
- [ ] Read the list of IPs from a file
- [ ] Read the smaller list of IPs as an argument
- [ ] Get the API key as an argument
