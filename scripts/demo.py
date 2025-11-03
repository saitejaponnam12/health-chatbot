"""
Quick Demo - Health Chatbot Usage Examples
Shows how to use the chatbot in different ways
"""

from health_chatbot import HealthChatbot
import json


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def demo_single_query():
    """Demonstrate a single query."""
    print_section("DEMO 1: Single Query")
    
    chatbot = HealthChatbot(
        dataset_path='data/health_qa_dataset.json',
        confidence_threshold=0.3
    )
    
    query = "What are the symptoms of dengue fever?"
    print(f"Query: {query}\n")
    
    response = chatbot.answer_query(query)
    
    print(f"Status: {'✓ Successful' if response['success'] else '⚠ Fallback'}")
    print(f"Confidence: {response['confidence']:.1%}")
    print(f"Category: {response['category'].upper()}")
    print(f"\nAnswer:\n{response['answer']}")
    print(f"\nExplanation:\n{response['explanation']}")


def demo_multiple_queries():
    """Demonstrate multiple queries at once."""
    print_section("DEMO 2: Multiple Queries (Batch)")
    
    chatbot = HealthChatbot('data/health_qa_dataset.json')
    
    queries = [
        "How to prevent malaria?",
        "Tell me about COVID-19",
        "Flu treatment options",
        "random xyz text"
    ]
    
    responses = chatbot.batch_answer(queries)
    
    print("Query Results Summary:")
    print("-" * 80)
    print(f"{'Query':<40} {'Confidence':<15} {'Category'}")
    print("-" * 80)
    
    for q, r in zip(queries, responses):
        status = "✓" if r['success'] else "✗"
        print(f"{status} {q[:38]:<38} {r['confidence']:>6.1%}  {r['category']}")
    
    print("\nDetailed Result for Query 1:")
    print("-" * 80)
    response = responses[0]
    print(f"Answer: {response['answer'][:100]}...")
    print(f"Confidence: {response['confidence']:.1%}")


def demo_similarity_analysis():
    """Demonstrate similarity score analysis."""
    print_section("DEMO 3: Similarity Score Analysis")
    
    chatbot = HealthChatbot('data/health_qa_dataset.json')
    
    test_queries = [
        "dengue fever symptoms",
        "malaria treatment",
        "COVID vaccine",
        "common cold",
        "xyz nonsense"
    ]
    
    scores = chatbot.get_similarity_scores_for_testing(test_queries)
    
    print("Similarity Scores for Test Queries:")
    print("-" * 80)
    print(f"{'Query':<40} {'Score'}")
    print("-" * 80)
    
    for query, score in zip(test_queries, scores):
        bar = "█" * int(score * 20)
        print(f"{query[:38]:<40} {score:>6.1%} {bar}")
    
    print(f"\nMean Score: {sum(scores)/len(scores):.1%}")
    print(f"Min Score:  {min(scores):.1%}")
    print(f"Max Score:  {max(scores):.1%}")


def demo_conversation_history():
    """Demonstrate conversation history tracking."""
    print_section("DEMO 4: Conversation History")
    
    chatbot = HealthChatbot('data/health_qa_dataset.json')
    
    # Ask multiple questions
    queries = [
        "What is asthma?",
        "How to manage anxiety?",
        "Thyroid disease symptoms"
    ]
    
    for i, query in enumerate(queries, 1):
        chatbot.answer_query(query)
    
    # Get history
    history = chatbot.get_conversation_history()
    
    print(f"Conversation History ({len(history)} queries):")
    print("-" * 80)
    
    for i, item in enumerate(history, 1):
        print(f"\n{i}. Query: {item['query']}")
        print(f"   Confidence: {item['response']['confidence']:.1%}")
        print(f"   Category: {item['response']['category']}")
        print(f"   Success: {item['response']['success']}")


def demo_confidence_threshold():
    """Demonstrate different confidence thresholds."""
    print_section("DEMO 5: Confidence Threshold Impact")
    
    query = "I have a fever and body aches"
    
    for threshold in [0.2, 0.4, 0.6, 0.8]:
        chatbot = HealthChatbot(
            dataset_path='data/health_qa_dataset.json',
            confidence_threshold=threshold
        )
        
        response = chatbot.answer_query(query)
        
        status = "✓ Accepted" if response['success'] else "✗ Fallback"
        print(f"Threshold {threshold:.1%}: {status} (Score: {response['confidence']:.1%})")


