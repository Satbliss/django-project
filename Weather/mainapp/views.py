from django.shortcuts import render
import requests
# Create your views here.
def index(request):
    BASE_URL = 'http://api.weatherapi.com/v1'

    API_KEY = '678be013aa8d4ad4ac3111006243008'

    if request.method == 'POST':
        city = request.POST.get('city').lower()
        print(city)

        if API_KEY == '':
            print('Please add your generated API key into the "API_KEY" variable within the views.py')
            return render(request, 'index.html', {'checker': 'Please add your generated  API key into the "API_KEY" variable within the views.py'})
        
        elif (city == ''):
            print('No value')
            return render(request, 'index.html', {'checker':'Please eneter valid info...!'})
        
        else:
            request_url = f"{BASE_URL}/current.json?key={API_KEY}&q={city}&aqi=no"

            response = requests.get(request_url)

            if response.status_code == 200:
                data =  response.json()

                location = data['location']
                weather = data['current']

                print(location['tz_id'])
                print(weather['temp_c'])


                context = {
                    'weather':weather['temp_c'],
                    'wind_mph':weather['wind_mph'],
                    'humidity':weather['humidity'],
                    'city_name':location['name'],
                    'region':location['region'],
                    'country':location['country'],
                    'lat':location['lat'],
                    'lon':location['lon'],
                    'localtime':location['localtime'],
                    'continent':location['tz_id'],
                    'static_city':city                               
                
                }

                return render(request,'index.html',context)
            
            else:
                print("An error occured")
                return render(request, 'index.html', {'static_city':city, 'checker': 'Please enter valid city'})
            
    return render(request, 'index.html', {})