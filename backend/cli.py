import argparse
from dotenv import load_dotenv
from app.agents.sre_agent import SREAgent

# Load environment variables from .env.local
load_dotenv('.env.local')

def main():
    parser = argparse.ArgumentParser(description="SRE Question CLI")
    parser.add_argument("--question", type=str, required=True, help="The SRE question to ask.")
    args = parser.parse_args()

    agent = SREAgent()
    response = agent.ask_question(args.question)
    print(response)

if __name__ == "__main__":
    main()