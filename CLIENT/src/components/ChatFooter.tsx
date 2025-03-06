import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { Globe, Loader2, Send } from "lucide-react";
import { Message } from "../types";

interface ChatFooterProps {
  input: string;
  isLoading: boolean;
  // isOverload: boolean;
  isSearch: boolean;
  messages: Message[];
  wordCount: number;
  onInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (e: React.FormEvent) => void;
  onToggleSearch: () => void;
}

const WORD_LIMIT = 50;

const ChatFooter: React.FC<ChatFooterProps> = ({
  input,
  isLoading,
  // isOverload,
  isSearch,
  wordCount,
  onInputChange,
  onSubmit,
  onToggleSearch,
}) => (
  <footer className="border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-black p-4 sm:p-6 sticky bottom-0 z-20 shadow-sm rounded-t-2xl sm:rounded-none">
    <div className="max-w-3xl mx-auto space-y-3 sm:space-y-3">
      <div className="flex justify-between items-center mb-3">
        <div className="sm:hidden">
          <span className="bg-gray-100 dark:bg-gray-800 px-3.5 py-2 rounded-full text-sm font-medium">
            {wordCount}/{WORD_LIMIT} từ
          </span>
        </div>
      </div>
      <form onSubmit={onSubmit} className="relative">
        <div className="relative flex items-center">
          <div className="relative">
            <button
              type="button"
              onClick={onToggleSearch}
              className={cn(
                "absolute left-2 sm:left-2 top-1/2 -translate-y-1/2 p-2.5 sm:p-2.5 rounded-full transition-colors border group",
                isSearch
                  ? "bg-blue-500 text-white border-blue-500"
                  : "text-gray-500 border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800"
              )}
              aria-label={
                isSearch
                  ? "Chuyển sang chế độ hỏi đáp"
                  : "Chuyển sang chế độ tìm kiếm"
              }
            >
              <Globe className="w-5 h-5 sm:w-4 sm:h-4" />
              <span className="hidden sm:block absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs bg-gray-800 text-white rounded opacity-0 group-hover:opacity-100 whitespace-nowrap pointer-events-none transition-opacity max-w-[90vw] overflow-hidden text-ellipsis">
                {isSearch ? "Chế độ hỏi đáp" : "Chế độ tìm kiếm"}
              </span>
            </button>
          </div>
          <Input
            placeholder={
              isSearch ? "Tìm kiếm thông minh..." : "Hỏi đáp tư vấn..."
            }
            value={input}
            onChange={onInputChange}
            disabled={isLoading}
            className="w-full pl-14 sm:pl-14 pr-14 sm:pr-16 py-7 sm:py-6 rounded-full border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 focus:outline-none text-base sm:text-base placeholder-gray-400 disabled:bg-gray-100 transition-all"
          />
          <Button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="absolute right-2 sm:right-2 top-1/2 -translate-y-1/2 rounded-full aspect-square p-2.5 sm:p-2.5 bg-blue-500 hover:bg-blue-600 text-white transition-colors disabled:opacity-50 disabled:bg-gray-400"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 sm:w-5 sm:h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5 sm:w-5 sm:h-5" />
            )}
          </Button>
        </div>
      </form>
      <div className="text-xs text-gray-500 dark:text-gray-400 text-center mt-4">
        <div className="flex items-center justify-center gap-3">
          <div className="hidden sm:flex items-center">
            <span className="bg-gray-100 text-black dark:bg-gray-800 px-3 py-1.5 rounded-full text-xs font-medium">
              {wordCount}/{WORD_LIMIT} từ
            </span>
          </div>
          <span className="hidden sm:inline">•</span>
          <span className="text-xs sm:text-xs font-medium">
            IUH AI đang thử nghiệm, phản hồi có thể chưa hoàn toàn chính xác.
          </span>
        </div>
      </div>
    </div>
  </footer>
);

export default ChatFooter;
