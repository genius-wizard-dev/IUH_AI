import { ScrollArea } from "@/components/ui/scroll-area";
import { User } from "firebase/auth";
import { RefObject } from "react";
import { Message, Step } from "../types";
import MessageList from "./MessageList";
import WelcomeMessage from "./WelcomeMessage";
interface ChatMainProps {
  messages: Message[];
  image: string;
  currentUser: User | null;
  scrollRef: RefObject<HTMLDivElement>;
  renderStepIndicator: (step?: Step | string | null) => JSX.Element;
}

const ChatMain: React.FC<ChatMainProps> = ({
  messages,
  image,
  currentUser,
  scrollRef,
  renderStepIndicator,
}) => (
  <main className="flex-1 overflow-hidden relative bg-white dark:bg-black flex items-center justify-center">
    <ScrollArea className="h-full w-full px-4">
      <div className="max-w-4xl mx-auto py-6 space-y-6">
        {messages.length === 0 ? (
          <WelcomeMessage />
        ) : (
          <MessageList
            messages={messages}
            image={image}
            currentUser={currentUser}
            renderStepIndicator={renderStepIndicator}
          />
        )}
        <div ref={scrollRef} />
      </div>
    </ScrollArea>
  </main>
);

export default ChatMain;
