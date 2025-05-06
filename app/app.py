from flask import Flask, request, jsonify
from models import RequestData

app = Flask(__name__)

@app.route('/sort', methods=['POST'])
def sort():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Request body must be valid JSON"}), 400
        
        request_data = RequestData.from_dict(data)
        sorted_contacts = {
            'contacts': [],
        }
        sorted_contacts['contacts'] = request_data.sort_contacts()

        return jsonify(sorted_contacts), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)