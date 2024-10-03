from django.shortcuts import render
from django.http import request
import requests

# Create your views here.
def home(request):
    BASE_API = 'http://api.marketstack.com/v1'

    API_KEY = '983e92d30f30c103dfda6accfac5a693'
    symbol = 'AAPL'

    # if API_KEY == '':
    #     print("Please enter the API_KEY generated from market api")
    #     return render(request, 'index.html',{'checker': 'Enter valid api_key'})
    
    # else:
    request_url = f"{BASE_API}/eod?access_key={API_KEY}&symbols={symbol}"

    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
        print(data, '%%%%%%%%%%%%%%%%%%%%%%%')

        access_data = data['data'][0]
        print(access_data, '**************************')
            
        context = {
                'open': access_data.get('open', 'N/A'),
                'high': access_data.get('high', 'N/A'),
                'low': access_data.get('low', 'N/A'),
                'adj_high': access_data.get('adj_high', 'N/A'),
                'adj_low': access_data.get('adj_low','N/A')
                }
            
        return render(request, 'index.html', context)
    else:
        print("An error occured")
        return render(request, 'index.html', {})
        
        # return render(response, 'index.html', {})


    


