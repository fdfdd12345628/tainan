twd97 = "171012.57025 2541428.99683333,171015.004416667 2541429.42016667,171015.216083333 2541428.5735,171012.88775 2541427.9385,171012.781916667 2541428.04433333,171012.57025 2541428.99683333"



import pyproj

TWD97 = pyproj.Proj(init='epsg:3826') #定義TWD97坐標系
WGS84 = pyproj.Proj(init='epsg:4326') #定義WGS84坐標系

for line in twd97.split(','):
    t = line.split()  # separate each column, using "space"
    lon,lat = pyproj.transform(TWD97, WGS84,t[0],t[1])
    #將TWD97坐標轉成WGS84經緯度
    print(lon,lat)
