import React, { createContext, useCallback, useContext, useState } from "react";

export interface Message {
  id: number;
  author: string;
  text: string;
  timestamp: Date;
}

export interface MessageContext {
  messages: Message[];
  addMessage: (message: Pick<Message, "author" | "text">) => void;
}

const MessageContext = createContext<MessageContext>({
  messages: [],
  addMessage: () => {},
});

export function useMessageContext() {
  return useContext(MessageContext);
}

export function MessageProvider({ children }: { children: React.ReactNode }) {
  const [messages, setMessages] = useState<Message[]>([]);

  const addMessage = useCallback(
    (message: Pick<Message, "author" | "text">) => {
      setMessages((messages) => [
        ...messages,
        { ...message, id: messages.length, timestamp: new Date() },
      ]);
    },
    []
  );

  return (
    <MessageContext.Provider value={{ messages, addMessage }}>
      {children}
    </MessageContext.Provider>
  );
}
