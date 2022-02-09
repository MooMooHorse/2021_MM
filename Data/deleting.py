import csv
from math import sin, cos, sqrt, atan2, radians

f = open("modis_2020_Australia.csv")
L = list(csv.reader(f))

R = 6373.0
west = 140.966
east = 149.977
north = -33.98
south = -39.14
confidence_require = 70

#functions
def cal_dis(latitude1,longitude1,latitude2,longitude2):
    lat1 = radians(float(latitude1))
    lon1 = radians(float(longitude1))
    lat2 = radians(float(latitude2))
    lon2 = radians(float(longitude2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def loc_in(lat,lon):
    if ((float(lat) > south) & (float(lat) < north) & (float(lon) > west) & (float(lon) < east)):
        return 1;
    else:
        return 0;

##just locate the area between west = 140.966 east = 149.977 north = -33.98 south = -39.14
result = []
for i in range (1,len(L)):
    if (loc_in(L[i][0],L[i][1]) & (L[i][9] > confidence_require)):
        result.append(i)

#print(len(result))  28056







