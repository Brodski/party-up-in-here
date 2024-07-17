# import requests
import http.client

host = "addons.mozilla.org"
path = "/firefox/downloads/file/4312995/styl_us-1.5.48.xpi"
conn = http.client.HTTPSConnection(host)
conn.request("GET", path)
response = conn.getresponse()
data = response.read()
conn.close()

with open("extensions/stylus.xpi", "wb") as file:
    file.write(data)