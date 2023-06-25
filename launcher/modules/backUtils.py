import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }

# function to check internet connection
def checkInternet() -> bool:
    try:
        requests.get('https://updater.braxtonelmer.com/', timeout=10, headers=headers)
        return True
    except:
        return False


# function to download a file using url 
def downloadFile(file_url, file_loc) -> bool:
    try:
        r = requests.get(file_url, stream = True, headers=headers, verify=False)
        with open(file_loc, 'wb') as ufile:
            for chunk in r.iter_content(chunk_size=1024):
    
            # Writing one chunk at a time to file (No excessive memory usage on large-size files)
                if chunk:
                    ufile.write(chunk)
                    ufile.flush()

        return True
    
    except:
        return False