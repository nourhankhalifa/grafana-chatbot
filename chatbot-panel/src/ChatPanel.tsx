import React, {useState} from 'react';
import { PanelProps } from '@grafana/data';
// import {getBackendSrv} from '@grafana/runtime';

interface ChatMessage {
    text: string;
    sender: 'user' | 'bot';
    timestamp: string;
  }

export const ChatPanel: React.FC<PanelProps> = ({width, height}) => {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState('');

    const sendMessage = async () => {
        if(!input.trim()){
            return
        };

        const userMessage: ChatMessage = {
            text: input,
            sender: 'user',
            timestamp: new Date().toDateString()
        };

        setMessages([...messages, userMessage]);
        setInput('');

        try {
            const res = await fetch('http://localhost:8000/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: input }),
            });
            const data = await res.json();
            // const res = await getBackendSrv().post('/api/plugins/custom-chatbot-panel/resources/logql-agent', {
            //     messages: input,
            //   });

            const botMessage: ChatMessage = {
                text: data.message,
                sender: 'bot',
                timestamp: new Date().toDateString()
            };

            setMessages(messages => [...messages, botMessage]);
        } 
        catch (err) {
            const defaultMessage: ChatMessage = {
                text: 'Error: could not contact agent.',
                sender: 'bot',
                timestamp: new Date().toDateString()
            };
            setMessages(messages => [...messages, defaultMessage]);
            console.error('Error sending messages: ', err)
        }
    };
    return (
        <div style={{ width, height, display: 'flex', flexDirection: 'column', padding: '10px'}}>
            <div style={{ flex: 1, overflow: 'auto', marginBottom: '10px'}}>
                {messages.map((msg, index) => (
                    <div key={index} style={{
                        textAlign: msg.sender === 'user' ? 'right' : 'left',
                        margin: '5px',
                        padding: '5px',
                        borderRadius: '10px',
                        backgroundColor: msg.sender === 'user' ? '#e6f3ff' : '#f0f0f0'
                    }}>
                        <pre>{JSON.stringify(msg.text, null, 2)}</pre>
                    </div>
                ))}
            </div>
            <div style={{ display: 'flex' }}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    style={{ flex: 1, marginRight: '10px', padding: '5px'}}
                />
                <button onClick={sendMessage} style={{ padding: '5px 10px'}}>Send</button>
            </div>
        </div>
    );
};
