import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from collections import defaultdict, Counter
import pickle
import os

class CognitiveAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        
        # Q-table for reinforcement learning
        self.q_table = defaultdict(lambda: defaultdict(float))
        
        # Memory for sender patterns and keywords
        self.sender_memory = defaultdict(lambda: {
            'action_counts': Counter(),
            'total_emails': 0,
            'avg_confidence': 0.0,
            'last_interaction': None
        })
        
        # Keyword memory
        self.keyword_memory = defaultdict(lambda: {
            'action_counts': Counter(),
            'confidence_scores': []
        })
        
        # Subject-topic relationships
        self.topic_memory = defaultdict(lambda: {
            'action_counts': Counter(),
            'keywords': set(),
            'confidence_scores': []
        })
        
        # Available actions
        self.actions = ['Reply', 'Archive', 'Forward', 'Mark Important', 'Delete', 'Spam']
        
        # Feedback history
        self.feedback_history = []
        
        # Load existing data if available
        self.load_memory()
    
    def extract_features(self, email_data):
        """Extract features from email for state representation"""
        sender = email_data.get('sender', '').lower()
        subject = email_data.get('subject', '').lower()
        body = email_data.get('body', '').lower()
        
        # Extract keywords from subject and body
        keywords = set()
        for word in subject.split() + body.split():
            if len(word) > 3 and word.isalpha():
                keywords.add(word)
        
        # Create state representation
        state = {
            'sender': sender,
            'subject_length': len(subject),
            'body_length': len(body),
            'has_urgent_words': any(word in subject + body for word in ['urgent', 'asap', 'important', 'deadline']),
            'has_question': '?' in subject or '?' in body,
            'sender_frequency': self.sender_memory[sender]['total_emails'],
            'time_of_day': datetime.now().hour
        }
        
        return state, keywords
    
    def get_state_key(self, state):
        """Convert state to string key for Q-table"""
        return f"{state['sender']}_{state['has_urgent_words']}_{state['has_question']}_{state['time_of_day']}"
    
    def predict_action(self, email_data):
        """Predict action using epsilon-greedy policy"""
        state, keywords = self.extract_features(email_data)
        state_key = self.get_state_key(state)
        
        # Check sender memory for patterns
        sender = email_data.get('sender', '').lower()
        if sender in self.sender_memory and self.sender_memory[sender]['total_emails'] > 5:
            most_common_action = self.sender_memory[sender]['action_counts'].most_common(1)
            if most_common_action:
                sender_bias = most_common_action[0][0]
                confidence_bonus = 0.3
            else:
                sender_bias = None
                confidence_bonus = 0.0
        else:
            sender_bias = None
            confidence_bonus = 0.0
        
        # Epsilon-greedy action selection
        if random.random() < self.epsilon:
            action = random.choice(self.actions)
        else:
            # Get Q-values for current state
            q_values = {action: self.q_table[state_key][action] for action in self.actions}
            
            # Apply sender bias if available
            if sender_bias:
                q_values[sender_bias] += 0.5
            
            action = max(q_values, key=q_values.get)
        
        # Calculate confidence score
        confidence = self.calculate_confidence(state, action, keywords, confidence_bonus)
        
        # Generate explanation
        explanation = self.generate_explanation(state, action, keywords, sender)
        
        return {
            'action': action,
            'confidence': confidence,
            'explanation': explanation,
            'state': state,
            'keywords': list(keywords)
        }
    
    def calculate_confidence(self, state, action, keywords, confidence_bonus):
        """Calculate confidence score for the predicted action"""
        base_confidence = 0.5
        
        # Sender-based confidence
        sender = state['sender']
        if sender in self.sender_memory:
            sender_data = self.sender_memory[sender]
            if sender_data['total_emails'] > 0:
                action_frequency = sender_data['action_counts'][action] / sender_data['total_emails']
                base_confidence += action_frequency * 0.3
        
        # Keyword-based confidence
        keyword_confidence = 0.0
        for keyword in keywords:
            if keyword in self.keyword_memory:
                keyword_data = self.keyword_memory[keyword]
                if keyword_data['action_counts'][action] > 0:
                    keyword_confidence += 0.1
        
        # State-based confidence
        if state['has_urgent_words'] and action in ['Reply', 'Mark Important']:
            base_confidence += 0.2
        if state['has_question'] and action == 'Reply':
            base_confidence += 0.2
        
        final_confidence = min(0.95, base_confidence + keyword_confidence + confidence_bonus)
        return round(final_confidence, 3)
    
    def generate_explanation(self, state, action, keywords, sender):
        """Generate human-readable explanation for the action"""
        explanations = []
        
        # Sender-based explanation
        if sender in self.sender_memory and self.sender_memory[sender]['total_emails'] > 3:
            most_common = self.sender_memory[sender]['action_counts'].most_common(1)[0]
            if most_common[0] == action:
                explanations.append(f"Based on {most_common[1]} previous interactions with this sender")
        
        # State-based explanations
        if state['has_urgent_words']:
            explanations.append("Contains urgent keywords")
        if state['has_question']:
            explanations.append("Contains a question")
        if state['subject_length'] > 50:
            explanations.append("Long subject suggests detailed content")
        
        # Keyword-based explanations
        if keywords:
            relevant_keywords = [k for k in keywords if k in self.keyword_memory]
            if relevant_keywords:
                explanations.append(f"Keywords: {', '.join(relevant_keywords[:3])}")
        
        if not explanations:
            explanations.append("Based on general email patterns")
        
        return "; ".join(explanations)
    
    def receive_feedback(self, email_data, predicted_action, user_feedback, correct_action=None):
        """Receive feedback and update Q-table and memory"""
        state, keywords = self.extract_features(email_data)
        state_key = self.get_state_key(state)
        sender = email_data.get('sender', '').lower()
        
        # Determine reward
        if user_feedback == 'approve':
            reward = 2.0
            final_action = predicted_action
        elif user_feedback == 'reject':
            reward = -2.0
            final_action = correct_action if correct_action else predicted_action
        else:
            reward = 0.0
            final_action = predicted_action
        
        # Update Q-table
        current_q = self.q_table[state_key][predicted_action]
        max_future_q = max([self.q_table[state_key][action] for action in self.actions])
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_future_q - current_q)
        self.q_table[state_key][predicted_action] = new_q
        
        # Update sender memory
        self.sender_memory[sender]['action_counts'][final_action] += 1
        self.sender_memory[sender]['total_emails'] += 1
        self.sender_memory[sender]['last_interaction'] = datetime.now().isoformat()
        
        # Update keyword memory
        for keyword in keywords:
            self.keyword_memory[keyword]['action_counts'][final_action] += 1
            self.keyword_memory[keyword]['confidence_scores'].append(reward)
        
        # Log feedback
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'sender': sender,
            'subject': email_data.get('subject', ''),
            'predicted_action': predicted_action,
            'user_feedback': user_feedback,
            'correct_action': final_action,
            'reward': reward,
            'confidence': self.calculate_confidence(state, predicted_action, keywords, 0.0)
        }
        self.feedback_history.append(feedback_entry)
        
        # Save memory
        self.save_memory()
        
        return feedback_entry
    
    def get_statistics(self):
        """Get agent statistics for dashboard"""
        total_feedback = len(self.feedback_history)
        if total_feedback == 0:
            return {
                'total_feedback': 0,
                'approval_rate': 0,
                'avg_confidence': 0,
                'top_actions': [],
                'top_senders': [],
                'recent_performance': []
            }
        
        # Calculate approval rate
        approvals = sum(1 for f in self.feedback_history if f['user_feedback'] == 'approve')
        approval_rate = approvals / total_feedback
        
        # Average confidence
        avg_confidence = np.mean([f['confidence'] for f in self.feedback_history])
        
        # Top actions
        action_counts = Counter([f['correct_action'] for f in self.feedback_history])
        top_actions = action_counts.most_common(5)
        
        # Top senders
        sender_counts = Counter([f['sender'] for f in self.feedback_history])
        top_senders = sender_counts.most_common(5)
        
        # Recent performance (last 10 feedbacks)
        recent_feedback = self.feedback_history[-10:]
        recent_performance = []
        for f in recent_feedback:
            recent_performance.append({
                'timestamp': f['timestamp'],
                'reward': f['reward'],
                'confidence': f['confidence']
            })
        
        return {
            'total_feedback': total_feedback,
            'approval_rate': round(approval_rate, 3),
            'avg_confidence': round(avg_confidence, 3),
            'top_actions': top_actions,
            'top_senders': top_senders,
            'recent_performance': recent_performance
        }
    
    def save_memory(self):
        """Save agent memory to files"""
        memory_data = {
            'q_table': dict(self.q_table),
            'sender_memory': dict(self.sender_memory),
            'keyword_memory': dict(self.keyword_memory),
            'topic_memory': dict(self.topic_memory),
            'feedback_history': self.feedback_history
        }
        
        with open('agent_memory.json', 'w') as f:
            json.dump(memory_data, f, indent=2, default=str)
    
    def load_memory(self):
        """Load agent memory from files"""
        try:
            with open('agent_memory.json', 'r') as f:
                memory_data = json.load(f)
                
            self.q_table = defaultdict(lambda: defaultdict(float))
            for state, actions in memory_data.get('q_table', {}).items():
                for action, value in actions.items():
                    self.q_table[state][action] = value
            
            self.sender_memory = defaultdict(lambda: {
                'action_counts': Counter(),
                'total_emails': 0,
                'avg_confidence': 0.0,
                'last_interaction': None
            })
            for sender, data in memory_data.get('sender_memory', {}).items():
                self.sender_memory[sender] = data
                self.sender_memory[sender]['action_counts'] = Counter(data.get('action_counts', {}))
            
            self.keyword_memory = defaultdict(lambda: {
                'action_counts': Counter(),
                'confidence_scores': []
            })
            for keyword, data in memory_data.get('keyword_memory', {}).items():
                self.keyword_memory[keyword] = data
                self.keyword_memory[keyword]['action_counts'] = Counter(data.get('action_counts', {}))
            
            self.feedback_history = memory_data.get('feedback_history', [])
            
        except FileNotFoundError:
            # Initialize with empty memory
            pass 