from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from uuid import uuid4
import datetime
import math

app = Flask(__name__)
CORS(app)  # Enable CORS
api = Api(app)

receipts = {}

def calculate_points(receipt):
    points = 0

    # 1. One point for every alphanumeric character in the retailer name.
    points += sum(char.isalnum() for char in receipt['retailer'])

    # 2. 50 points if the total is a round dollar amount with no cents.
    total = float(receipt['total'])
    if total == math.floor(total):
        points += 50

    # 3. 25 points if the total is a multiple of 0.25.
    if total % 0.25 == 0:
        points += 25

    # 4. 5 points for every two items on the receipt.
    points += (len(receipt['items']) // 2) * 5

    # 5. If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer.
    for item in receipt['items']:
        description_length = len(item['shortDescription'].strip())
        if description_length % 3 == 0:
            item_price = float(item['price'])
            points += math.ceil(item_price * 0.2)

    # 6. 6 points if the day in the purchase date is odd.
    purchase_date = datetime.datetime.strptime(receipt['purchaseDate'], '%Y-%m-%d')
    if purchase_date.day % 2 != 0:
        points += 6

    # 7. 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    purchase_time = datetime.datetime.strptime(receipt['purchaseTime'], '%H:%M')
    if 14 <= purchase_time.hour < 16:
        points += 10

    return points

class ProcessReceipts(Resource):
    def post(self):
        receipt = request.json
        receipt_id = str(uuid4())
        points = calculate_points(receipt)
        receipts[receipt_id] = {
            "receipt": receipt,
            "points": points
        }
        return jsonify({"id": receipt_id})

class GetPoints(Resource):
    def get(self, receipt_id):
        if receipt_id not in receipts:
            return {"error": "Receipt not found"}, 404
        return jsonify({"points": receipts[receipt_id]["points"]})

class GetAllReceipts(Resource):
    def get(self):
        all_receipts = [{"id": rid, "receipt": data["receipt"]} for rid, data in receipts.items()]
        return jsonify(all_receipts)

api.add_resource(ProcessReceipts, '/receipts/process')
api.add_resource(GetPoints, '/receipts/<string:receipt_id>/points')
api.add_resource(GetAllReceipts, '/receipts')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
