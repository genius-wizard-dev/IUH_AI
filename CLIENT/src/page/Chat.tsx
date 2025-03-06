import { useAuth } from "@/utils/useAuth";
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import ChatFooter from "../components/ChatFooter";
import ChatHeader from "../components/ChatHeader";
import ChatMain from "../components/ChatMain";
import LoadingScreen from "../components/LoadingScreen";
import ProfileDialog from "../components/ProfileDialog";
import StepIndicator from "../components/StepIndicator";
import { Message, Step } from "../types";
import { countWords, generateChatId } from "../utils/chatUtils";

const App: React.FC = () => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  // const [isOverload, setIsOverload] = useState(false);
  // const [showAlert, setShowAlert] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const [isSearch, setIsSearch] = useState(false);
  // const MESSAGE_LIMIT = 10;
  const { currentUser, logOut } = useAuth();
  const [showProfile, setShowProfile] = useState(false);
  const [chatId, setChatId] = useState<string>("");
  const navigate = useNavigate();
  const WORD_LIMIT = 100;
  const [wordCount, setWordCount] = useState(0);
  const [currentStep, setCurrentStep] = useState<string | null>(null);
  const [steps, setSteps] = useState<Step[]>([]);

  const handleLogout = async () => {
    try {
      await logOut();
      navigate("/login");
    } catch (error) {
      console.error("Failed to log out", error);
    }
  };

  useEffect(() => {
    if (!chatId) return;
    const wsUrl = `${import.meta.env.VITE_SOCKET_URL}/${chatId}`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log("WebSocket Connected");
      setSocket(ws);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("Received WebSocket data:", data);

      if (data.status === "Processing") {
        console.log("Processing step:", data.step);
        setCurrentStep(data.step);
      } else if (data.message) {
        setCurrentStep(null);
        setMessages((prevMessages) => {
          const typingIndex = prevMessages.findIndex((msg) => msg.isTyping);
          if (typingIndex !== -1) {
            const updatedMessages = [...prevMessages];
            updatedMessages[typingIndex] = {
              role: "assistant",
              content: data.message,
              responseTime: data.time,
              isTyping: false,
            };
            return updatedMessages;
          }
          return prevMessages;
        });
        setIsLoading(false);
      } else if (data.error) {
        console.error("Error from server:", data.error);
        setIsLoading(false);
        setCurrentStep(null);
      }
    };

    ws.onerror = (error) => console.error("WebSocket error:", error);
    ws.onclose = () => setSocket(null);

    return () => {
      if (ws.readyState !== WebSocket.CLOSED) ws.close();
    };
  }, [chatId]);

  useEffect(() => {
    setChatId(generateChatId());
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isLoading, currentStep]);

  const handleNewChat = () => {
    setMessages([]);
    setInput("");
    setChatId(generateChatId());
    // setIsOverload(false);
    setIsSearch(false);
    setCurrentStep(null);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // if (isOverload || !input.trim() || !socket) return;
    if (!input.trim() || !socket) return;
    setIsLoading(true);
    const userMessage = input.trim();
    setInput("");
    // if (messages.length >= MESSAGE_LIMIT - 1) setIsOverload(true);
    setSteps([]);
    setWordCount(0);
    setCurrentStep(null);
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    socket.send(
      JSON.stringify({
        question: userMessage,
        chat_id: chatId,
        user_name: currentUser?.displayName ?? "User",
        is_search: isSearch,
      })
    );
    setMessages((prev) => [
      ...prev,
      { role: "assistant", content: "Đang xử lý...", isTyping: true },
    ]);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const text = e.target.value;
    const words = countWords(text);
    if (words <= WORD_LIMIT) {
      setInput(text);
      setWordCount(words);
    } else {
      const wordsArray = text.split(/\s+/);
      const trimmedText = wordsArray.slice(0, WORD_LIMIT).join(" ");
      setInput(trimmedText);
      setWordCount(WORD_LIMIT);
    }
  };

  useEffect(() => {
    if (currentStep) {
      console.log("Setting steps with currentStep:", currentStep);
      setSteps((prev) => {
        const existingStep = prev.find((s) => s.text === currentStep);
        if (existingStep) {
          return prev.map((s) =>
            s.text === currentStep
              ? { ...s, completed: false }
              : { ...s, completed: true }
          );
        } else {
          return [
            ...prev.map((s) => ({ ...s, completed: true })),
            { text: currentStep, completed: false },
          ];
        }
      });
    }
  }, [currentStep]);

  const renderStepIndicator = (step?: Step | string | null): JSX.Element => {
    console.log("Rendering step indicator:", step, "steps:", steps);
    return steps.length > 0 ? <StepIndicator steps={steps} /> : <></>;
  };

  return socket ? (
    <div className="flex flex-col h-screen bg-white dark:bg-gray-900 font-sans relative overflow-hidden max-h-[100dvh]">
      <div className="absolute inset-0 bg-gradient-to-tr from-teal-50/30 via-transparent to-purple-50/30 dark:from-teal-900/10 dark:to-purple-900/10" />
      <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-5" />
      <ChatHeader
        currentUser={currentUser}
        onNewChat={handleNewChat}
        onShowProfile={() => setShowProfile(true)}
        onLogout={handleLogout}
      />
      <div className="flex-1 overflow-auto">
        <ChatMain
          messages={messages}
          image="/logo.png"
          currentUser={currentUser}
          scrollRef={scrollRef}
          renderStepIndicator={renderStepIndicator}
        />
      </div>
      <ChatFooter
        input={input}
        isLoading={isLoading}
        // isOverload={isOverload}
        isSearch={isSearch}
        messages={messages}
        wordCount={wordCount}
        onInputChange={handleInputChange}
        onSubmit={handleSubmit}
        onToggleSearch={() => setIsSearch(!isSearch)}
      />
      <ProfileDialog
        open={showProfile}
        onOpenChange={setShowProfile}
        currentUser={currentUser}
      />
    </div>
  ) : (
    <LoadingScreen />
  );
};

export default App;
