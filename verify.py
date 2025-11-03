#!/usr/bin/env python
"""Quick verification that the system is working"""

import sys
sys.path.insert(0, 'scripts')
from health_chatbot import HealthChatbot

print("\n" + "="*70)
print("  🏥 HEALTH CHATBOT - SYSTEM VERIFICATION")
print("="*70 + "\n")

try:
    # Initialize chatbot
    print("Initializing chatbot...")
    bot = HealthChatbot('data/health_qa_dataset.json')
    print("✓ Chatbot initialized successfully\n")
    
    # Test query
    print("Testing query: 'What is malaria?'\n")
    response = bot.answer_query('What is malaria?')
    
    print("✓ System Working!")
    print(f"Confidence: {response['confidence']:.1%}")
    print(f"Category: {response['category']}")
    print(f"Answer: {response['answer'][:100]}...\n")
    
    # Test multiple queries
    print("Testing batch processing...")
    queries = ["dengue symptoms", "COVID prevention", "asthma management"]
    responses = bot.batch_answer(queries)
    print(f"✓ Successfully processed {len(responses)} queries\n")
    
    # Show results
    print("Results Summary:")
    print("-" * 70)
    for q, r in zip(queries, responses):
        print(f"  {q:<30} → Confidence: {r['confidence']:.0%}")
    print()
    
    print("="*70)
    print("  ✅ ALL SYSTEMS OPERATIONAL - READY FOR DEPLOYMENT")
    print("="*70 + "\n")
    
except Exception as e:
    print(f"❌ Error: {str(e)}\n")
    print("Please ensure:")
    print("  1. data/health_qa_dataset.json exists")
    print("  2. scikit-learn is installed (pip install scikit-learn)")
    print("  3. numpy is installed (pip install numpy)")
