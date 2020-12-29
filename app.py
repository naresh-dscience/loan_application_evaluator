from flask import Flask, render_template, request
import json
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('loan_application.pickle', 'rb'))

with open("columns.json", "r") as f:
    __data_columns = json.load(f)['data_columns']

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():

    if request.method == 'POST':
        applicantincome = int(request.form['applicantincome'])
        coapplicantincome = int(request.form['coapplicantincome'])
        loanamount = int(request.form['loanamount'])
        loanamountterm = int(request.form['loanamountterm'])
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        selfemployed = request.form['selfemployed']
        credithistory = request.form['credithistory']
        propertyarea = request.form['propertyarea']

        if gender == 'Female':
            g_f = 1
            g_m = 0
        else:
            g_f = 0
            g_m = 1

        # print('Genderr:',gender)

        if married == 'No':
            m_y = 0
            m_n = 1
        else:
            m_y = 1
            m_n = 0

        dep = dependents
        dp = np.zeros(4)
        if dep == '1':
            dp[1] = 1
        elif dep == '2':
            dp[2] = 1
        elif dep == '3+':
            dp[3] = 1
        else:
            dp[0] = 1

        if education == 'Not Graduate':
            e_g = 0
            e_n = 1
        else:
            e_g = 1
            e_n = 0

        if selfemployed == 'Yes':
            se_n = 0
            se_y = 1
        else:
            se_n = 1
            se_y = 0

        if credithistory == '0':
            ch_0 = 1
            ch_1 = 0
        else:
            ch_0 = 0
            ch_1 = 1

        prop_area = propertyarea
        pa = np.zeros(3)
        if prop_area == 'Rural':
            pa[0] = 1
        elif prop_area == 'Urban':
            pa[2] = 1
        else:
            pa[1] = 1

        x = np.zeros(len(__data_columns))

        x[0] = applicantincome
        x[1] = coapplicantincome
        x[2] = loanamount
        x[3] = loanamountterm

        x[4] = g_f
        x[5] = g_m
        x[6] = m_n
        x[7] = m_y
        x[8] = dp[0]
        x[9] = dp[1]
        x[10] = dp[2]
        x[11] = dp[3]
        x[12] = e_g
        x[13] = e_n
        x[14] = se_n
        x[15] = se_y
        x[16] = ch_0
        x[17] = ch_1
        x[18] = pa[0]
        x[19] = pa[1]
        x[20] = pa[2]

        prediction=model.predict([x])[0]




        if prediction==0:
            return render_template('index.html',prediction_text="Sorry, your loan application is Rejected.")
        else:
            return render_template('index.html',prediction_text="Congratulations!!!, your loan application is Approved!!!")
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run()

