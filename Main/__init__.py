import json
import requests
import datetime

prefix = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
fq = "fq=news_desk(\"Health\")"
sort = "sort=newest"
page = "page="
key = "api-key=bc6f4a013b593ac80ff7f31de9c52b80:11:74279314"
begin_date = "begin_date=20160217"
end_date = "end_date=20160224"

count = 1

days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

url = prefix + "?&" + fq + "&" + "sort=oldest" + "&" + page + str(1) + "&" + key
resp = requests.get(url)
oldest_year = (resp.json()["response"]["docs"][0]["pub_date"])[0:4]
current_year = datetime.date.today().strftime('%Y')
current_date = ((datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y%m%d'))
with open("stats.csv", "a") as stats:
    stats.write("Begin Date, End Date, Hits, Pages\n")
for year in range(int(oldest_year), int(current_year) + 1):
    for month in range(1, 13):
        for date in range(1, days[month - 1], 7):
            mon = month
            bd = date
            ed = date
            if (month < 10):
                mon = "0" + str(month)
            if (bd < 10):
                bd = "0" + str(bd)
            if (ed + 6 < 10):
                ed = "0" + str(ed + 6)
            elif (ed + 6 > days[month - 1]):
                ed = days[month - 1]
            else:
                ed = ed + 6
            begin_date = "begin_date=" + str(year) + str(mon) + str(bd)
            end_date = "end_date=" + str(year) + str(mon) + str(ed)
            url = prefix + "?&" + fq + "&" + sort + "&" + begin_date + "&" + end_date + "&" + page + "1" + "&" + key
            print(url)
            resp = requests.get(url)
            hits = resp.json()["response"]["meta"]["hits"]
            pages = int(hits / 10)
            if (pages * 10 < hits):
                pages += 1
            if (pages > 0):
                print("Number of pages = " + str(pages))
            with open("stats.csv", "a") as stats:
                stats.write(str(year) + str(mon) + str(bd) + "," + str(year) + str(mon) + str(ed) + "," + str(hits) + "," + str(pages)+"\n")
            for i in range(0, pages):
                url = prefix + "?&" + fq + "&" + sort + "&" + begin_date + "&" + end_date + "&" + page + str(
                    i) + "&" + key
                resp = requests.get(url)
                with open("../jsonFiles/news_desk_health_" + str(count) + ".json", 'w') as file:
                    json.dump(resp.json(), file)
                print("Writing to file: news_desk_health_" + str(count) + ".json")
                print("Page = " + str(i) + " done")
                count += 1
