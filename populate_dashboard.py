#!/usr/bin/env python3
"""
Script to populate the dashboard with sample data
Run this to generate emails and feedback for the dashboard
"""

from cognitive_agent import CognitiveAgent
from email_simulator import EmailSimulator
from steganography import SteganographyModule
import json

def populate_dashboard():
    """Generate sample data for the dashboard"""
    print("📊 Populating Dashboard with Sample Data...")
    
    # Initialize components
    agent = CognitiveAgent()
    simulator = EmailSimulator()
    stego = SteganographyModule()
    
    # Generate emails from blackhole01729@gmail.com
    print("📧 Generating emails from blackhole01729@gmail.com...")
    
    email_types = ["urgent", "question", "newsletter"]
    feedback_types = ["approve", "reject", "approve", "reject", "approve"]
    
    for i in range(5):
        # Generate email
        email = simulator.generate_specific_email(
            sender="blackhole01729@gmail.com",
            subject_type=email_types[i % 3]
        )
        
        # Get prediction
        prediction = agent.predict_action(email)
        
        # Generate stealth log
        stealth_entry = stego.generate_stealth_log(email, prediction)
        
        # Provide feedback
        feedback = agent.receive_feedback(
            email, 
            prediction['action'], 
            feedback_types[i]
        )
        
        print(f"   Email {i+1}: {email['subject']}")
        print(f"   Action: {prediction['action']} (Confidence: {prediction['confidence']:.3f})")
        print(f"   Feedback: {feedback_types[i].upper()}")
        print(f"   Stealth: {stealth_entry['emoji_trigger']}")
        print()
    
    # Generate some emails from other senders
    print("📧 Generating emails from other senders...")
    
    other_senders = [
        "john.doe@company.com",
        "sarah.smith@business.org", 
        "mike.wilson@startup.io",
        "lisa.chen@techcorp.com"
    ]
    
    for i, sender in enumerate(other_senders):
        email = simulator.generate_email(sender=sender)
        prediction = agent.predict_action(email)
        stealth_entry = stego.generate_stealth_log(email, prediction)
        
        # Provide feedback (alternate approve/reject)
        feedback_type = "approve" if i % 2 == 0 else "reject"
        feedback = agent.receive_feedback(email, prediction['action'], feedback_type)
        
        print(f"   Email {i+6}: {email['subject']} (from {sender})")
        print(f"   Action: {prediction['action']} (Confidence: {prediction['confidence']:.3f})")
        print(f"   Feedback: {feedback_type.upper()}")
        print(f"   Stealth: {stealth_entry['emoji_trigger']}")
        print()
    
    # Save the data
    agent.save_memory()
    simulator.save_inbox()
    
    # Show final statistics
    stats = agent.get_statistics()
    print("📊 Final Dashboard Statistics:")
    print(f"   📈 Total Feedback: {stats['total_feedback']}")
    print(f"   ✅ Approval Rate: {stats['approval_rate']:.1%}")
    print(f"   🧠 Average Confidence: {stats['avg_confidence']:.3f}")
    
    if stats['top_actions']:
        print(f"   🏆 Top Action: {stats['top_actions'][0][0]} ({stats['top_actions'][0][1]} times)")
    
    if stats['top_senders']:
        print(f"   👤 Top Sender: {stats['top_senders'][0][0]} ({stats['top_senders'][0][1]} emails)")
    
    print("\n🎉 Dashboard populated successfully!")
    print("🔄 Refresh your Streamlit app to see the new data.")
    print("📊 Navigate to the Dashboard page to see analytics.")

if __name__ == "__main__":
    populate_dashboard() 

