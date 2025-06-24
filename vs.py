from flask import Flask, render_template_string, request, jsonify, session
import re
import json
from datetime import datetime
import random
import secrets
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(16))

KNOWLEDGE_BASE = {
    "company_info": {
        "name": "ECO Matrix",
        "location": "Winnipeg, Canada",
        "industry": "Energy Modeling Consultancy",
        "specialization": "Architectural, Engineering, and Construction (AEC) industry",
        "mission": "Optimizing building decision metrics and KPIs through advanced parametric modeling",
        "founded": "Established energy modeling consultancy",
        "team": "Expert energy modeling professionals and engineers"
    },
    "services": {
        "primary": "SaaS application for building design optimization",
        "energy_modeling": "Advanced parametric energy modeling protocols",
        "cost_analysis": "Capital and operational cost minimization",
        "compliance": "Building code compliance verification",
        "benchmarking": "Energy performance benchmarking",
        "consulting": "Expert energy modeling consultation",
        "design_optimization": "Building design solution identification",
        "load_analysis": "Detailed building load analysis"
    },
    "platform_features": {
        "3d_modeling": "Generate 3D, project-specific building models",
        "energy_simulation": "Perform energy simulations for various design combinations",
        "comparison_engine": "Compare thousands of design options",
        "cost_optimization": "Identify cost-effective solutions",
        "efficiency_analysis": "Maximize energy efficiency analysis",
        "reporting": "Detailed performance reports and analytics",
        "integration": "Integration with existing AEC workflows"
    },
    "contact": {
        "email": "anup@ecomatrix.io",
        "phone": "+1 (204) 894 0387",
        "website": "https://ecomatrix.io"
    },
    "technical_specs": {
        "technology": "Proprietary SaaS application",
        "modeling_type": "Parametric energy modeling",
        "output_formats": "3D models, energy reports, cost analysis",
        "industries_served": "Architecture, Engineering, Construction",
        "compliance_standards": "Building energy codes and standards"
    }
}

