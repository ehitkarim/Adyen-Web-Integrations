from flask import Flask, render_template,jsonify, request, url_for
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv('/Users/REAZUL/Downloads/eh/Keys.env') # Specify full path to .env file

api_key = os.getenv('API_KEY')
merchant = os.getenv('MERCHANT')
returnURL = os.getenv('RETURN_URL')

app = Flask(__name__)


@app.route('/handle', methods=['POST'])

def addRegion():
    AM = float(request.form['AM'])*100 # Amount in minor units
    CA = request.form['CA'] # Country 
    IN = request.form['I'] # Type of integration

    # Following is for generating payment reference 
    currentDateAndTime = datetime.now()
    Date = str(currentDateAndTime)
    string_element = ''.join([char for char in Date if char.isnumeric()])

    # Country-Currency pairs
    Currency = { "SG":"SGD", "GB":"GBP", "US":"USD", "NL":"EUR", "AU":"AUD"}

    Headers = {"x-API-key": api_key, "content-type": "application/json"}

    body = { "merchantAccount": merchant,
         "amount": { "value": AM,"currency": Currency[CA] },
         "returnUrl": returnURL,
         "reference": 'Ref_'+string_element,
         "countryCode": CA
         }

    Result = requests.post("https://checkout-test.adyen.com/v69/sessions",headers = Headers,json = body)     

    Result = Result.json()
    #print(api_key)
    #return Result["sessionData"]
    if(IN == 'W'):
    	return render_template('Web Drop-In.html', Sessions= Result["sessionData"], ID = Result["id"])
    elif(IN == 'C'):
    	return render_template('Web Components.html', Sessions= Result["sessionData"], ID = Result["id"])
    else:
    	return render_template('gg.html')

@app.route('/redirect', methods=['GET'])

def status():
    sessionId = request.args.get('sessionId')
    redirectResult = request.args.get('redirectResult')

    headers = {"x-API-key": api_key, "content-type": "application/json"}
    body =  { "details": {"redirectResult":redirectResult}}

    Result = requests.post("https://checkout-test.adyen.com/v69/payments/details",headers = headers, json = body)
    Result = Result.json()

    return render_template('redirect.html', Outcome = Result['resultCode'], Reference = Result['merchantReference'], Amount = Result['amount']['value']/100, Currency =Result['amount']['currency']  )

@app.route('/')

def func():

	return render_template("Homepage.html")

@app.route('/checkout', methods=['POST'])

def checkout():
    header2 = request.headers.get('amount')
    #projectpath = request.form['myForm']
    return render_template('checkout.html', am=header2)


if __name__ == "__main__":
    app.run()
