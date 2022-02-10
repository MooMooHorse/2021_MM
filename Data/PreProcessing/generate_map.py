"""
python -m pip install basemap-data
python -m pip install basemap-data-hires
https://github.com/matplotlib/basemap
"""
def plot_map(lat,lon):
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt

    m = Basemap(llcrnrlon=140.874088,llcrnrlat=-39.054526,urcrnrlon=151.567450,urcrnrlat=-33.122107,projection='mill',\
                    resolution='l')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.fillcontinents(color='#04BAE3', lake_color='#FFFFFF')
    m.drawmapboundary(fill_color='#FFFFFF')
    
    x,y = m(lon,lat)
    m.plot(x,y,'ro',markersize=4,alpha=.5)

    # # x,y = m(lon2,lat2)
    # # m.plot(x,y,'go',markersize=4,alpha=.5)

    plt.title('Geo Plotting')
    plt.show()

plot_map([-37],[146])