class AdvancedChatbot:
    def preprocess_query(self, query):
        query = query.lower().strip()
        query = re.sub(r'[^\w\s]', ' ', query)
        query = re.sub(r'\s+', ' ', query)
        return query

    def extract_intent(self, query):
        intents = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'services': ['service', 'offering', 'what do you do', 'capabilities', 'help with'],
            'product': ['product', 'platform', 'software', 'application', 'tool', 'saas'],
            'company': ['company', 'about', 'who are you', 'business', 'organization'],
            'contact': ['contact', 'reach', 'phone', 'email', 'address', 'location'],
            'technical': ['how does it work', 'technical', 'specification', 'technology'],
            'pricing': ['price', 'cost', 'pricing', 'fee', 'subscription', 'payment'],
            'comparison': ['vs', 'versus', 'compare', 'difference', 'better than'],
            'benefits': ['benefit', 'advantage', 'why choose', 'value proposition'],
            'industry': ['construction', 'architecture', 'engineering', 'aec', 'building'],
            'energy': ['energy', 'efficiency', 'modeling', 'simulation', 'optimization'],
            'farewell': ['bye', 'goodbye', 'thank you', 'thanks', 'see you']
        }
        detected_intents = []
        for intent, keywords in intents.items():
            if any(keyword in query for keyword in keywords):
                detected_intents.append(intent)
        return detected_intents if detected_intents else ['general']

    def get_contextual_response(self, query, intents):
        responses = []
        if 'greeting' in intents:
            greetings = [
                "Hello! I'm your ECO Matrix AI Assistant. How can I help you today?",
                "Hi there! Welcome to ECO Matrix. What would you like to know?",
                "Greetings! I'm here to help you with all your energy modeling questions."
            ]
            responses.append(random.choice(greetings))
        if 'services' in intents:
            responses.append(f"""
**ECO Matrix Services:**

🏢 **Core Offering**: Our innovative SaaS application helps Architectural, Engineering, and Construction firms identify building design solutions that maximize energy efficiency while minimizing costs.

🔧 **Key Services**:
- Advanced parametric energy modeling protocols
- Building design optimization and analysis
- Capital and operational cost minimization strategies
- Energy performance benchmarking
- Building code compliance verification
- Detailed building load analysis
- Expert energy modeling consultation

💡 **Value Proposition**: We enable you to compare thousands of design options with detailed analysis, ensuring you get the most cost-effective and energy-efficient solutions for your projects.
            """)
        if 'product' in intents or 'technical' in intents:
            responses.append(f"""
**ECO Matrix Platform Features:**

🎯 **3D Modeling**: Generate project-specific 3D building models tailored to your requirements

⚡ **Energy Simulation**: Perform comprehensive energy simulations for various design combinations

📊 **Comparison Engine**: Compare thousands of design options simultaneously

💰 **Cost Optimization**: Identify solutions that outperform benchmarks in cost-effectiveness

📈 **Performance Analytics**: Detailed reporting and energy benchmarking capabilities

🔗 **Integration**: Seamlessly integrates with existing AEC industry workflows

The platform uses proprietary algorithms to help you make data-driven decisions for optimal building performance.
            """)
        if 'company' in intents:
            responses.append(f"""
**About ECO Matrix:**

🏢 **Company**: ECO Matrix is a specialized energy modeling consultancy based in Winnipeg, Canada

🎯 **Mission**: We focus on optimizing building decision metrics and KPIs for the AEC industry through advanced parametric modeling protocols

👥 **Expertise**: Our team consists of expert energy modeling professionals and engineers

🌍 **Industry Focus**: We serve the Architectural, Engineering, and Construction industries

🚀 **Innovation**: We're committed to providing cutting-edge solutions that drive energy efficiency and cost optimization in building design
            """)
        if 'contact' in intents:
            responses.append(f"""
**Contact ECO Matrix:**

📧 **Email**: anup@ecomatrix.io
📞 **Phone**: +1 (204) 894 0387
🌐 **Website**: https://ecomatrix.io
📍 **Location**: Winnipeg, Canada

Feel free to reach out for consultations, demos, or any questions about our energy modeling services!
            """)
        if 'energy' in intents:
            responses.append(f"""
**Energy Modeling & Optimization:**

🔋 **Energy Efficiency**: Our platform maximizes building energy efficiency through advanced modeling techniques

📐 **Parametric Modeling**: We use sophisticated parametric protocols to analyze multiple design scenarios

⚖️ **Performance Benchmarking**: Compare your building's performance against industry standards and codes

🎛️ **Load Analysis**: Detailed analysis of building energy loads and consumption patterns

📊 **Optimization Reports**: Comprehensive reports showing energy savings potential and cost implications

Our energy modeling approach ensures your buildings meet or exceed efficiency standards while staying within budget.
            """)
        if 'benefits' in intents:
            responses.append(f"""
**Why Choose ECO Matrix:**

✅ **Cost Savings**: Minimize both capital and operational costs through optimized design

⚡ **Energy Efficiency**: Maximize building performance and energy savings

🎯 **Data-Driven Decisions**: Make informed choices based on comprehensive analysis

⏱️ **Time Efficiency**: Quickly compare thousands of design options

📋 **Compliance Assurance**: Ensure building code compliance from the design phase

🏆 **Competitive Advantage**: Stay ahead with cutting-edge energy modeling technology

💼 **Expert Support**: Access to experienced energy modeling professionals
            """)
        if 'pricing' in intents:
            responses.append(f"""
**Pricing Information:**

For detailed pricing information and subscription options, please contact us directly:

📧 Email: anup@ecomatrix.io
📞 Phone: +1 (204) 894 0387

We offer flexible pricing models tailored to your project needs and company size. Our team will be happy to discuss options that work best for your specific requirements.
            """)
        if 'farewell' in intents:
            farewells = [
                "Thank you for your interest in ECO Matrix! Feel free to reach out anytime.",
                "Goodbye! Don't hesitate to contact us for your energy modeling needs.",
                "Thanks for chatting! We're here whenever you need energy modeling expertise."
            ]
            responses.append(random.choice(farewells))
        if not responses or 'general' in intents:
            keywords = query.split()
            relevant_info = []
            for keyword in keywords:
                for category, data in KNOWLEDGE_BASE.items():
                    if isinstance(data, dict):
                        for key, value in data.items():
                            if keyword in key.lower() or keyword in str(value).lower():
                                relevant_info.append(f"**{key.replace('_', ' ').title()}**: {value}")
            if relevant_info:
                responses.append("Here's what I found relevant to your query:\n\n" + "\n".join(relevant_info[:3]))
            else:
                responses.append(f"""
I'd be happy to help you with information about ECO Matrix! Here are some topics I can assist with:

🏢 **Company Information** - Learn about ECO Matrix and our mission
🔧 **Services** - Discover our energy modeling and optimization services
💻 **Platform Features** - Explore our SaaS application capabilities
📞 **Contact Details** - Get in touch with our team
⚡ **Energy Modeling** - Understand our technical approach
💰 **Benefits** - See why ECO Matrix is the right choice

Please feel free to ask about any of these topics or anything specific about energy modeling and building optimization!
                """)
        return "\n\n".join(responses)

    def generate_response(self, query):
        processed_query = self.preprocess_query(query)
        intents = self.extract_intent(processed_query)
        response = self.get_contextual_response(processed_query, intents)
        return response

