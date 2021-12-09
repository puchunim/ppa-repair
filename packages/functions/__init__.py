from requests import get # Function to make HTTP requests
from lxml.html import fromstring # Function to parse HTML pages

def test_versions(ppa: str) -> str:
    """
    Function to test all the versions name of a informed ppa.
    ---
    
    [Params]
     ppa : str
        PPA team and application (TEAM/APP)
    
    [Return]
     str
        Results of the search
    """

    devs_site = "https://en.wikipedia.org/wiki/Ubuntu_version_history#Release_history" # Site with development names of Ubuntu

    devs = [
        dev[13:].replace("LTS ", "").replace(")", "").replace("(", "")
        for dev in fromstring(get(devs_site).text).xpath(
            '//span[@class="mw-headline"]/text()'
        ) 
        if "Ubuntu" in dev
    ] # Generating list of Ubuntu development names (adjective + animal)

    dev_names = list(map(
        lambda d: d.split(" ")[0].lower(),
        devs
    )) # Generating list of Ubuntu development names (just adjective)

    for dev in dev_names[::-1]: # For all development names (reversed order)
        try: # Try the lines in the block
            base_url = "http://ppa.launchpad.net/{}/{}/ubuntu/dists/" # Base url of a ppa
            ppa_team, ppa_app = ppa.split('/') # Spliting the two values in ppa
            v = get(base_url.format(ppa_team, ppa_app) + version) # Get the page of ppa
        
        except: # Except (a error is raised)
             return "" # Nothing is returned
        
        else: # Else (request worked)
            if v.status_code == 200: # If status code is OK
                return version # Development name is returned

    return "" # If request worked but status_code != 200, nothing is returned
