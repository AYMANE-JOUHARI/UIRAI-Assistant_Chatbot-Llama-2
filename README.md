# UIRAI-Llama-2-Assistant_Chatbot

## Project Overview
UIRAI-Llama-2-Assistant_Chatbot is a Llama 2-based AI Assistant designed for Université Internationale de Rabat (UIR) to help students efficiently handle queries and retrieve relevant information. This chatbot leverages natural language processing (NLP) capabilities to interact in a friendly and helpful manner.

## Key Features
- **Retrieval-Augmented Generation (RAG)**: Efficient document search and knowledge retrieval using Pinecone.
- **Interactive User Interface**: Built with Streamlit, offering text and text-to-speech capabilities for an enhanced user experience.
- **High Query Precision**: Achieved a 20% improvement in accuracy and a response time of 7.44 seconds.
- **User Satisfaction**: Optimized performance with an average satisfaction score of 8/10 for search-based interactions.

## Technologies Used
- **Llama 2**: Large language model for conversational responses.
- **LangChain**: Framework for building LLM-powered applications.
- **Pinecone**: Vector database used for embedding storage and similarity search.
- **Streamlit**: Web-based interface for user interaction.
- **gTTS**: Google Text-to-Speech for audio output.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AYMANE-JOUHARI/UIRAI-Llama-2-Assistant_Chatbot.git
   cd UIRAI-Llama-2-Assistant_Chatbot
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then install the required packages using:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**:
   - **OpenAI**: Add your OpenAI API key in the appropriate configuration or code file (`utils.py` in this case).
   - **Pinecone**: Set up your Pinecone API key and environment.
   - Ensure that sensitive data (like API keys) is managed securely and not hard-coded in the code.

## Usage

1. **Run the Chatbot Application**:
   Start the chatbot using Streamlit:
   ```bash
   streamlit run main.py
   ```

2. **Interface**:
   - Enter your query in the text box, and the chatbot will respond accordingly.
   - Audio responses are available for queries using Google Text-to-Speech.

3. **Expected Output**:
   - Real-time query refinement and response from the chatbot.
   - Visual feedback on interaction history and refined queries.

## Project Structure

```
UIRAI-Llama-2-Assistant_Chatbot/
├── main.py              # Streamlit app for chatbot interface
├── utils.py             # Utility functions for embeddings and querying
├── requirements.txt     # Python dependencies
├── UIR.png              # Project logo for the UI
├── README.md            # Project README file
└── final_report.pdf     # Project report with detailed documentation
```

## Future Improvements
- **Support for Additional Languages**: Enhance the chatbot’s ability to respond in multiple languages.
- **User Feedback Collection**: Implement a feedback loop to improve response quality.
- **Integration with Other LLMs**: Test and add other models for more diverse responses.

## License
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/
