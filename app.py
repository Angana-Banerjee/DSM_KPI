from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load data when the app starts
data = pd.read_csv("Ahm_Project (version 1).csv")

@app.route('/salesman', methods=['GET'])
def get_salesman_by_contact():
    contact = request.args.get('contact')
    if not contact:
        return jsonify({'error': 'Missing required parameter: contact'}), 400

    # Search the contact as string to avoid type mismatch
    record = data[data['Contacts'].astype(str) == str(contact)]

    if record.empty:
        return jsonify({'error': 'Contact not found'}), 404

    row = record.iloc[0]

    # Safely cast to native types for JSON serialization
    def safe_cast(value, cast_type):
        return cast_type(value) if pd.notnull(value) else None

    response = {
        'Contact': str(row['Contacts']),
        'Salesman Code': str(row['Salesman Code']),
        'Mandays': safe_cast(row['Mandays'], float),
        'Listed_Outlets': safe_cast(row['Listed_Outlets'], int),
        'Gate_Way_ECO_30': safe_cast(row['Gate_Way_ECO_30'], int),
        'ECO_MTD': safe_cast(row['ECO_MTD'], int),
        'Oil_Tgt_': safe_cast(row['Oil_Tgt_'], int),
        'Oil_Vol(MT)': safe_cast(row['Oil_Vol(MT)'], float),
        'Food_Tgt_': safe_cast(row['Food_Tgt_'], int),
        'Food_Vol(MT)': safe_cast(row['Food_Vol(MT)'], float)
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