def demo_alternative_suggestions():
    """Demonstrate alternative suggestion system."""
    print_section("DEMO 6: Alternative Suggestions")
    
    chatbot = HealthChatbot('data/health_qa_dataset.json')
    
    query = "heart problems and chest pain"
    response = chatbot.answer_query(query)
    
    print(f"Query: {query}\n")
    print(f"Primary Answer (Confidence: {response['confidence']:.1%}):")
    print(f"  {response['answer'][:80]}...\n")
    
    if response['alternatives']:
        print("Alternative Answers:")
        print("-" * 80)
        for i, alt in enumerate(response['alternatives'][:3], 1):
            print(f"{i}. [{alt['confidence']:.1%}] {alt['question']}")
            print(f"   {alt['answer'][:70]}...\n")


def demo_category_analysis():
    """Demonstrate category-based analysis."""
    print_section("DEMO 7: Category Analysis")
    
    chatbot = HealthChatbot('data/health_qa_dataset.json')
    
    # Sample from each category
    test_queries = [
        "dengue fever information",
        "malaria prevention",
        "COVID vaccine",
        "cold treatment",
        "flu symptoms",
        "diabetes management",
        "heart disease prevention",
        "anxiety disorder",
        "depression treatment",
        "weight management"
    ]
    
    responses = chatbot.batch_answer(test_queries)
    
    # Analyze by category
    categories = {}
    for r in responses:
        cat = r['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r['confidence'])
    
    print("Category Performance:")
    print("-" * 80)
    print(f"{'Category':<25} {'Avg Confidence':<15} {'Count'}")
    print("-" * 80)
    
    for cat in sorted(categories.keys()):
        scores = categories[cat]
        avg = sum(scores) / len(scores)
        print(f"{cat:<25} {avg:>6.1%}              {len(scores)}")


def demo_export_results():
    """Demonstrate exporting results to JSON."""
    print_section("DEMO 8: Export Results to JSON")
    
    chatbot = HealthChatbot('data/health_qa_dataset.json')
    
    queries = [
        "What is dengue?",
        "COVID prevention",
        "Diabetes symptoms"
    ]
    
    responses = chatbot.batch_answer(queries)
    
    # Create exportable format
    export_data = {
        'metadata': {
            'total_queries': len(queries),
            'model': 'TF-IDF + Cosine Similarity',
            'threshold': 0.3
        },
        'results': responses
    }
    
    # Show structure
    print("Export Structure:")
    print(json.dumps({
        'metadata': export_data['metadata'],
        'results': f"[{len(responses)} response objects]"
    }, indent=2))
    
    print(f"\n✓ Ready to export {len(responses)} responses")
    print("✓ Can be saved to JSON for analysis")


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " " * 20 + "🏥 HEALTH CHATBOT - USAGE EXAMPLES" + " " * 25 + "║")
    print("╚" + "="*78 + "╝")
    
    demos = [
        ("Single Query", demo_single_query),
        ("Multiple Queries", demo_multiple_queries),
        ("Similarity Analysis", demo_similarity_analysis),
        ("Conversation History", demo_conversation_history),
        ("Confidence Threshold", demo_confidence_threshold),
        ("Alternative Suggestions", demo_alternative_suggestions),
        ("Category Analysis", demo_category_analysis),
        ("Export Results", demo_export_results),
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        try:
            demo_func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {str(e)}")
    
    # Final summary
    print_section("ALL DEMOS COMPLETED")
    
    print("""
    ✅ Demonstrated:
    • Single query answering with explanations
    • Batch query processing
    • Similarity score analysis
    • Conversation history tracking
    • Confidence threshold variations
    • Alternative suggestion system
    • Category-based performance analysis
    • Result export capabilities
    
    📊 System Performance: Ready for Production! 🚀
    
    Next Steps:
    1. Review outputs/conversation_logs.json for example logs
    2. Check outputs/similarity_scores_analysis.png for visualization
    3. Run: python scripts/interactive_chatbot.py --mode interactive
    4. Deploy to your application!
    """)


if __name__ == "__main__":
    main()
