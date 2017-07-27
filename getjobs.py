import requests
import urllib
import urllib2
import json

#helper function to check whether user redeemed code 
def get_user_input():
    query = raw_input("Did you redeem your code? Y/N:")
    if query == "Y":
        print("Continuing Authentification")
    else:
        print("Please redeem your code")
        get_user_input()
        
#requesting Google code 
url1 = "http://gauth.dev.wgcloud.net/v1/oauth2/device/google/getcode?grant_type=google_device&scope=email"
headers = {'cache control': "no-cache"}
response = requests.request("GET", url1, headers = headers)
response1 = str(response.text)
ucindex = response1.find("user_code")
usercode = response1[ucindex + 12 : ucindex + 21]
print("Please redeem the usercode " +  usercode + " at http://www.google.com/device")
get_user_input()
dcindex = response1.find("device_code")
devicecode = response1[dcindex + 14: ucindex - 3]
print("Device Code: " + devicecode)

#after code is redeemed
url2 = "http://gauth.dev.wgcloud.net/v1/oauth2/device/google/redeemed"
payload = "{\n    \"device_code\": \""+ devicecode +"\"\n} "
response = requests.request("POST", url2, data=payload, headers=headers)
response2 = str(response.text)
rtindex = response2.find("refresh_token")
reftoken = response2[rtindex + 16: -2]
print("Refresh Token: " + reftoken)

#Exchange the Google refresh token for an Apcera access token
url3 = "http://gauth.dev.wgcloud.net/v1/oauth2/device/google/refresh"
payload = "{\r\n     \"refresh_token\": \""+ reftoken + "\",\r\n     \"token_type\": \"GOOGLE_REFRESH\"\r\n }"
response = requests.request("POST", url3, data=payload, headers=headers)
response3 = str(response.text)
atindx = response3.find("access_token")
tokentypeindx = response3.find("token_type")
accesstoken = response3[atindx + 15: tokentypeindx -3]
print("Acess Token: " + accesstoken)

#Calling Apcera REST API
url4 = "http://api.dev.wgcloud.net/v1/info"
headers = {'authorization': "Bearer " + accesstoken}
response = requests.request("GET", url4, headers=headers)

#Getting a list of jobs
url5= "http://api.dev.wgcloud.net/v1/jobs"
headers = {'authorization': "Bearer " + accesstoken}
response = requests.request("GET", url5, headers=headers)
strresponse = response.json()

#Append all "fqn" entries to a list
fqnlist = []
x= strresponse
data = json.dumps(x)
data = str(data)
data = data.split()
for word in range(len(data)):
    if "fqn" in data[word] and "_fqn" not in data[word]:
        fqnlist.append(data[word+1])

#Return a list with only job entries
joblist = []
counter = 0 
for entry in fqnlist:
    if "job" in entry:
        joblist.append(entry)
        counter = counter + 1

#Print cleaned names on newline
for jobs in joblist:
    jobs = jobs[1:-2]
    print(jobs)
    
table = []
for i in joblist:
    nested = []
    findx = i.find("::")
    first = i[:findx]
    nested.append(first)
    string2 = i[findx+2:]
    sindx = string2.find("::")
    second = string2[:sindx]
    nested.append(second)
    third = string2[sindx + 2 :]
    nested.append(third)
    table.append(nested)
    table_str = str(table)
print table 
print("There are " + str(counter) + " jobs") 

        



    
    
    


        
