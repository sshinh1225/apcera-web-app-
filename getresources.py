import requests
import sys 
import json

def parsetolist(get, customurl, headers, fqnlist):
    response = requests.request("GET", customurl, headers=headers)
    x = response.json()
    data = (str(json.dumps(x))).split()
    for word in range(len(data)):
        if "fqn" in data[word] and "_fqn" not in data[word]:
            fqnlist.append(data[word+1])
            
def getresources(resource): 
    #Get access token
    arg = sys.argv[1]
    arg_str  = str(arg)
    
    url = "http://basicauth.dev.wgcloud.net/v1/oauth2/token"
    
    headers = { 'authorization': "Basic YWRtaW46UGFzc3cwcmQjMTIzNA==",
    'cache-control': "no-cache"
    }
    
    response0 = requests.request("POST", url, headers=headers)
    response = str(response0.text) 
    atindx = response.find("access_token")
    tokentypeindx = response.find("token_type")
    accesstoken = response[atindx + 15: tokentypeindx -3]
    print("Acess Token: " + accesstoken)
            
    
    #Get a list of resources and append all "fqn" entries to a list
    fqnlist = []
    get = "GET"
    options = ["stager", "app", "gateway", "docker", "sempipe", "capsule"]
    headers = {'authorization': "Bearer " + accesstoken}
    
    try: 
        if arg_str == "sempipe":
            customurl = "http://api.dev.wgcloud.net/v1/jobs?tag=pipeline"
            parsetolist(get,customurl,headers, fqnlist)
        elif arg_str == "capsule":
            ender = "heavy"
            customurl = "http://api.dev.wgcloud.net/v1/jobs?tag=heavy" 
            parsetolist(get,customurl,headers, fqnlist)
        elif arg_str in options[0:5]:
            customurl = "http://api.dev.wgcloud.net/v1/jobs?tag=" + arg_str
            parsetolist(get,customurl,headers, fqnlist)
        else:
            customurl = "http://api.dev.wgcloud.net/v1/" + arg_str
            parsetolist(get,customurl,headers, fqnlist)
    except:
        print("Valid names: app, stager, gateway, sempipe, capsule, docker, jobs, packages, networks, services, providers")

    
    #Return a list with only job entries
    list = []
    counter = 0 
    for entry in fqnlist:
        if arg_str[-1] == 's':
            if arg_str[:-1] in entry:
                list.append(entry)
                counter = counter + 1 
        else:
            if arg_str in options and "job" in entry:
                list.append(entry)
                counter = counter + 1
            elif arg_str not in options and arg_str in entry:
                list.append(entry)
                counter = counter + 1
    
    #Print cleaned names on newline
    l1 = []
    for x in list:
        resources = x[1:-2]
        print(resources)
        l1.append(resources)
          
    
    if arg_str[-1] == "s":
        print("There are " + str(counter) + " " + arg_str)
    else:
        print("There are " + str(counter) + " " + arg_str + "s")
    
    table = []
    for i in l1:
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
print(table)

adder = "" 
for list in table:
    uno = "<td>" + str(list[0]) + "</td>"
    dos = "<td>" + str(list[1]) + "</td>"
    tres = "<td>" + str(list[2]) + "</td>"
    adder = adder + "<tr> + uno + dos + tres + </tr>"
          
html = """ <table>
        <thead>
          <tr>
              <th>Endpoint</th>
              <th>Namespace</th>
              <th>Name</th>
          </tr>
        </thead>
        <tbody>""" + adder + " </tbody> </table>"
 
print(html) 
f = file.open('tester.html', 'w')
f.write(html)


        
            

    
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        getresources(sys.argv[1])
    else:
        sys.exit("More than one arg")            



        
