from countryinfo import CountryInfo

def get_country_info(country):
    try:
        res = CountryInfo(country)
        data = res.info()
        return f'''Country name: {data['name']}
Capital: {data['capital']}
Area: {data['area']} km²
Currency: {data['currencies'][0]}
To learn more go to: {data['wiki']}
'''

    except:
        return f'Enter valid country name. country named {country} does not exist'