import requests
from bs4 import BeautifulSoup

def infoGet(role, champ):
    info = {}
    runeDict = {}
    stats = {}

    url = f"https://app.mobalytics.gg/lol/champions/{champ}/build?role={role}"
    page = requests.get(url)
    
    soup = BeautifulSoup(page.content, "html.parser")

    roles = soup.find("div", class_="e1s7gn3p1 css-10avw8z ex3ogo80")

    not_allowed = []
    
    for i in roles:
        if "not-allowed" in str(i):
            if i.find("img")["alt"].lower() == "bot":
                not_allowed.append("adc")
            else:
                not_allowed.append(i.find("img")["alt"].lower())

    if role in not_allowed:
        print(f"Mobalytics doesn't have a build for {role.capitalize()}. \nHere's the default build instead.\n")
        role = ""
        url = f"https://app.mobalytics.gg/lol/champions/{champ}/build?role={role}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        string = soup.find("div", class_="css-p3pzap").text
        string = string[1:]
        newRole = ""
        for i in string:
            if i != " ":
                newRole += i
            else:
                break

        print(f'Defaulting to {newRole} role.')

    runeList = []

    runeList.append(soup.find("img", class_="e5svq4w6 css-1bdyqpk")['alt'])

    for i in soup.find_all("div", class_="css-1gh2v5y"):
        runeList.append(i.find("img", alt = True)['alt'])

    tree = soup.find_all("div", class_="css-6g060g e5svq4w3")

    runeDict[tree[0].text] = runeList[:4]
    runeDict[tree[1].text] = runeList[4:]

    shards = {
        "5001": "Health",
        "5002": "Armor",
        "5003": "Magic Resist",
        "5005": "Attack Speed",
        "5007": "Ability Haste",
        "5008": "Adaptive Force",
    }

    shardList = []
    for i in soup.find_all("img", class_="css-1vgqbrs enkhv8q1"):
        shardList.append(shards[i["src"].split(".png")[0][-4:]])

    runeDict["Shard"] = shardList

    items = soup.find_all("div", class_="e407fnc2 css-qyyk3q e179j9rf2")

    starterList = []
    for i in items[0].find_all("img", alt = True):
        starterList.append(i["alt"])
        
    earlyList = []
    for i in items[1].find_all("img", alt = True):
        earlyList.append(i["alt"])
        
    coreList = []
    for i in items[2].find_all("img", alt = True):
        coreList.append(i["alt"])

    itemList = []
    for i in items[3].find_all("img", alt = True):
        itemList.append(i["alt"])

    order = []
    for i in soup.find_all("div", class_="css-hgy7ai etewe3q4"):
        order.append(i.text)

        
    countSyn = {}
    for i in soup.find_all("div", class_="css-cukjo e1pfij5r0"):
        tempDict = {}
        for b in i.find_all("a", class_="ez6mgdl2 css-10l8hyk ebg788s8"):
            tempDict[b.find("p", class_="css-1w0si3o ebg788s4").text] = b.find("p", class_="css-1t0zj6v ebg788s6").text
        try:
            countSyn[(i.find("div", class_="css-11cwscx e1pfij5r4").text)] = tempDict
        except:
            break
        
    sumSpell = []
    for i in soup.find_all("img", class_="css-1xsdwvo e6oy32g1"):
        spell = i["src"].split(".png")[0].split("Summoner")[1]

        if spell == "Dot":
            spell = "Ignite"
        elif spell == "Haste":
            spell = "Ghost"
        elif spell == "Boost":
            spell = "Cleanse"

        sumSpell.append(spell)

    sit = []
    for i in soup.find_all("img", class_="e1tojong3 css-z0bo12"):
        sit.append(i['alt'])

    maxS = []
    for i in soup.find_all("p", class_="css-1sjorax e167aynf1"):
        maxS.append(i.text)

    try:
        stats["Tier"] = (soup.find("img", class_="e1jhwlgm1 css-pzje53")['alt'])
    except:
        stats["Tier"] = "N/A"

    rateHtml = soup.find_all("p", class_="css-fvdxx1 e1wiit2o5")

    try:
        stats["Win Rate"] = rateHtml[0].text+"%"
    except:
        stats["Win Rate"] = "N/A"

    try:
        stats["Pick Rate"] = rateHtml[1].text+"%"
    except:
        stats["Pick Rate"] = "N/A"

    try:
        stats["Ban Rate"] = rateHtml[2].text+"%"
    except:
        stats["Ban Rate"] = "N/A"

    try:
        stats["Skill"] = soup.find("p", class_="css-1ecmoju efj3fx62").text
    except:
        stats["Skill"] = "N/A"

    try:
        stats["Type"] = soup.find("p", class_="css-4fcf3p efzizsr2").text
    except:
        stats["Type"] = "N/A"
    tempDict = {}
    try:
        tempDict["AP"] = soup.find("p", class_="css-1whdbvu ew1cocw1").text.split(" ")[0]
    except:
        tempDict["AP"] = "N/A"

    try:
        tempDict["AD"] = soup.find("p", class_="css-hpipof ew1cocw2").text.split(" ")[0]
    except:
        tempDict["AD"] = "N/A"
        
    stats["Damage Type"] = tempDict
    
    string = soup.find("div", class_="css-p3pzap").text
    string = string[1:]
    newRole = ""
    for i in string:
        if i != " ":
            newRole += i
        else:
            break

    info["Role"] = newRole
    info['Link'] = url
    info["Stats"] = stats
    info["Counter and Synergy"] = countSyn
    info["Item List"] = itemList
    info["Core Items"] = coreList
    info["Early Items"] = earlyList
    info["Situational"] = sit
    info["Starters"] = starterList
    info["Rune"] = runeDict
    info["Ability"] = order
    info["Max Ability"] = maxS
    info["Summoner Spell"] = sumSpell

    return(info)
    
    
while True:
    role = input("Role: ")
    champ = input("Champ: ")
    print(infoGet(role, champ))

    
