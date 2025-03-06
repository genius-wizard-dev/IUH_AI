export interface Message {
  role: "user" | "assistant";
  content: string;
  responseTime?: string;
  isTyping?: boolean;
}

export interface Step {
  text: string;
  completed: boolean;
}
