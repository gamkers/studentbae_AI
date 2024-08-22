import React from 'react';
import { FaArrowLeft } from 'react-icons/fa';
import './Chat.css';

function TopBar({ currentChat, toggleSidebar }) {
    return (
        <div className="top-bar">
            <button className="menu-toggle" onClick={toggleSidebar}><FaArrowLeft /></button>
            <h2>{currentChat || 'New Chat'}</h2>
            <div className="user-profile"></div>
        </div>
    );
}

export default TopBar;
