# 🧠 Daily Cognitive Agent

A sophisticated email inbox assistant that learns from user feedback using reinforcement learning. The agent predicts actions for incoming emails and continuously improves its decision-making through user interactions.

## 🌟 Features

### 📧 Inbox Simulator
- **Real-time email generation** with realistic content
- **Multiple sender profiles** including the specified `blackhole01729@gmail.com`
- **Priority levels** and attachment simulation
- **Time-based email distribution**

### 🤖 Cognitive Agent
- **Reinforcement Learning** with Q-learning algorithm
- **Epsilon-greedy exploration** for balanced learning
- **Sender pattern recognition** and memory
- **Keyword-based learning** from email content
- **Confidence scoring** with explanations

### 📊 Live Reinforcement Learning
- **Real-time Q-table updates** based on user feedback
- **Reward system** (+2 for approval, -2 for rejection)
- **Memory persistence** across sessions
- **Adaptive learning rates** and exploration parameters

### 🧠 Agent Memory
- **Sender relationship tracking** with action history
- **Keyword association learning** for better predictions
- **Topic-based pattern recognition**
- **Long-term memory storage** in JSON format

### 📈 Feedback Dashboard
- **Action distribution** visualizations
- **Confidence trend analysis**
- **Top sender/action statistics**
- **Performance metrics** and learning progress
- **Real-time reward tracking**

### 🕵️ Creative Stealth Add-on
- **Steganography**: Embed agent confidence data in transparent PNG images
- **Emoji-based triggers**: Visual indicators for agent behavior
- **Hidden data extraction** from image metadata
- **Stealth logging** with embedded information

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone or download** the project files to your local machine

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
streamlit run app.py
```

4. **Open your browser** and navigate to `http://localhost:8501`

## 🎯 How to Use

### 1. Generate Emails
- Click **"📧 Generate New Email"** to create a single email
- Click **"📬 Generate Inbox (10 emails)"** to create multiple emails
- The system has a 30% chance to generate emails from `blackhole01729@gmail.com`

### 2. Review Agent Predictions
- The agent will analyze each email and predict an action
- View the **confidence score** and **explanation**
- See the **emoji trigger** for quick visual feedback

### 3. Provide Feedback
- **👍 Approve**: If the agent's prediction is correct
- **👎 Reject**: If the prediction is wrong
- **Select correct action** from dropdown and submit correction

### 4. Monitor Learning
- Navigate to **"📊 Dashboard"** to see learning progress
- Check **"🕵️ Stealth Logs"** to view embedded data
- Review **"📝 Feedback History"** for detailed logs

## 🔧 Configuration

### Agent Settings
- **Learning Rate**: Controls how quickly the agent learns (0.01-0.5)
- **Exploration Rate (Epsilon)**: Controls exploration vs exploitation (0.0-1.0)

### Available Actions
- **Reply**: Respond to the email
- **Archive**: Move to archive
- **Forward**: Forward to another recipient
- **Mark Important**: Flag as important
- **Delete**: Delete the email
- **Spam**: Mark as spam

## 🕵️ Stealth Features

### Steganography
The system embeds agent confidence data in transparent PNG images:
- **Confidence scores** hidden in pixel values
- **Action predictions** stored in image metadata
- **Email information** encoded in binary format
- **Data extraction** and verification capabilities

### Emoji Triggers
Visual indicators for agent behavior:
- 💬 Reply
- 📁 Archive  
- 📤 Forward
- 📌 Mark Important
- 🗑️ Delete
- 🚫 Spam

Confidence levels:
- 🔥 High confidence (>0.8)
- ✅ Medium confidence (0.6-0.8)
- 🤔 Low confidence (0.4-0.6)
- ❓ Very low confidence (<0.4)

## 📁 File Structure

```
daily-cognitive-agent/
├── app.py                 # Main Streamlit application
├── cognitive_agent.py     # Reinforcement learning agent
├── email_simulator.py     # Email generation system
├── steganography.py       # Stealth data embedding
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── agent_memory.json     # Persistent agent memory (auto-generated)
└── inbox_data.json       # Email history (auto-generated)
```

## 🧠 Technical Details

### Reinforcement Learning
- **Q-Learning Algorithm** with state-action value updates
- **State Representation**: sender + urgency + question + time
- **Reward Function**: +2 for approval, -2 for rejection
- **Exploration Strategy**: Epsilon-greedy with configurable parameters

### Memory System
- **Sender Memory**: Tracks action patterns per sender
- **Keyword Memory**: Learns from email content keywords
- **Topic Memory**: Recognizes subject-topic relationships
- **Feedback History**: Complete interaction logs

### Data Persistence
- **JSON-based storage** for agent memory
- **Session state management** for real-time updates
- **Automatic saving** after each feedback interaction

## 🎨 UI Features

### Modern Interface
- **Responsive design** with sidebar navigation
- **Real-time updates** without page refresh
- **Interactive charts** with Plotly
- **Color-coded confidence** indicators
- **Expandable email details**

### Dashboard Visualizations
- **Bar charts** for action distribution
- **Pie charts** for sender analysis
- **Line charts** for performance trends
- **Metrics cards** for key statistics

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Font Issues**: The system will fallback to default fonts if Arial is not available

3. **Memory Issues**: Large datasets may require more RAM, consider clearing old data

4. **Performance**: For large feedback histories, consider archiving old data

### Data Management
- **Clear Memory**: Delete `agent_memory.json` to reset agent learning
- **Export Data**: Copy JSON files for backup or analysis
- **Import Data**: Replace JSON files to restore previous state

## 🚀 Future Enhancements

- **Email API Integration** for real email processing
- **Advanced NLP** for better content understanding
- **Multi-language Support** for international emails
- **Team Collaboration** features
- **Advanced Analytics** and reporting
- **Mobile App** version

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

**🧠 Daily Cognitive Agent** - Powered by Reinforcement Learning 