"""
Interactive Health Chatbot with Conversation Logs and Examples
Demonstrates the chatbot with real-world health queries
"""

import json
import sys
import numpy as np
from pathlib import Path
from health_chatbot import HealthChatbot
from datetime import datetime


class InteractiveChatbot:
    """Interactive interface for the Health Chatbot."""
    
    def __init__(self, dataset_path: str):
        """Initialize the interactive chatbot."""
        self.chatbot = HealthChatbot(
            dataset_path=dataset_path,
            confidence_threshold=0.3
        )
    
    def format_response(self, response: dict, query: str) -> str:
        """Format response for console display."""
        output = []
        output.append("\n" + "="*80)
        output.append("USER QUERY")
        output.append("="*80)
        output.append(f"❓ {query}")
        
        output.append("\n" + "="*80)
        output.append("CHATBOT RESPONSE")
        output.append("="*80)
        
        if response['success']:
            output.append(f"✓ STATUS: Success")
            output.append(f"📁 CATEGORY: {response['category'].replace('-', ' ').title()}")
            output.append(f"🎯 CONFIDENCE: {response['confidence']:.1%}")
            output.append("")
            output.append("📝 ANSWER:")
            output.append("-" * 80)
            output.append(response['answer'])
            output.append("-" * 80)
        else:
            output.append(f"⚠ STATUS: Low Confidence")
            output.append(f"🎯 CONFIDENCE: {response['confidence']:.1%}")
            output.append("")
            output.append("📝 RESPONSE:")
            output.append("-" * 80)
            output.append(response['answer'])
            output.append("-" * 80)
        
        output.append("")
        output.append("💡 EXPLANATION:")
        output.append("-" * 80)
        output.append(response['explanation'])
        output.append("-" * 80)
        
        if response.get('matched_question'):
            output.append("")
            output.append(f"🔗 MATCHED ORIGINAL QUESTION: {response['matched_question']}")
        
        if response.get('alternatives'):
            output.append("")
            output.append("📌 ALTERNATIVE MATCHES:")
            for i, alt in enumerate(response['alternatives'][:2], 1):
                output.append(f"  {i}. [{alt['confidence']:.1%}] {alt['question']}")
        
        output.append("\n" + "="*80 + "\n")
        return "\n".join(output)
    
    def interactive_mode(self):
        """Run interactive chatbot mode."""
        print("\n" + "="*80)
        print("🏥 HEALTH CHATBOT - INTERACTIVE MODE")
        print("="*80)
        print("Ask health-related questions. Type 'quit' to exit, 'history' for conversation log.\n")
        
        while True:
            try:
                query = input("👤 You: ").strip()
                
                if query.lower() == 'quit':
                    print("\n👋 Thank you for using Health Chatbot. Stay healthy!")
                    break
                
                if query.lower() == 'history':
                    self._print_conversation_history()
                    continue
                
                if not query:
                    continue
                
                response = self.chatbot.answer_query(query)
                print(self.format_response(response, query))
                
            except KeyboardInterrupt:
                print("\n\n👋 Conversation ended.")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")
    
    def _print_conversation_history(self):
        """Print the conversation history."""
        history = self.chatbot.get_conversation_history()
        if not history:
            print("\n📋 No conversation history yet.\n")
            return
        
        print("\n" + "="*80)
        print("📋 CONVERSATION HISTORY")
        print("="*80)
        for i, item in enumerate(history, 1):
            print(f"\n{i}. [{item['timestamp']}]")
            print(f"   Query: {item['query']}")
            print(f"   Confidence: {item['response']['confidence']:.1%}")
            print(f"   Category: {item['response']['category']}")
        print("\n" + "="*80 + "\n")
    
    def run_examples(self, examples: list) -> dict:
        """Run example conversations and log results."""
        print("\n" + "="*80)
        print("🔬 RUNNING EXAMPLE CONVERSATIONS")
        print("="*80)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_queries': len(examples),
            'conversations': []
        }
        
        for i, query in enumerate(examples, 1):
            print(f"\n[{i}/{len(examples)}] Processing: {query}")
            response = self.chatbot.answer_query(query)
            
            results['conversations'].append({
                'query_number': i,
                'query': query,
                'response': response
            })
        
        print(f"\n✓ Processed {len(examples)} example queries\n")
        return results


