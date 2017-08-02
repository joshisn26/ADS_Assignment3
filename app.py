from flask import Flask, render_template, request, session, redirect, url_for
from forms import predictionForm
import json
import urllib.request


app = Flask(__name__)
app.secret_key = "mysec-key"

	
@app.route("/prediction", methods =["GET" , "POST"])
def prediction():
	form = predictionForm()
	if request.method == "POST":
		credit_score = form.credit_score.data
		first_payment_date = form.first_payment_date.data
		fthb_flag = form.fthb_flag.data
		matr_date = form.matr_date.data
		msa = form.msa.data
		mortage_insurance_pct = form.mortage_insurance_pct.data
		no_of_units = form.no_of_units.data
		occupancy_status = form.occupancy_status.data
		cltv = form.cltv.data
		dti_ratio = form.dti_ratio.data
		original_upb = form.original_upb.data
		
		data = {	
				"Inputs": {
					"input1":
						[
							{
								'credit_score': credit_score,   
								'first_payment_date': first_payment_date,   
								'fthb_flag': fthb_flag,   
								'matr_date': matr_date,   
								'msa': msa,   
								'mortage_insurance_pct': mortage_insurance_pct,   
								'no_of_units': no_of_units,   
								'occupancy_status': occupancy_status,   
								'cltv': cltv,   
								'dti_ratio': dti_ratio,   
								'original_upb': original_upb, 
							}
						],
					},
				"GlobalParameters":  {
			}
		}
		body = str.encode(json.dumps(data))

		url = 'https://ussouthcentral.services.azureml.net/workspaces/7a01f9d6cb9b4df09ebc6b306c3a06f0/services/2a4594c77fb147ef9876506f4dc66e9d/execute?api-version=2.0&format=swagger'
		api_key = 'JhBn9dZ907p1ZbJHk+UflP7pDvANyha/8aOH6sk+T06wJwU+bcXdtW+bH4B7c8CKo+ivDtsH+m4cpXUAoMVh2A==' 
		headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

		req = urllib.request.Request(url, body, headers)

		try:
			response = urllib.request.urlopen(req)

			result = response.read()
			response_dict = json.loads(result)
			print(result) 
			est_int_rate = response_dict['Results']['output1'][0]["Scored Labels"]
			print("Interest rate: ", est_int_rate)
		except urllib.error.HTTPError as error:
			print("The request failed with status code: " + str(error.code))

			# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
			print(error.info())
			print(json.loads(error.read().decode("utf8", 'ignore')))

		return render_template("success.html", pred_int_rate = est_int_rate)
	elif request.method == 'GET':
		return render_template('prediction.html',form=form)
		
@app.route("/")
def home():
    return render_template('mainpage.html', context={})


if __name__ == "__main__":
  app.run(debug=True)