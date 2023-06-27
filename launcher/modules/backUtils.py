# import required modules
import requests
import psutil

# define web headers
legacyHeaders = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# function to check internet connection
def checkInternet() -> bool:
    try:
        requests.get('https://updater.braydenedgar.com/', timeout=10, headers=headers)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

def getRam() -> int:
    return int(psutil.virtual_memory().total / (1024**2))

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