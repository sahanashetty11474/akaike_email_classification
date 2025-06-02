from flask import Flask, request, jsonify
from models import classify_email
from utils import mask_pii

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    try:
        data = request.get_json()
        email_body = data.get("input_email_body")
        if not email_body:
            return jsonify({"error": "No input_email_body provided"}), 400

        # Mask PII from email text
        masked_email, entities = mask_pii(email_body)
        
        # Classify masked email text
        category = classify_email(masked_email)

        # Build the response as per required format
        response = {
            "input_email_body": email_body,
            "list_of_masked_entities": entities,
            "masked_email": masked_email,
            "category_of_the_email": category
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Starting the API server...")
    app.run(debug=True, host='0.0.0.0', port=7860)
