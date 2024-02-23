import pandas as pd
import googlemaps
import time

aed_location_path = '../Data2024-csv/aed_for_googlemap.csv'
output = '../get_aed_location_latlon/'
gmaps = googlemaps.Client(key='addyourgmapkey')
def get_latlon_from_googlemap_aedloc(input_path,output_path):
    '''
    Get latitude and longitude data from google map API
    :param input_path:
    :param output_path:
    :return: A pd dataframe with two columns (latitude and longitude)
    '''
    aed_location = pd.read_csv(input_path,encoding='utf-8')
    #Preprocessing the data
    #Drop records with NAN id
    #need to ensure id should be unique and valid
    aed_location = aed_location[-aed_location['id'].isna()]
    aed_location = aed_location[-aed_location['full_address'].isna()]
    #Drop duplicates
    #aed_location = aed_location.drop_duplicates(subset=['id'])
    #might have some records with same address but different id
    #keep these duplicates
    #aed_location = aed_location.drop_duplicates(subset=['full_address'])
    aed_location['new_id'] = aed_location.index + 1
    aed_location.to_csv('../preprocessed-data/aed_location_cleaned.csv',index=False,encoding='utf-8')
    print(aed_location.shape)
    #count number
    i = 1
    d = 1
    id = list()
    new_id = list()
    lat = list()
    lon = list()
    for index, row in aed_location.iterrows():
        id.append(row['id'])
        new_id.append(row['new_id'])
        temp_full_address = row['full_address']
        try:
            geocode_result = gmaps.geocode(temp_full_address)
            temp_lat = geocode_result[0]['geometry']['location']['lat']
            temp_lon = geocode_result[0]['geometry']['location']['lng']
            lat.append(temp_lat)
            lon.append(temp_lon)
            time.sleep(0.05)  #limit the retreiving speed
        except:
            print('Fail to get location data')
            lat.append('NAN')
            lon.append('NAN')
        i = i + 1
        # if i > 2:
        #     #print(pd.DataFrame(dict(id=id)))
        #     break
        if i % 200 == 0:
            print(f'Finished i tasks, remaining{aed_location.shape[0]-i}')
    aed_location_latlon = pd.DataFrame(dict(id=id,new_id=new_id, lat=lat, lon=lon))
    return aed_location_latlon




if __name__ == '__main__':
    # aed = get_latlon_from_googlemap_aedloc(aed_location_path,None)
    # aed.to_csv('../get_aed_location_latlon/aed_location_latlon_v1.csv',index=False,encoding='utf-8')

    old_aed_loc = pd.read_csv('../preprocessed-data/aed_location_cleaned.csv',encoding='utf-8')
    #print(old_aed_loc.head())
    aed_loc_latlon = pd.read_csv('../get_aed_location_latlon/aed_location_latlon_v1.csv',encoding='utf-8')
    merged_aed_loc = pd.merge(old_aed_loc, aed_loc_latlon, on='new_id')
    merged_aed_loc.to_csv('../get_aed_location_latlon/merged_aed_loc.csv',encoding='utf-8',index=False)
