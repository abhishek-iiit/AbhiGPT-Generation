import { useState } from 'react';
import './ChatBox.css';

function ChatBox() {
    const [question, setQuestion] = useState('');
    const [messages, setMessages] = useState([]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!question.trim()) return;
        
        const response = await fetch('http://localhost:8000/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question }),
        });
        const data = await response.json();
        
        setMessages(prev => [...prev, {
            question: question,
            answer: data.answer.content,
            id: Date.now()
        }]);
        setQuestion('');
    };

    const formatAnswer = (answerText) => {
        let formattedAnswer = answerText
            .replace(/\n/g, '<br />')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/`(.*?)`/g, '<code class="inline-code">$1</code>')
            .replace(/```(\w+)?\s([\s\S]*?)```/g, (match, lang, code) => {
                return `<pre class="code-block"><code class="${lang || ''}">${code.trim()}</code></pre>`;
            });

        return formattedAnswer;
    };

    return (
        <div className="chat-container">
            <div className="message-list">
                {messages.map((message) => (
                    <div key={message.id} className="message-group">
                        <div className="user-question">
                            <div className="question-bubble">{message.question}</div>
                        </div>
                        <div className="assistant-answer">
                            <div 
                                className="answer-content"
                                dangerouslySetInnerHTML={{ __html: formatAnswer(message.answer) }}
                            />
                        </div>
                    </div>
                ))}
            </div>

            <form className="input-container" onSubmit={handleSubmit}>
                <div className="input-wrapper">
                    <input
                        type="text"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        placeholder="Ask a question about your code..."
                    />
                    <button type="submit" className="send-button">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
                            <path fill="currentColor" d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                        </svg>
                    </button>
                </div>
            </form>
        </div>
    );
}

export default ChatBox;