def generate_example_logs():
    """Generate example conversation logs."""
    
    # Initialize chatbot
    bot = InteractiveChatbot(
        dataset_path='data/health_qa_dataset.json'
    )
    
    # Define 10 example queries covering different health topics
    example_queries = [
        "What is dengue fever and how does it spread?",
        "Tell me about COVID-19 symptoms and prevention",
        "I have symptoms like high fever, body aches, and headache. What could it be?",
        "How can I prevent malaria when traveling to endemic areas?",
        "What are the risk factors for high blood pressure?",
        "I've been feeling tired and gaining weight unexpectedly",
        "How is influenza different from common cold?",
        "What should I do if I have severe joint pain?",
        "I'm experiencing heart palpitations and shortness of breath",
        "Can stress cause physical health problems?",
    ]
    
    # Run examples
    results = bot.run_examples(example_queries)
    
    # Format for logging
    log_output = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_conversations': len(results['conversations']),
            'model': 'TF-IDF with Cosine Similarity',
            'confidence_threshold': 0.3
        },
        'conversations': []
    }
    
    # Process each conversation
    for conv in results['conversations']:
        query = conv['query']
        response = conv['response']
        
        log_entry = {
            'conversation_id': conv['query_number'],
            'timestamp': datetime.now().isoformat(),
            'user_input': query,
            'chatbot_response': {
                'success': response['success'],
                'answer': response['answer'],
                'confidence': response['confidence'],
                'category': response['category'],
                'confidence_percentage': f"{response['confidence']:.1%}",
                'explanation': response['explanation'],
                'matched_original_question': response.get('matched_question', 'N/A'),
            },
            'quality_metrics': {
                'similarity_score': response['confidence'],
                'has_alternatives': len(response.get('alternatives', [])) > 0,
                'num_alternatives': len(response.get('alternatives', []))
            }
        }
        
        log_output['conversations'].append(log_entry)
    
    # Save logs to file
    output_path = Path('outputs/conversation_logs.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(log_output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Conversation logs saved to: {output_path}")
    
    # Print summary
    print("\n" + "="*80)
    print("📊 CONVERSATION SUMMARY")
    print("="*80)
    
    successful = sum(1 for c in log_output['conversations'] 
                    if c['chatbot_response']['success'])
    fallback = sum(1 for c in log_output['conversations'] 
                   if not c['chatbot_response']['success'])
    
    print(f"Total Conversations: {len(log_output['conversations'])}")
    print(f"Successful Matches: {successful}")
    print(f"Fallback Responses: {fallback}")
    print(f"Average Confidence: {np.mean([c['quality_metrics']['similarity_score'] for c in log_output['conversations']]):.1%}")
    
    print("\n📝 Sample Conversation Details:")
    print("-" * 80)
    
    for i, conv in enumerate(log_output['conversations'][:3], 1):
        print(f"\n{i}. Query: {conv['user_input']}")
        print(f"   Answer: {conv['chatbot_response']['answer'][:100]}...")
        print(f"   Confidence: {conv['chatbot_response']['confidence_percentage']}")
        print(f"   Category: {conv['chatbot_response']['category']}")
    
    print("\n" + "="*80 + "\n")
    
    return log_output


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Health Chatbot Interface')
    parser.add_argument('--mode', choices=['interactive', 'examples'], 
                       default='examples',
                       help='Run mode: interactive or examples')
    
    args = parser.parse_args()
    
    if args.mode == 'interactive':
        bot = InteractiveChatbot(dataset_path='data/health_qa_dataset.json')
        bot.interactive_mode()
    else:
        # Generate example conversation logs
        generate_example_logs()


if __name__ == "__main__":
    main()
