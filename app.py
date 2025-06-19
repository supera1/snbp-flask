from flask import Flask, render_template, request, jsonify
from google.oauth2 import service_account
import google.auth.transport.requests
import requests
import json
import os

app = Flask(__name__)

# Configuration
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
API_URL = "https://api-snbp.snpmb.id/snbp-check"
SERVICE_ACCOUNT_FILE = "service-account.json"

def get_snbp_data(nisn, npsn):
    """
    Fetch SNBP data from the API using service account authentication
    """
    try:
        # Create credentials from service account
        creds = service_account.IDTokenCredentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            target_audience=API_URL,
        )
        
        # Refresh the credentials to get a valid token
        auth_request = google.auth.transport.requests.Request()
        creds.refresh(auth_request)
        
        # Make the API request
        params = {"nisn": nisn, "npsn": npsn}
        headers = {"Authorization": f"Bearer {creds.token}"}
        
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    except FileNotFoundError:
        return {"error": "Service account file not found. Please ensure 'service-account.json' is in the application directory."}
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_snbp():
    """Handle SNBP check requests"""
    nisn = request.form.get('nisn', '').strip()
    npsn = request.form.get('npsn', '').strip()
    
    # Validate inputs
    if not nisn or not npsn:
        return jsonify({
            "error": "Both NISN and NPSN are required"
        }), 400
    
    # Get data from API
    result = get_snbp_data(nisn, npsn)
    
    # Check for errors
    if "error" in result:
        return jsonify(result), 500
    
    # Extract the required fields from the nested structure
    data = result.get("data", {})
    message = result.get("message", "").lower()
    
    # Determine eligibility based on message
    if message == "siswa diterima":
        eligibility = "Tidak Dapat Mengikuti Test Mandiri T2 UNSRAT"
    elif message in ["siswa tidak diterima", "siswa bukan peserta"]:
        eligibility = "Dapat Mengikuti Test Mandiri T2 UNSRAT"
    else:
        eligibility = "N/A"
    
    response_data = {
        "nama": data.get("nama", "N/A"),
        "status": data.get("status", "N/A"),
        "keterangan": result.get("message", "N/A"),
        "eligibility": eligibility
    }
    
    return jsonify(response_data)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Check if service account file exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Warning: {SERVICE_ACCOUNT_FILE} not found. Please ensure it's in the same directory as this script.")
    
    app.run(debug=True, host='0.0.0.0', port=5000)