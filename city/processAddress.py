import csv
import pyproj

TWD97 = pyproj.Proj(init='epsg:3826') #定義TWD97坐標系
WGS84 = pyproj.Proj(init='epsg:4326') #定義WGS84坐標系

file1 = open('names.csv', 'r')
file2 = open('record.csv', 'w')
reader = csv.reader(file1)
writer = csv.writer(file2)
new_rows_list = []
header = "TOWN_CODE	LOCATION ABE_DA	AEN_DA AREA_TA UN_NA CL_DA	LASTMOD	POLY_LIST"
#0 5 7 8 11 12 23 24
#1 2 3 4 6 9 10 13 14 15 16 17 18 19 20 21 22
for row in reader:
    if row[0] == "TOWN_CODE":
        pass
    else:
        print(row[3])
        tmp = row[24].split(",")
        first = 0
        second = 0
        for eachPlace in tmp:
            first += float(eachPlace.split(" ")[0])
            second += float(eachPlace.split(" ")[1])
        first/=len(tmp)
        second/=len(tmp)
        lon, lat = pyproj.transform(TWD97, WGS84, first, second)
        new_row = [row[0], row[5], row[7], row[8], row[11], row[12], row[23], [lon,lat]]
        new_rows_list.append(new_row)
file1.close()   # <---IMPORTANT

# Do the writing
writer.writerows(new_rows_list)
file2.close()