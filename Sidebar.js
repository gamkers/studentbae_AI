import React from 'react';
import './Chat.css'; 

function Sidebar({ isSidebarOpen, setCurrentChat }) {
    const chatHistory = [
        "Collaboration Inquiry Details",
        "Ethical Hacking Course Outline",
        "Saving Session Data React",
        // Add more chat history items
    ];

    return (
        <div className={`sidebar ${isSidebarOpen ? 'open' : 'closed'}`}>
            <div className="sidebar-header">
                <h1>ChatGPT</h1>
            </div>
            <nav>
                <ul>
                    <li>GamkersGPT</li>
                    <li>Studentbae</li>
                    <li>InterviewAI</li>
                </ul>
            </nav>
            <div className="chat-history">
                <h2>Today</h2>
                <ul>
                    {chatHistory.map((chat, index) => (
                        <li key={index} onClick={() => setCurrentChat(chat)}>{chat}</li>
                    ))}
                </ul>
            </div>
            <button className="upgrade-button">Upgrade plan</button>
        </div>
    );
}

export default Sidebar;
