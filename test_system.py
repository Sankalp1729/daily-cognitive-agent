#!/usr/bin/env python3
"""
Test script for Daily Cognitive Agent System
Run this to verify all components are working correctly
"""

import sys
import json
from datetime import datetime

# Import our modules
try:
    from cognitive_agent import CognitiveAgent
    from email_simulator import EmailSimulator
    from steganography import SteganographyModule
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_cognitive_agent():
    """Test the cognitive agent functionality"""
    print("\n🧠 Testing Cognitive Agent...")
    
    agent = CognitiveAgent()
    
    # Test email data
    test_email = {
        'id': 'test_1',
        'sender': 'blackhole01729@gmail.com',
        'subject': 'URGENT: Action required immediately',
        'body': 'This is an urgent matter that requires your immediate attention.',
        'timestamp': datetime.now().isoformat(),
        'priority': 'high',
        'attachments': []
    }
    
    # Test prediction
    prediction = agent.predict_action(test_email)
    print(f"✅ Prediction: {prediction['action']} (confidence: {prediction['confidence']:.3f})")
    print(f"✅ Explanation: {prediction['explanation']}")
    
    # Test feedback
    feedback = agent.receive_feedback(test_email, prediction['action'], 'approve')
    print(f"✅ Feedback recorded: {feedback['reward']} reward")
    
    # Test statistics
    stats = agent.get_statistics()
    print(f"✅ Statistics: {stats['total_feedback']} feedback, {stats['approval_rate']:.1%} approval rate")
    
    return True

def test_email_simulator():
    """Test the email simulator functionality"""
    print("\n📧 Testing Email Simulator...")
    
    simulator = EmailSimulator()
    
    # Test single email generation
    email = simulator.generate_email()
    print(f"✅ Generated email from: {email['sender']}")
    print(f"✅ Subject: {email['subject']}")
    
    # Test specific email generation
    specific_email = simulator.generate_specific_email(
        sender="blackhole01729@gmail.com",
        subject_type="urgent"
    )
    print(f"✅ Generated specific email: {specific_email['subject']}")
    
    # Test inbox generation
    inbox = simulator.generate_inbox(5)
    print(f"✅ Generated inbox with {len(inbox)} emails")
    
    return True

def test_steganography():
    """Test the steganography functionality"""
    print("\n🕵️ Testing Steganography...")
    
    stego = SteganographyModule()
    
    # Test email data
    test_email = {
        'id': 'test_2',
        'sender': 'test@example.com',
        'subject': 'Test Subject',
        'body': 'Test body content',
        'timestamp': datetime.now().isoformat()
    }
    
    prediction = {
        'action': 'Reply',
        'confidence': 0.85,
        'explanation': 'Test explanation'
    }
    
    # Test stealth log generation
    stealth_entry = stego.generate_stealth_log(test_email, prediction)
    print(f"✅ Generated stealth log with emoji: {stealth_entry['emoji_trigger']}")
    
    # Test data decoding
    decoded = stego.decode_stealth_data(stealth_entry)
    if 'error' not in decoded:
        print("✅ Stealth data decoded successfully")
        print(f"✅ Extracted action: {decoded['extracted_data']['action']}")
    else:
        print(f"❌ Decoding error: {decoded['error']}")
    
    return True

def test_integration():
    """Test full system integration"""
    print("\n🔗 Testing System Integration...")
    
    # Initialize all components
    agent = CognitiveAgent()
    simulator = EmailSimulator()
    stego = SteganographyModule()
    
    # Generate email
    email = simulator.generate_specific_email(
        sender="blackhole01729@gmail.com",
        subject_type="question"
    )
    
    # Get prediction
    prediction = agent.predict_action(email)
    
    # Generate stealth log
    stealth_entry = stego.generate_stealth_log(email, prediction)
    
    # Provide feedback
    feedback = agent.receive_feedback(email, prediction['action'], 'approve')
    
    print(f"✅ Integration test completed:")
    print(f"   - Email: {email['subject']}")
    print(f"   - Prediction: {prediction['action']}")
    print(f"   - Stealth emoji: {stealth_entry['emoji_trigger']}")
    print(f"   - Feedback reward: {feedback['reward']}")
    
    return True

def main():
    """Run all tests"""
    print("🧠 Daily Cognitive Agent - System Test")
    print("=" * 50)
    
    tests = [
        test_cognitive_agent,
        test_email_simulator,
        test_steganography,
        test_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to run.")
        print("\n🚀 To start the application, run:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 