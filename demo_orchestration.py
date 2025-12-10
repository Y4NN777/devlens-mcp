"""
Demo: Smart Orchestration for LidgiCash API Research

This demonstrates how the orchestration system intelligently selects
tools and builds workflows for real-world research tasks.
"""

import sys
sys.path.insert(0, "src")

from webdocx.utils.orchestrator import suggest_tools, ResearchContext


def demo_lidgicash_integration():
    """Demonstrate smart workflow for LidgiCash API integration."""
    
    print("=" * 80)
    print("DEMO: Smart Research Orchestration")
    print("=" * 80)
    print()
    
    # Scenario 1: Starting from scratch
    print("📋 SCENARIO 1: Complete Unknown")
    print("-" * 80)
    query = "How can I integrate mobile payments with LidgiCash API in Cameroon?"
    print(f"Query: {query}\n")
    
    result = suggest_tools(query)
    
    print(f"🎯 Intent: {result['primary_intent']['type']} ({result['primary_intent']['confidence']:.0%})")
    print(f"   Reasoning: {result['primary_intent']['reasons'][0]}\n")
    
    print("🔧 Recommended Workflow:")
    for step in result['workflow']:
        print(f"\n   Step {step['step']}: {step['tool']}")
        print(f"   └─ {step['purpose']}")
        if step['suggested_parameters']:
            params = ', '.join(f"{k}={v}" for k, v in step['suggested_parameters'].items())
            print(f"      Parameters: {params}")
    
    print("\n" + "=" * 80)
    print()
    
    # Scenario 2: With known documentation URL
    print("📋 SCENARIO 2: Known Documentation URL")
    print("-" * 80)
    query = "LidgiCash API complete documentation and integration guide"
    context = ResearchContext(known_urls=["https://lidgicash.cm/documentation"])
    print(f"Query: {query}")
    print(f"Context: Known URL = https://lidgicash.cm/documentation\n")
    
    result = suggest_tools(query, context)
    
    print(f"🎯 Intent: {result['primary_intent']['type']} ({result['primary_intent']['confidence']:.0%})")
    print(f"   Keywords matched: {', '.join(result['primary_intent']['keywords'])}\n")
    
    print("🔧 Optimized Workflow (skips search):")
    for step in result['workflow']:
        print(f"\n   Step {step['step']}: {step['tool']}")
        print(f"   └─ {step['purpose']}")
        if step['suggested_parameters']:
            params = ', '.join(f"{k}={v}" for k, v in step['suggested_parameters'].items())
            print(f"      Parameters: {params}")
        print(f"      Cost: {step['tool_details']['resource_cost']} / {step['tool_details']['estimated_duration']}")
    
    print("\n" + "=" * 80)
    print()
    
    # Scenario 3: Comparison research
    print("📋 SCENARIO 3: Comparison Research")
    print("-" * 80)
    query = "Compare LidgiCash vs Orange Money vs MTN Mobile Money for Cameroon merchants"
    print(f"Query: {query}\n")
    
    result = suggest_tools(query)
    
    print(f"🎯 Intent: {result['primary_intent']['type']} ({result['primary_intent']['confidence']:.0%})")
    if result['secondary_intents']:
        print(f"   Secondary: {result['secondary_intents'][0]['type']} ({result['secondary_intents'][0]['confidence']:.0%})")
    print()
    
    print("🔧 Comparison Workflow:")
    for step in result['workflow']:
        parallel = f" [PARALLEL GROUP {step['parallel_group']}]" if step['parallel_group'] else ""
        fallback = " ⚠️" if step['has_fallback'] else ""
        print(f"\n   Step {step['step']}: {step['tool']}{parallel}{fallback}")
        print(f"   └─ {step['purpose']}")
        if step['suggested_parameters']:
            params = ', '.join(f"{k}={v}" for k, v in step['suggested_parameters'].items())
            print(f"      Parameters: {params}")
    
    print("\n" + "=" * 80)
    print()
    
    # Scenario 4: Deep research mode
    print("📋 SCENARIO 4: Comprehensive Deep Research")
    print("-" * 80)
    query = "Research everything about mobile payment integration in Cameroon - comprehensive analysis"
    print(f"Query: {query}\n")
    
    result = suggest_tools(query)
    
    print(f"🎯 Intent: {result['primary_intent']['type']} ({result['primary_intent']['confidence']:.0%})")
    print(f"   Matched: {', '.join(result['primary_intent']['keywords'])}\n")
    
    print("🔧 Deep Research Workflow:")
    for step in result['workflow']:
        print(f"\n   Step {step['step']}: {step['tool']}")
        print(f"   └─ {step['purpose']}")
        if step['suggested_parameters']:
            params = ', '.join(f"{k}={v}" for k, v in step['suggested_parameters'].items())
            print(f"      Parameters: {params}")
        print(f"      Best for: {step['tool_details']['best_for'][0]}")
    
    print("\n" + "=" * 80)
    print()
    
    # Summary
    print("✅ ORCHESTRATION FEATURES DEMONSTRATED:")
    print("   • Intent classification with confidence scores")
    print("   • Dynamic workflow generation based on context")
    print("   • Parameter optimization per intent (limit, depth, max_pages)")
    print("   • Parallel execution for comparison workflows")
    print("   • Skipping unnecessary steps when URLs are known")
    print("   • Resource cost estimation (fast/medium/slow)")
    print("   • Fallback strategies for error handling")
    print()
    print("=" * 80)


if __name__ == "__main__":
    demo_lidgicash_integration()
