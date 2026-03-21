import argparse
from src.agent.core import CrestaAIAgent

# A simple set of test cases to evaluate reasoning and tool usage
TEST_CASES = [
    {
        "query": "What is the status of my order ORD-12345?",
        "expected_tool": "check_order_status",
        "expected_answer_snippet": "Shipped"
    },
    {
        "query": "How do I reset my password?",
        "expected_tool": "search_knowledge_base",
        "expected_answer_snippet": "settings > security"
    },
    {
        "query": "Who is the user USER-001 and what plan are they on?",
        "expected_tool": "get_customer_info",
        "expected_answer_snippet": "Pro"
    }
]

def run_evaluation():
    print("Starting Agent Evaluation...")
    agent = CrestaAIAgent()
    
    passed = 0
    total = len(TEST_CASES)
    
    for i, test in enumerate(TEST_CASES):
        print(f"\\n--- Running Test {i+1}/{total} ---")
        print(f"Query: {test['query']}")
        
        try:
            result = agent.get_response(test["query"])
            
            # Extract tools used from intermediate steps
            tools_used = [action.tool for action, _ in result.get("intermediate_steps", [])]
            
            tool_matched = test["expected_tool"] in tools_used
            answer_matched = test["expected_answer_snippet"].lower() in result["answer"].lower()
            
            if tool_matched and answer_matched:
                print("✅ Passed!")
                passed += 1
            else:
                print("❌ Failed!")
                print(f"Expected tool '{test['expected_tool']}', got {tools_used}")
                print(f"Expected answer snippet '{test['expected_answer_snippet']}', got {result['answer']}")
                
        except Exception as e:
            print(f"❌ Failed with error: {e}")

    print(f"\\nEvaluation Complete! Score: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
if __name__ == "__main__":
    run_evaluation()
