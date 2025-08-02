#!/usr/bin/env python3
"""
Demo script for Daily Cognitive Agent System
This script demonstrates the key features of the system
"""

from cognitive_agent import CognitiveAgent
from email_simulator import EmailSimulator
from steganography import SteganographyModule
from datetime import datetime
import json

def demo_basic_functionality():
    """Demonstrate basic agent functionality"""
    print("🧠 Daily Cognitive Agent - Demo")
    print("=" * 50)
    
    # Initialize components
    agent = CognitiveAgent()
    simulator = EmailSimulator()
    stego = SteganographyModule()
    
    print("\n1. 📧 Generating test emails...")
    
    # Generate emails from the specified address
    emails = []
    for i in range(3):
        email = simulator.generate_specific_email(
            sender="blackhole01729@gmail.com",
            subject_type=["urgent", "question", "newsletter"][i]
        )
        emails.append(email)
        print(f"   - {email['subject']}")
    
    print("\n2. 🤖 Agent predictions and learning...")
    
    for i, email in enumerate(emails, 1):
        # Get prediction
        prediction = agent.predict_action(email)
        
        print(f"\n   Email {i}: {email['subject']}")
        print(f"   📧 From: {email['sender']}")
        print(f"   🎯 Predicted Action: {prediction['action']}")
        print(f"   📊 Confidence: {prediction['confidence']:.3f}")
        print(f"   💡 Explanation: {prediction['explanation']}")
        
        # Generate stealth log
        stealth_entry = stego.generate_stealth_log(email, prediction)
        print(f"   🕵️ Stealth Emoji: {stealth_entry['emoji_trigger']}")
        
        # Simulate user feedback (alternate approve/reject)
        feedback_type = 'approve' if i % 2 == 1 else 'reject'
        feedback = agent.receive_feedback(email, prediction['action'], feedback_type)
        
        print(f"   👍 User Feedback: {feedback_type.upper()}")
        print(f"   🎁 Reward: {feedback['reward']}")
    
    print("\n3. 📊 Learning progress...")
    
    stats = agent.get_statistics()
    print(f"   📈 Total Feedback: {stats['total_feedback']}")
    print(f"   ✅ Approval Rate: {stats['approval_rate']:.1%}")
    print(f"   🧠 Average Confidence: {stats['avg_confidence']:.3f}")
    
    if stats['top_actions']:
        print(f"   🏆 Top Action: {stats['top_actions'][0][0]} ({stats['top_actions'][0][1]} times)")
    
    if stats['top_senders']:
        print(f"   👤 Top Sender: {stats['top_senders'][0][0]} ({stats['top_senders'][0][1]} emails)")
    
    print("\n4. 🕵️ Stealth features demonstration...")
    
    # Show stealth data extraction
    test_email = emails[0]
    test_prediction = agent.predict_action(test_email)
    stealth_entry = stego.generate_stealth_log(test_email, test_prediction)
    
    print(f"   📧 Email: {test_email['subject']}")
    print(f"   🎯 Action: {test_prediction['action']}")
    print(f"   📊 Confidence: {test_prediction['confidence']:.3f}")
    print(f"   🕵️ Emoji Trigger: {stealth_entry['emoji_trigger']}")
    
    # Decode stealth data
    decoded = stego.decode_stealth_data(stealth_entry)
    if 'error' not in decoded:
        print(f"   ✅ Stealth data extracted successfully!")
        print(f"   🔍 Extracted action: {decoded['extracted_data']['action']}")
        print(f"   🔍 Data integrity: {'✅ Match' if decoded['data_match'] else '❌ Mismatch'}")
    else:
        print(f"   ❌ Stealth extraction error: {decoded['error']}")
    
    print("\n5. 🧠 Agent memory demonstration...")
    
    # Show sender memory
    sender = "blackhole01729@gmail.com"
    if sender in agent.sender_memory:
        sender_data = agent.sender_memory[sender]
        print(f"   📧 Sender: {sender}")
        print(f"   📊 Total emails: {sender_data['total_emails']}")
        print(f"   🎯 Action patterns: {dict(sender_data['action_counts'])}")
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed successfully!")
    print("\n🚀 To run the full interactive application:")
    print("   streamlit run app.py")
    print("\n📖 For more information, see README.md")

def demo_advanced_features():
    """Demonstrate advanced features"""
    print("\n🔬 Advanced Features Demo")
    print("=" * 30)
    
    agent = CognitiveAgent()
    simulator = EmailSimulator()
    
    # Test different email types
    email_types = ["urgent", "question", "newsletter"]
    
    for email_type in email_types:
        email = simulator.generate_specific_email(
            sender="blackhole01729@gmail.com",
            subject_type=email_type
        )
        
        prediction = agent.predict_action(email)
        
        print(f"\n📧 {email_type.upper()} Email:")
        print(f"   Subject: {email['subject']}")
        print(f"   Action: {prediction['action']}")
        print(f"   Confidence: {prediction['confidence']:.3f}")
        print(f"   Keywords: {prediction['keywords'][:5]}...")
    
    # Test learning progression
    print(f"\n📈 Learning Progression Test:")
    
    # Send multiple similar emails to see learning
    for i in range(5):
        email = simulator.generate_specific_email(
            sender="blackhole01729@gmail.com",
            subject_type="urgent"
        )
        
        prediction = agent.predict_action(email)
        feedback = agent.receive_feedback(email, prediction['action'], 'approve')
        
        print(f"   Email {i+1}: {prediction['action']} (conf: {prediction['confidence']:.3f})")
    
    stats = agent.get_statistics()
    print(f"\n   Final stats: {stats['total_feedback']} feedback, {stats['approval_rate']:.1%} approval rate")

if __name__ == "__main__":
    demo_basic_functionality()
    demo_advanced_features() 