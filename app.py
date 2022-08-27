from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__, template_folder='template')

def load_model():
    with open('model_linreg.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

model = load_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form-prediksi')
def form_prediksi():
    return render_template('formpage.html')

@app.route('/prediksi-hasil-panen', methods=['POST'])
def predict():
    
    Tahun = float(request.form['Tahun'])
    Bulan = float(request.form['Bulan'])
    ukuran = float(request.form['ukuran'])

    hitung = np.array([[Tahun, Bulan, ukuran]])
    
    prediction = model.predict(hitung)
    hasil_pred = round(prediction[0], 3)
    
    def ton(value):
        str_value = str(value)
        separate_decimal = str_value.split(".")
        after_decimal = separate_decimal[0]
        before_decimal = separate_decimal[1]

        reverse = after_decimal[::-1]
        temp_reverse_value = ""

        for index, val in enumerate(reverse):
            if (index + 1) % 3 == 0 and index + 1 != len(reverse):
                temp_reverse_value = temp_reverse_value + val + "."
            else:
                temp_reverse_value = temp_reverse_value + val

        temp_result = temp_reverse_value[::-1]

        return "" + temp_result + "," + before_decimal
    
    output = ton(hasil_pred)
    
    #versi int
    tahun = int(request.form['Tahun'])
    bulan = int(request.form['Bulan'])
    
    #nentuin ukuran
    if ukuran == 1:
        ukuran = "Besar"
    elif ukuran == 2:
        ukuran = "Sedang"
    else:
        ukuran = "Kecil"
    
    return render_template('hasil.html', hasil = output, year = tahun, month = bulan, size = ukuran)

if __name__ == '__main__':
    app.run(debug = True)