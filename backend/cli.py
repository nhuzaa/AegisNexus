import argparse
import pprint
from dotenv import load_dotenv
from app.agents.sre_agent import SREAgent

# Load environment variables from .env.local
load_dotenv('.env.local')

def get_agent(agent_name: str):
    """Factory function to get agent by name"""
    agents = {
        'sre_agent': SREAgent,
        'sre': SREAgent,  # Allow short form
    }
    
    if agent_name.lower() not in agents:
        available_agents = ', '.join(agents.keys())
        raise ValueError(f"Unknown agent '{agent_name}'. Available agents: {available_agents}")
    
    return agents[agent_name.lower()]()

def main():
    parser = argparse.ArgumentParser(description="AI Agent Question CLI")
    parser.add_argument("-q", "--question", type=str, required=True, 
                       help="The question to ask the agent.")
    parser.add_argument("-a", "--agent", type=str, default="sre_agent", 
                       help="Agent name to use (default: sre_agent).")
    args = parser.parse_args()

    try:
        agent = get_agent(args.agent)
        response = agent.ask_question(args.question)
        
        # Pretty print the response
        pp = pprint.PrettyPrinter(indent=2, width=80, depth=None)
        print(f"\n🤖 Agent: {args.agent}")
        print(f"❓ Question: {args.question}")
        print("📋 Response:")
        pp.pprint(response)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()