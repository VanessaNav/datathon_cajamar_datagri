import json

eu_countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Estonia', 'Finland',
                'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
                'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden']

with open('europe.geojson') as json_file:
    data = json.load(json_file)
    features = []
    for f in data['features']:
        if f['properties']['name'] == 'Czech Republic':
            f['properties']['name'] = 'Czechia'
        if f['properties']['name'] in eu_countries:
            features.append(f)
    data['features'] = features

    with open('europe-filtered.geojson', 'w') as outfile:
        json.dump(data, outfile)


