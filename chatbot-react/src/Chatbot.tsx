import { useState } from "react";
import axios from "axios";
import { TextField, Button, Box, Paper, Typography } from "@mui/material";

interface Message {
  text: string;
  sender: "user" | "bot";
}

export default function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages: Message[] = [
      ...messages,
      { text: input, sender: "user" },
    ];
    setMessages(newMessages);
    setInput("");

    try {
      const response = await axios.post<{ response: string }>(
        "http://localhost:5000/agent",
        { prompt: input }
      );
      setMessages([
        ...newMessages,
        { text: response.data.response, sender: "bot" },
      ]);
    } catch (error) {
      console.error("Error communicating with server:", error);
      setMessages([
        ...newMessages,
        { text: "Error connecting to server.", sender: "bot" },
      ]);
    }
  };

  return (
    <Box
      sx={{
        maxWidth: 400,
        mx: "auto",
        mt: 4,
        p: 2,
        borderRadius: 2,
        boxShadow: 3,
      }}
    >
      <Paper sx={{ height: 300, overflowY: "auto", p: 2, mb: 2 }}>
        {messages.map((msg, index) => (
          <Typography
            key={index}
            sx={{
              p: 1,
              my: 1,
              borderRadius: 1,
              bgcolor: msg.sender === "user" ? "primary.main" : "grey.300",
              color: msg.sender === "user" ? "white" : "black",
              textAlign: msg.sender === "user" ? "right" : "left",
            }}
          >
            {msg.text}
          </Typography>
        ))}
      </Paper>
      <Box sx={{ display: "flex", gap: 1 }}>
        <TextField
          fullWidth
          variant="outlined"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <Button variant="contained" color="primary" onClick={sendMessage}>
          Send
        </Button>
      </Box>
    </Box>
  );
}