chatbot = AdvancedChatbot()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ECO Matrix AI Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .main-header {
            background: linear-gradient(90deg, #2E8B57, #4682B4);
            color: white;
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .main-header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .main-header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            flex: 1;
            display: flex;
            gap: 2rem;
        }
        
        .chat-section {
            flex: 3;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 600px;
        }
        
        .chat-header {
            background: #f8f9fa;
            padding: 1rem;
            border-bottom: 1px solid #e9ecef;
            font-weight: bold;
            font-size: 1.1rem;
            color: #2E8B57;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .message {
            padding: 1rem;
            border-radius: 10px;
            max-width: 80%;
            word-wrap: break-word;
        }
        
        .user-message {
            background-color: #e3f2fd;
            border-left: 4px solid #4682B4;
            align-self: flex-end;
            margin-left: auto;
        }
        
        .bot-message {
            background-color: #f1f8e9;
            border-left: 4px solid #2E8B57;
            align-self: flex-start;
        }
        
        .message-content {
            white-space: pre-wrap;
            line-height: 1.5;
        }
        
        .message-header {
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: #333;
        }
        
        .input-section {
            border-top: 1px solid #e9ecef;
            padding: 1rem;
            background: #f8f9fa;
        }
        
        .input-form {
            display: flex;
            gap: 0.5rem;
        }
        
        .message-input {
            flex: 1;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 25px;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s;
        }
        
        .message-input:focus {
            border-color: #2E8B57;
        }
        
        .send-button {
            background: linear-gradient(90deg, #2E8B57, #4682B4);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1rem;
            transition: transform 0.2s;
        }
        
        .send-button:hover {
            transform: translateY(-1px);
        }
        
        .sidebar {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .quick-actions, .contact-info {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .section-title {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #2E8B57;
        }
        
        .quick-button {
            width: 100%;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            text-align: left;
            transition: all 0.3s;
        }
        
        .quick-button:hover {
            background: #e9ecef;
            border-color: #2E8B57;
        }
        
        .clear-button {
            background: #dc3545;
            color: white;
            border: none;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            width: 100%;
            margin-top: 1rem;
            transition: background-color 0.3s;
        }
        
        .clear-button:hover {
            background: #c82333;
        }
        
        .contact-details {
            line-height: 1.8;
            color: #555;
        }
        
        .contact-details strong {
            color: #2E8B57;
        }
        
        .footer {
            text-align: center;
            color: #666;
            padding: 2rem;
            margin-top: 2rem;
            border-top: 1px solid #e9ecef;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 1rem;
            color: #666;
        }
        
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #2E8B57;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .container {
                flex-direction: column;
                padding: 0 1rem;
            }
            
            .main-header h1 {
                font-size: 2rem;
            }
            
            .main-header p {
                font-size: 1rem;
            }
            
            .chat-section {
                height: 500px;
            }
        }
    </style>
</head>
<body>
    <div class="main-header">
        <h1>🤖 ECO Matrix AI Assistant</h1>
        <p>Your intelligent companion for energy modeling and building optimization</p>
    </div>
    
    <div class="container">
        <div class="chat-section">
            <div class="chat-header">
                💬 Chat with ECO Matrix AI
            </div>
            
            <div class="chat-messages" id="chatMessages">
                </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <span>ECO Matrix AI is thinking...</span>
            </div>
            
            <div class="input-section">
                <form class="input-form" id="messageForm">
                    <input type="text" class="message-input" id="messageInput" 
                           placeholder="Ask me anything about ECO Matrix..." required>
                    <button type="submit" class="send-button">Send 📤</button>
                </form>
            </div>
        </div>
        
        <div class="sidebar">
            <div class="quick-actions">
                <div class="section-title">🚀 Quick Actions</div>
                <button class="quick-button" onclick="sendQuickMessage('What services does ECO Matrix offer?')">
                    What services does ECO Matrix offer?
                </button>
                <button class="quick-button" onclick="sendQuickMessage('How does the platform work?')">
                    How does the platform work?
                </button>
                <button class="quick-button" onclick="sendQuickMessage('Tell me about the company')">
                    Tell me about the company
                </button>
                <button class="quick-button" onclick="sendQuickMessage('How can I contact ECO Matrix?')">
                    How can I contact ECO Matrix?
                </button>
                <button class="quick-button" onclick="sendQuickMessage('What are the benefits of using ECO Matrix?')">
                    What are the benefits of using ECO Matrix?
                </button>
                <button class="quick-button" onclick="sendQuickMessage('What is energy modeling?')">
                    What is energy modeling?
                </button>
                <button class="clear-button" onclick="clearConversation()">
                    🗑️ Clear Conversation
                </button>
            </div>
            
            <div class="contact-info">
                <div class="section-title">📞 Contact Info</div>
                <div class="contact-details">
                    <strong>Email:</strong> anup@ecomatrix.io<br>
                    <strong>Phone:</strong> +1 (204) 894 0387<br>
                    <strong>Website:</strong> <a href="https://ecomatrix.io" target="_blank">https://ecomatrix.io</a>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        Powered by ECO Matrix AI Assistant | Advanced Energy Modeling Solutions | © 2025 All Rights Reserved.
    </div>
    <script>
        let isLoading = false;
        const messageForm = document.getElementById('messageForm');
        const messageInput = document.getElementById('messageInput');
        const chatMessages = document.getElementById('chatMessages');
        const loading = document.getElementById('loading');
        function formatMessage(content) {
            return content
                .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
                .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
                .replace(/\\n/g, '<br>');
        }
        function addMessage(role, content) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}-message`;
            const messageHeader = document.createElement('div');
            messageHeader.className = 'message-header';
            messageHeader.textContent = role === 'user' ? 'You:' : 'ECO Matrix AI:';
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.innerHTML = formatMessage(content);
            messageDiv.appendChild(messageHeader);
            messageDiv.appendChild(messageContent);
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        async function sendMessage(message) {
            if (isLoading) return;
            isLoading = true;
            loading.style.display = 'block';
            addMessage('user', message);
            messageInput.value = '';
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });
                if (!response.ok) {
                    const errorText = await response.text();
                    console.error(`HTTP error! status: ${response.status}, response: ${errorText}`);
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                if (data.success) {
                    addMessage('bot', data.response);
                } else {
                    addMessage('bot', data.error || 'Sorry, I encountered an unknown error. Please try again.');
                }
            } catch (error) {
                console.error('Fetch Error:', error);
                addMessage('bot', 'Sorry, I encountered an error. Please check your connection and try again.');
            } finally {
                isLoading = false;
                loading.style.display = 'none';
            }
        }
        messageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const message = messageInput.value.trim();
            if (message && !isLoading) {
                sendMessage(message);
            }
        });
        function sendQuickMessage(message) {
            if (!isLoading) {
                sendMessage(message);
            }
        }
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const message = messageInput.value.trim();
                if (message && !isLoading) {
                    sendMessage(message);
                }
            }
        });
        async function clearConversation() {
            if (confirm('Are you sure you want to clear the conversation?')) {
                try {
                    const response = await fetch('/clear', { 
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        }
                    });
                    if (response.ok) {
                        chatMessages.innerHTML = '';
                        addMessage('bot', 'Hello! I\'m your ECO Matrix AI Assistant. How can I help you today?');
                    } else {
                        const errorText = await response.text();
                        console.error('Failed to clear conversation:', errorText);
                        alert('Failed to clear conversation on server. Please try refreshing the page.');
                    }
                } catch (error) {
                    console.error('Error clearing conversation:', error);
                    alert('Error communicating with server to clear conversation.');
                }
            }
        }
        document.addEventListener('DOMContentLoaded', () => {
            addMessage('bot', 'Hello! I\'m your ECO Matrix AI Assistant. How can I help you today?');
        });
    </script>
</body>
</html>
"""

def render_template(template, **context):
    return render_template_string(template, **context)

@app.route('/')
def index():
    return render_template(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({"success": False, "error": "Message cannot be empty."}), 400
    response = chatbot.generate_response(user_message)
    logging.info(f"User: {user_message}")
    logging.info(f"Bot: {response}")
    return jsonify({"success": True, "response": response})

@app.route('/clear', methods=['POST'])
def clear_conversation():
    logging.info("Conversation cleared by user.")
    return jsonify({"success": True, "response": "Conversation cleared. Hello! I'm your ECO Matrix AI Assistant. How can I help you today?"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
