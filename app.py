from flask import Flask, request, jsonify
from datetime import datetime, timezone
import json
from statistics import mean

app = Flask(__name__)


@app.route('/api/Test')
def aggregate_weights():
    try:
        with open("data.json", "r") as f:
            json_data = json.load(f)

        weight_data = []
        error_data = []
        totalDataItem = []
        latest_date = datetime.fromtimestamp(0, tz=timezone.utc)

        for item in json_data:
            if "Weight Data" in item:
                if len(weight_data) == 0:
                    weight_data = item["Weight Data"]
                elif len(weight_data) == len(item["Weight Data"]):
                    for i in range(len(weight_data)):
                        weight_data[i] += item["Weight Data"][i]

        for item in json_data:
            if "Error" in item:
                error_data.append(float(item["Error"]))

        for item in json_data:
            if "Device Data" in item:
                totalDataItem.append(int(item["Device Data"]))

        for item in json_data:
            item_date = datetime.fromisoformat(
                item["Date"]).replace(tzinfo=timezone.utc)
            if item_date > latest_date:
                latest_date = item_date

        if weight_data:  # check if data is not empty
            weight_data = [value / len(json_data) for value in weight_data]

        if error_data:  # check if data is not empty
            error_data = sum(error_data) / len(error_data)

        if totalDataItem:  # check if data is not empty
            totalDataItem = sum(totalDataItem) / len(totalDataItem)

        return jsonify({"Date": latest_date, "ModelData": json.dumps(weight_data), "Error": error_data, "totalDataItems": int(totalDataItem)})

    except json.decoder.JSONDecodeError:
        return jsonify({}), 404


@app.route('/api/Data/PostTrainData')
def post_train_data_endpoint():
    # code to handle the request and return a response goes here
    # you can access the "data" and "mode" query parameters using the request.args object
    data = request.args.get('data')
    mode = request.args.get('mode')
    # store the data in a file
    open('data.txt', 'a').close()
    with open('data.txt', 'a') as f:
        f.write(f'{data} ({mode})\n')

    return 'Data stored successfully'


@app.route('/api/Data/ViewData')
def view_data_endpoint():
    # code to handle the request and return a response goes here
    # create the file if it does not exist
    open('data.txt', 'a').close()

    # read the data from the file
    with open('data.txt', 'r') as f:
        data = f.read()

    return data


@app.route('/api/MorpheusData/PostValues', methods=['POST'])
def post_weights():
    json_data = request.json
    data = json_data['data'].split(",")
    weight_data = [float(x) for x in data]
    device_id = json_data['device']
    error = json_data['error']
    mode = json_data['mode']
    device_data = json_data['deviceData']
    model_date = json_data['modelDate']

    # Do something with the data, like saving it to a database or processing it
    print("Weight Data:", weight_data)
    print("Device ID:", device_id)
    print("Error:", error)
    print("Mode:", mode)
    print("Device Data:", device_data)
    print("Model Date", model_date)

    # Saving data to a JSON file
    new_data = {"Date": model_date,
                "Weight Data": weight_data,
                "Device ID": device_id,
                "Error": error,
                "Mode": mode,
                "Device Data": device_data}
    try:
        with open("data.json", "r") as f:
            json_data = json.load(f)
    except json.decoder.JSONDecodeError:
        json_data = []
    json_data.append(new_data)

    with open("data.json", "w") as f:
        json.dump(json_data, f)
    return "Success"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=True, debug=True)
