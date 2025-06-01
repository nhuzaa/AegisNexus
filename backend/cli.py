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
    parser = argparse.ArgumentParser(
        description="AI Agent Question CLI with SRE Tools"
    )
    parser.add_argument(
        "-q", "--question", type=str,
        help="The question to ask the agent."
    )
    parser.add_argument(
        "-a", "--agent", type=str, default="sre_agent",
        help="Agent name to use (default: sre_agent)."
    )
    parser.add_argument(
        "--incident", type=str, nargs=2, metavar=('ALERT_NAME', 'SEVERITY'),
        help="Trigger incident response workflow. "
             "Usage: --incident 'HighCPU' 'critical'"
    )
    parser.add_argument(
        "--health", action="store_true",
        help="Get system health report"
    )
    parser.add_argument(
        "--demo", action="store_true",
        help="Run SRE tools demo"
    )
    parser.add_argument(
        "--tools-health", action="store_true",
        help="Check SRE tools health status"
    )

    args = parser.parse_args()

    try:
        agent = get_agent(args.agent)

        # Handle different command types
        if args.demo:
            print("🎬 Running SRE Tools Demo...")
            from app.tools.sre_tools import demo_sre_tools
            demo_sre_tools()
            return

        if args.tools_health:
            print("🔧 Checking SRE Tools Health...")
            health_status = agent.tools.health_check()
            pp = pprint.PrettyPrinter(indent=2, width=80, depth=None)
            pp.pprint(health_status)
            return

        if args.health:
            print("🏥 Generating System Health Report...")
            response = agent.get_system_health()
        elif args.incident:
            alert_name, severity = args.incident
            print(f"🚨 Triggering Incident Response for '{alert_name}' "
                  f"(severity: {severity})")
            response = agent.execute_incident_response(alert_name, severity)
        elif args.question:
            print(f"❓ Asking question: {args.question}")
            response = agent.ask_question(args.question)
        else:
            parser.print_help()
            return

        # Pretty print the response
        pp = pprint.PrettyPrinter(indent=2, width=80, depth=None)
        print(f"\n🤖 Agent: {args.agent}")
        if args.question:
            print(f"❓ Question: {args.question}")
        print("📋 Response:")
        pp.pprint(response)

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()