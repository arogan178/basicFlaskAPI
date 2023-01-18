# Basic Flask API
This is a Flask API that provides endpoints for handling and aggregating data. The API has four main endpoints:

/api/Test: This endpoint returns the aggregate of all data stored in data.json file. It returns the latest date, mean of all weight data, mean of all error data and mean of all device data items.

/api/Data/PostTrainData: This endpoint allows the user to post some data and a mode to the server. The data is stored in data.txt file in the format of {data} ({mode}).

/api/Data/ViewData: This endpoint returns all the data stored in data.txt file.

/api/MorpheusData/PostValues: This endpoint allows the user to post data in json format. The json data contains weight data, device id, error, mode, device data and model date. The posted data is printed on the console and saved to a json file data.json.

## Installation
Install Flask using pip:
```pip install Flask```

Install json and statistics using pip:
```pip install json statistics```

## Usage
Run the api using the command:
```python app.py```

Use any client like postman to test the endpoints.

## Contributing
This is a simple API, contributions are welcome. If you want to contribute, please fork the repository and make changes as you wish. Pull requests are warmly welcome.
