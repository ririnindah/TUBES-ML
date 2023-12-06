import pickle
import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder

loaded_model = pickle.load(open('estimasi_mobil.sav', 'rb'))
car_models = ['SLK', 'S Class', 'SL CLASS', 'G Class', 'GLE Class', 'GLA Class', 'A Class', 'B Class', 'GLC Class', 'C Class', 'E Class', 'GL Class', 'CLS Class', 'CLC Class', 'CLA Class', 'V Class', 'M Class', 'CL Class', 'GLS Class', 'GLB Class', 'X-CLASS', 'CLK', 'R Class']
car_transmission = ['Automatic', 'Manual', 'Semi-Auto', 'Other']
car_fuel = ['Petrol', 'Hybrid', 'Diesel', 'Other']

st.title('Estimasi Harga Mobil Bekas')

# Set initial values to None
selected_model = st.selectbox('Model Mobil', car_models, index=None)
year = st.number_input('Tahun Mobil', value=None, format="%f")  # Format angka tanpa desimal
# transmission = st.selectbox('Transmisi', car_transmission, index=None)
mileage = st.number_input('Jarak Tempuh (mile)', value=None, format="%f")  # Format angka dengan float
# fuelType = st.selectbox('Jenis Bahan Bakar', car_fuel, index=None)
# tax = st.number_input('Pajak Mobil', value=None, format="%f")  # Format angka dengan float
mpg = st.number_input('Konsumsi Bahan Bakar (mpg)', value=None, format="%f")  # Format angka tanpa desimal
engineSize = st.number_input('Ukuran Mesin (cc)', value=None, format="%f")  # Format angka dengan float

# Create a DataFrame with the input values, replace None with NaN
input_data = pd.DataFrame({
    'year': [year],
    # 'transmission': [transmission],
    'mileage': [mileage],
    # 'fuelType': [fuelType],
    # 'tax': [tax],
    'mpg': [mpg],
    'engineSize': [engineSize],
    'model': [selected_model]
}).replace({None: float('nan')})

# Label encode categorical features in the input_data
le = LabelEncoder()
input_data['model'] = le.fit_transform(input_data['model'])
# input_data['transmission'] = le.fit_transform(input_data['transmission'])
# input_data['fuelType'] = le.fit_transform(input_data['fuelType'])

# Ensure that the column order matches the model's expectations
# column_order = ['model', 'year', 'transmission', 'mileage', 'fuelType', 'tax', 'mpg', 'engineSize']
column_order = ['model', 'year', 'mileage', 'mpg', 'engineSize']

# Ensure the correct order of features in the input_data
input_data = input_data[column_order]

predict = ''

if st.button('Estimasi'):
    # Check if any input value is still None (null)
    if input_data.isnull().values.any():
        st.warning('Mohon isi semua nilai input.')
    else:
        # Make predictions using the loaded model
        prediction = loaded_model.predict(input_data)
        predict = prediction[0]   # Assuming prediction is a single value
        st.write('Estimasi Harga Mobil Bekas (Euro): €{:,.2f}'.format(predict))