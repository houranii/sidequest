# HomeTask Rev

HomeTask Rev is a Flask application designed to handle user birthdays. It provides a simple REST API to store and retrieve user's birthday information and calculate the number of days until their next birthday.

## Features

- Store user's birthday information.
- Retrieve a birthday message for a user.
- Validate username and date of birth inputs.
- Logging of errors and informational messages.
- Security headers added to responses.
- Prometheus metrics integration for monitoring.
- CORS support for cross-origin requests.

## Installation

To install the application, you need to have Python 3.7 or higher. Clone the repository and install the dependencies:

``` bash
git clone https://github.com/houranii/hometask_rev.git
cd hometask_rev
pip install -e .
```

## Usage

To start the application, run:
``` bash
docker compose up --build -d
```

The application will start on `http://127.0.0.1:5000/`.

## API Endpoints

- `PUT /hello/<username>`: Update or create a user's birthday information.
- `GET /hello/<username>`: Get a birthday message for the user.

## Development

To contribute to the project, you can follow the standard git workflow:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/fooBar`).
3. Commit your changes (`git commit -am 'Add some fooBar'`).
4. Push to the branch (`git push origin feature/fooBar`).
5. Create a new Pull Request.

## Testing

To run the tests, install the test dependencies and run `pytest`:
``` bash
pip install '.[test]'
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Ahmad Hourani - ahmed.hourani@gmail.com