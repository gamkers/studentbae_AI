import React, { useState, useEffect } from 'react';
import './Chat.css';  // Import the CSS for the Chat component
import { marked } from 'marked'; // Import marked library for Markdown parsing

function Chat() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Add user message to the chat
        setMessages([...messages, { text: input, type: 'user' }]);
        
        try {
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: input }),
            });

            const data = await response.json();
            
            // Parse Markdown to HTML using marked
            const formattedReply = marked(data.reply);
            
            // Add bot response to the chat
            setMessages([...messages, { text: input, type: 'user' }, { text: formattedReply, type: 'bot' }]);
            setInput(''); // Clear input field
        } catch (error) {
            console.error('Error:', error);
        }
    };

    useEffect(() => {
        const codeBlocks = document.querySelectorAll('pre');

        codeBlocks.forEach((block) => {
            // Check if button already exists to prevent duplicates
            if (block.previousElementSibling && block.previousElementSibling.className === 'copy-button') {
                return;
            }

            // Create the copy button
            const button = document.createElement('button');
            button.className = 'copy-button';
            button.textContent = 'Copy';

            // Add button to the block container
            block.parentElement.insertBefore(button, block);

            // Add click event to copy code to clipboard
            button.addEventListener('click', () => {
                const code = block.innerText;
                navigator.clipboard.writeText(code).then(() => {
                    alert('Code copied to clipboard!');
                }).catch(err => {
                    console.error('Failed to copy code: ', err);
                });
            });
        });
    }, [messages]); // Dependency array ensures effect runs when messages change

    return (
        <div className="chat-container">
            <div className="chat-box">
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`message ${msg.type}`}
                        dangerouslySetInnerHTML={{ __html: msg.text }}
                    />
                ))}

                
            </div>
            <div className="chat-input">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                />
                <button onClick={handleSubmit}>➤</button>
            </div>
        </div>
    );
}

export default Chat;
