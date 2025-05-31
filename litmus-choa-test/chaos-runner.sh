#!/bin/bash

# Chaos Experiment Runner
# This script helps run and manage chaos experiments

set -e

EXPERIMENT_DIR="$HOME/chaos-experiments"

show_help() {
    echo "🧪 Chaos Experiment Runner"
    echo "=========================="
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  list           - List all available experiments"
    echo "  run <name>     - Run a specific experiment"
    echo "  status         - Show status of running experiments"
    echo "  stop <name>    - Stop a specific experiment"
    echo "  cleanup        - Clean up all experiments"
    echo "  logs <name>    - Show logs for an experiment"
    echo ""
    echo "Available experiments:"
    echo "  pod-delete     - Randomly delete pods"
    echo "  network-chaos  - Introduce network issues"
    echo "  cpu-hog        - Consume CPU resources"
    echo ""
    echo "Examples:"
    echo "  $0 run pod-delete"
    echo "  $0 status"
    echo "  $0 stop pod-delete"
}

list_experiments() {
    echo "📋 Available Experiments:"
    echo "========================="
    echo "1. pod-delete     - Randomly deletes application pods"
    echo "2. network-chaos  - Introduces network packet loss"
    echo "3. cpu-hog        - Consumes CPU resources on pods"
    echo ""
    echo "📁 Experiment files location: $EXPERIMENT_DIR"
}

run_experiment() {
    local exp_name=$1
    
    case $exp_name in
        "pod-delete")
            echo "🚀 Running Pod Delete Experiment..."
            kubectl apply -f $EXPERIMENT_DIR/pod-delete-experiment.yaml
            ;;
        "network-chaos")
            echo "🚀 Running Network Chaos Experiment..."
            kubectl apply -f $EXPERIMENT_DIR/network-chaos-experiment.yaml
            ;;
        "cpu-hog")
            echo "🚀 Running CPU Hog Experiment..."
            kubectl apply -f cpu-hog-experiment.yaml
            ;;
        *)
            echo "❌ Unknown experiment: $exp_name"
            echo "Use '$0 list' to see available experiments"
            exit 1
            ;;
    esac
    
    echo "✅ Experiment started successfully!"
    echo "💡 Monitor with: $0 status"
}

show_status() {
    echo "🔍 Chaos Experiment Status:"
    echo "==========================="
    
    echo ""
    echo "🧪 Active Chaos Engines:"
    kubectl get chaosengines --all-namespaces
    
    echo ""
    echo "📊 Chaos Results:"
    kubectl get chaosresults --all-namespaces
    
    echo ""
    echo "🔄 Pod Status in Target Namespace:"
    kubectl get pods -n chaos-apps
}

stop_experiment() {
    local exp_name=$1
    
    case $exp_name in
        "pod-delete")
            kubectl delete chaosengine nginx-pod-delete -n chaos-apps 2>/dev/null || echo "No pod-delete experiment running"
            ;;
        "network-chaos")
            kubectl delete chaosengine nginx-network-loss -n chaos-apps 2>/dev/null || echo "No network-chaos experiment running"
            ;;
        "cpu-hog")
            kubectl delete chaosengine cpu-hog-experiment -n chaos-apps 2>/dev/null || echo "No cpu-hog experiment running"
            ;;
        *)
            echo "❌ Unknown experiment: $exp_name"
            exit 1
            ;;
    esac
    
    echo "✅ Experiment stopped successfully!"
}

cleanup_all() {
    echo "🧹 Cleaning up all chaos experiments..."
    
    kubectl delete chaosengines --all --all-namespaces 2>/dev/null || echo "No chaos engines to delete"
    kubectl delete chaosresults --all --all-namespaces 2>/dev/null || echo "No chaos results to delete"
    
    echo "✅ Cleanup completed!"
}

show_logs() {
    local exp_name=$1
    
    echo "📝 Logs for experiment: $exp_name"
    echo "================================="
    
    # Get the chaos engine pod
    case $exp_name in
        "pod-delete")
            engine_name="nginx-pod-delete"
            ;;
        "network-chaos")
            engine_name="nginx-network-loss"
            ;;
        "cpu-hog")
            engine_name="cpu-hog-experiment"
            ;;
        *)
            echo "❌ Unknown experiment: $exp_name"
            exit 1
            ;;
    esac
    
    # Show chaos engine details
    kubectl describe chaosengine $engine_name -n chaos-apps 2>/dev/null || echo "Experiment not found or not running"
    
    # Show chaos result
    echo ""
    echo "📊 Chaos Results:"
    kubectl describe chaosresult $engine_name -n chaos-apps 2>/dev/null || echo "No results available yet"
}

# Main script logic
case "${1:-help}" in
    "help"|"-h"|"--help")
        show_help
        ;;
    "list")
        list_experiments
        ;;
    "run")
        if [ -z "$2" ]; then
            echo "❌ Please specify an experiment name"
            echo "Use '$0 list' to see available experiments"
            exit 1
        fi
        run_experiment "$2"
        ;;
    "status")
        show_status
        ;;
    "stop")
        if [ -z "$2" ]; then
            echo "❌ Please specify an experiment name to stop"
            exit 1
        fi
        stop_experiment "$2"
        ;;
    "cleanup")
        cleanup_all
        ;;
    "logs")
        if [ -z "$2" ]; then
            echo "❌ Please specify an experiment name"
            exit 1
        fi
        show_logs "$2"
        ;;
    *)
        echo "❌ Unknown command: $1"
        show_help
        exit 1
        ;;
esac
