"""
Visualization and Analysis of Chatbot Performance
Generates histograms and statistical analysis of similarity scores
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from health_chatbot import HealthChatbot


class ChatbotAnalyzer:
    """Analyze and visualize chatbot performance metrics."""
    
    def __init__(self, dataset_path: str):
        """Initialize analyzer with chatbot."""
        self.chatbot = HealthChatbot(
            dataset_path=dataset_path,
            confidence_threshold=0.3
        )
    
    def analyze_test_queries(self, test_queries: list) -> dict:
        """
        Analyze similarity scores for test queries.
        
        Args:
            test_queries: List of test queries
            
        Returns:
            Dictionary with analysis results
        """
        scores = []
        responses = []
        
        print("\n🔍 Analyzing test queries...")
        
        for query in test_queries:
            response = self.chatbot.answer_query(query)
            responses.append(response)
            scores.append(response['confidence'])
        
        # Calculate statistics
        analysis = {
            'num_queries': len(test_queries),
            'scores': scores,
            'mean_confidence': float(np.mean(scores)),
            'median_confidence': float(np.median(scores)),
            'std_confidence': float(np.std(scores)),
            'min_confidence': float(np.min(scores)),
            'max_confidence': float(np.max(scores)),
            'successful_matches': sum(1 for r in responses if r['success']),
            'fallback_responses': sum(1 for r in responses if not r['success']),
            'success_rate': sum(1 for r in responses if r['success']) / len(responses)
        }
        
        return analysis, responses
    
    def generate_visualizations(self, test_queries: list, output_dir: str = 'outputs'):
        """Generate visualizations for chatbot performance."""
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Analyze queries
        analysis, responses = self.analyze_test_queries(test_queries)
        scores = analysis['scores']
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (14, 12)
        
        # Create figure with subplots
        fig = plt.figure(figsize=(16, 14))
        
        # 1. Histogram of similarity scores
        ax1 = plt.subplot(2, 3, 1)
        n, bins, patches = ax1.hist(scores, bins=15, color='steelblue', alpha=0.7, edgecolor='black')
        ax1.axvline(analysis['mean_confidence'], color='red', linestyle='--', linewidth=2, label=f"Mean: {analysis['mean_confidence']:.2%}")
        ax1.axvline(self.chatbot.confidence_threshold, color='orange', linestyle='--', linewidth=2, label=f"Threshold: {self.chatbot.confidence_threshold:.2%}")
        ax1.set_xlabel('Similarity Score', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax1.set_title('Distribution of Similarity Scores', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Color bars
        for i in range(len(patches)):
            if bins[i] >= self.chatbot.confidence_threshold:
                patches[i].set_facecolor('green')
                patches[i].set_alpha(0.6)
            else:
                patches[i].set_facecolor('red')
                patches[i].set_alpha(0.4)
        
        # 2. Box plot
        ax2 = plt.subplot(2, 3, 2)
        bp = ax2.boxplot(scores, vert=True, patch_artist=True, widths=0.5)
        bp['boxes'][0].set_facecolor('lightblue')
        ax2.set_ylabel('Similarity Score', fontsize=11, fontweight='bold')
        ax2.set_title('Similarity Score Distribution (Box Plot)', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.set_xticklabels(['Scores'])
        
        # 3. Success vs Fallback Pie Chart
        ax3 = plt.subplot(2, 3, 3)
        sizes = [analysis['successful_matches'], analysis['fallback_responses']]
        colors = ['#2ecc71', '#e74c3c']
        labels = [f"Successful\n({analysis['successful_matches']})", 
                 f"Fallback\n({analysis['fallback_responses']})"]
        wedges, texts, autotexts = ax3.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                            startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
        ax3.set_title('Match Success Rate', fontsize=12, fontweight='bold')
        
        # 4. Cumulative distribution
        ax4 = plt.subplot(2, 3, 4)
        sorted_scores = np.sort(scores)
        cumulative = np.arange(1, len(sorted_scores) + 1) / len(sorted_scores)
        ax4.plot(sorted_scores, cumulative, marker='o', linestyle='-', linewidth=2, markersize=6, color='darkblue')
        ax4.axvline(self.chatbot.confidence_threshold, color='orange', linestyle='--', linewidth=2)
        ax4.fill_between(sorted_scores, cumulative, alpha=0.3)
        ax4.set_xlabel('Similarity Score', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Cumulative Probability', fontsize=11, fontweight='bold')
        ax4.set_title('Cumulative Distribution of Scores', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        # 5. Statistics text
        ax5 = plt.subplot(2, 3, 5)
        ax5.axis('off')
        
        stats_text = f"""
        📊 SIMILARITY SCORE STATISTICS
        
        Total Queries: {analysis['num_queries']}
        
        Mean Confidence: {analysis['mean_confidence']:.2%}
        Median Confidence: {analysis['median_confidence']:.2%}
        Std Deviation: {analysis['std_confidence']:.2%}
        
        Range:
        • Min: {analysis['min_confidence']:.2%}
        • Max: {analysis['max_confidence']:.2%}
        
        Performance:
        • Successful Matches: {analysis['successful_matches']}
        • Fallback Responses: {analysis['fallback_responses']}
        • Success Rate: {analysis['success_rate']:.1%}
        
        Threshold: {self.chatbot.confidence_threshold:.2%}
        """
        
        ax5.text(0.1, 0.5, stats_text, fontsize=11, verticalalignment='center',
                fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # 6. Category distribution
        ax6 = plt.subplot(2, 3, 6)
        categories = [r['category'] for r in responses if r['success']]
        if categories:
            unique_cats, counts = np.unique(categories, return_counts=True)
            sorted_idx = np.argsort(counts)[::-1]
            ax6.barh(unique_cats[sorted_idx], counts[sorted_idx], color='teal', alpha=0.7, edgecolor='black')
            ax6.set_xlabel('Number of Matches', fontsize=11, fontweight='bold')
            ax6.set_title('Answer Category Distribution', fontsize=12, fontweight='bold')
            ax6.grid(True, alpha=0.3, axis='x')
        
        plt.suptitle('🏥 Health Chatbot Performance Analysis', fontsize=14, fontweight='bold', y=0.995)
        plt.tight_layout()
        
        # Save figure
        output_path = Path(output_dir) / 'similarity_scores_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Visualization saved to: {output_path}")
        
        plt.close()
        
        return analysis, responses
    
    def generate_query_response_analysis(self, test_queries: list, output_dir: str = 'outputs'):
        """Generate detailed analysis of queries and responses."""
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        analysis_data = {
            'metadata': {
                'total_queries': len(test_queries),
                'model': 'TF-IDF with Cosine Similarity',
                'confidence_threshold': self.chatbot.confidence_threshold
            },
            'query_analysis': []
        }
        
        print("\n📋 Generating detailed query analysis...")
        
        for i, query in enumerate(test_queries, 1):
            response = self.chatbot.answer_query(query)
            
            analysis_data['query_analysis'].append({
                'query_id': i,
                'query_text': query,
                'answer': response['answer'][:150] + '...' if len(response['answer']) > 150 else response['answer'],
                'confidence': response['confidence'],
                'confidence_percentage': f"{response['confidence']:.1%}",
                'category': response['category'],
                'is_successful': response['success'],
                'matched_question': response.get('matched_question', 'N/A')
            })
        
        # Save analysis
        output_path = Path(output_dir) / 'query_response_analysis.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Query analysis saved to: {output_path}")
        
        return analysis_data


def generate_comprehensive_analysis():
    """Generate comprehensive analysis with visualization."""
    
    # Initialize analyzer
    analyzer = ChatbotAnalyzer(dataset_path='data/health_qa_dataset.json')
    
    # Comprehensive test queries
    test_queries = [
        # Dengue related
        "What is dengue fever?",
        "How dengue spreads mosquitoes",
        "Dengue prevention tips",
        
        # Malaria related
        "Tell me about malaria symptoms",
        "Malaria treatment options",
        "How to prevent malaria",
        
        # COVID-19 related
        "What is COVID-19?",
        "COVID symptoms and prevention",
        "COVID-19 vaccine information",
        
        # Common cold
        "Cold prevention methods",
        "Common cold treatment",
        
        # Flu
        "Influenza symptoms",
        "Flu vaccine importance",
        
        # Diabetes
        "What causes diabetes?",
        "Diabetes management",
        "Diabetes prevention",
        
        # Heart health
        "Heart disease prevention",
        "High blood pressure management",
        
        # Mental health
        "How to manage anxiety",
        "Depression treatment options",
        
        # Other conditions
        "Asthma triggers and management",
        "Arthritis symptoms and treatment",
        "Weight management tips",
        
        # Low confidence test
        "xyz abc qwerty random nonsense",
        "12345 ajskdhak",
        
        # Ambiguous queries
        "I feel tired and weak",
        "I have fever and body aches",
        "Chest pain symptoms",
    ]
    
    # Generate visualizations
    print("\n" + "="*80)
    print("🏥 HEALTH CHATBOT - COMPREHENSIVE ANALYSIS")
    print("="*80)
    
    analysis, responses = analyzer.generate_visualizations(test_queries)
    
    # Generate query-response analysis
    qa_analysis = analyzer.generate_query_response_analysis(test_queries)
    
    # Print summary
    print("\n" + "="*80)
    print("📊 ANALYSIS SUMMARY")
    print("="*80)
    print(f"\nTotal Queries Analyzed: {analysis['num_queries']}")
    print(f"Successful Matches: {analysis['successful_matches']} ({analysis['success_rate']:.1%})")
    print(f"Fallback Responses: {analysis['fallback_responses']} ({1-analysis['success_rate']:.1%})")
    print(f"\nConfidence Scores:")
    print(f"  • Mean: {analysis['mean_confidence']:.2%}")
    print(f"  • Median: {analysis['median_confidence']:.2%}")
    print(f"  • Std Dev: {analysis['std_confidence']:.2%}")
    print(f"  • Min: {analysis['min_confidence']:.2%}")
    print(f"  • Max: {analysis['max_confidence']:.2%}")
    
    print("\n" + "="*80)
    print("✓ Analysis complete! Check outputs/ directory for visualizations.")
    print("="*80 + "\n")
    
    return analysis, responses, qa_analysis


if __name__ == "__main__":
    generate_comprehensive_analysis()
