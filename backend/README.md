# SRE Agent API

## Overview
The SRE Agent API is a FastAPI application that allows users to ask Site Reliability Engineering (SRE) questions through a dedicated endpoint. It utilizes LangGraph and Llama-API to process and respond to these inquiries.

## Project Structure
```
sre-agent-api
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── agents
│   │   ├── __init__.py
│   │   └── sre_agent.py
│   ├── services
│   │   ├── __init__.py
│   │   └── llm_service.py
│   ├── models
│   │   ├── __init__.py
│   │   └── request_models.py
│   └── routes
│       ├── __init__.py
│       └── sre.py
├── tests
│   ├── __init__.py
│   ├── test_main.py
│   └── test_sre_agent.py
├── cli.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation
To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd sre-agent-api
pip install -r requirements.txt
```

## Usage
To run the FastAPI application, execute the following command:

```bash
uvicorn app.main:app --reload
```

This will start the server at `http://127.0.0.1:8000`.

### Asking SRE Questions
You can send a POST request to the `/sre/ask` endpoint with a JSON body containing your question. For example:

```json
{
  "question": "What is the role of an SRE?"
}
```

### Command Line Interface
You can also ask questions directly from the command line using the `cli.py` script:

```bash
python cli.py --question "What is the role of an SRE?"
```

## Environment Variables
Create a `.env` file in the root directory based on the `.env.example` file to configure any necessary environment variables for the application.

## Testing
To run the tests, use the following command:

```bash
pytest
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.