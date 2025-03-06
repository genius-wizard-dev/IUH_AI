import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import { User } from "firebase/auth";
import { Copy } from "lucide-react"; // Import Copy icon
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Message, Step } from "../types";

interface MessageListProps {
  messages: Message[];
  image: string;
  currentUser: User | null;
  renderStepIndicator: (step?: Step | string) => JSX.Element | null;
}

const MessageList: React.FC<MessageListProps> = ({
  messages,
  image,
  currentUser,
  renderStepIndicator,
}) => {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const handleCopyToClipboard = (text: string, index: number) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopiedIndex(index);
      setTimeout(() => setCopiedIndex(null), 2000);
    });
  };

  return (
    <div className="space-y-6">
      {messages.map((message, index) => (
        <div
          key={index}
          className={cn(
            "flex gap-2 md:gap-3",
            message.role === "user" ? "flex-row-reverse" : ""
          )}
        >
          <div
            className={cn(
              "hidden md:flex h-10 w-10 rounded-full overflow-hidden flex-shrink-0",
              message.role === "user" ? "bg-teal-600" : "bg-gray-200"
            )}
          >
            {message.role === "user" ? (
              currentUser?.photoURL ? (
                <img
                  src={currentUser.photoURL}
                  alt="User"
                  className="h-full w-full object-cover"
                />
              ) : (
                <Avatar className="h-9 w-9 border border-gray-200 dark:border-gray-700">
                  <AvatarImage
                    src={currentUser?.photoURL || ""}
                    className="object-cover"
                  />
                  <AvatarFallback className="bg-blue-500 text-white text-sm font-medium">
                    {currentUser?.displayName?.[0].toUpperCase()}
                  </AvatarFallback>
                </Avatar>
              )
            ) : (
              <img
                src={image}
                alt="AI"
                className="h-full w-full object-cover border-2 border-gray-200 rounded-full shadow-sm"
              />
            )}
          </div>
          <div
            className={cn(
              "rounded-lg px-3 md:px-4 py-2 max-w-[95%] md:max-w-[100%]",
              message.role === "user"
                ? "bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-md flex"
                : ""
            )}
          >
            <div className="relative flex items-center justify-center">
              {message.isTyping ? (
                <div className="prose prose-sm dark:prose-invert">
                  {renderStepIndicator("processing")}
                </div>
              ) : message.role === "assistant" ? (
                <>
                  <ReactMarkdown
                    components={{
                      a: ({ node, ...props }) => (
                        <a
                          {...props}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-500 font-normal"
                        />
                      ),
                    }}
                    className="prose prose-sm dark:prose-invert text-[16px]"
                  >
                    {message.content}
                  </ReactMarkdown>
                </>
              ) : (
                <p className="whitespace-pre-wrap font-normal text-white">
                  {message.content}
                </p>
              )}
            </div>
            <div className="flex items-center mt-2 justify-between">
              {message.responseTime && (
                <div className="text-xs text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 rounded-md px-2 py-1 inline-flex items-center">
                  <span className="font-medium mr-1">Phản hồi:</span>
                  {Math.round(Number(message.responseTime))}s
                </div>
              )}
              {message.role === "assistant" && message.responseTime && (
                <button
                  onClick={() => handleCopyToClipboard(message.content, index)}
                  className={`flex items-center text-xs rounded-md px-2 py-1 transition-all duration-200 ${
                    copiedIndex === index
                      ? "bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400"
                      : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-blue-100 dark:hover:bg-blue-900 hover:text-blue-600 dark:hover:text-blue-400"
                  }`}
                  title="Copy to clipboard"
                >
                  {copiedIndex === index ? (
                    <span className="text-xs font-medium flex items-center">
                      Copied!
                    </span>
                  ) : (
                    <div className="flex items-center">
                      <Copy size={14} className="mr-1" />
                      <span>Copy</span>
                    </div>
                  )}
                </button>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MessageList;
