import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { User } from "firebase/auth";
import { LogOut, SquarePen, UserIcon } from "lucide-react";

interface ChatHeaderProps {
  currentUser: User | null;
  onNewChat: () => void;
  onShowProfile: () => void;
  onLogout: () => void;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({
  currentUser,
  onNewChat,
  onShowProfile,
  onLogout,
}) => (
  <header className="flex items-center justify-between px-3 sm:px-6 py-2 sm:py-3 bg-white dark:bg-black border-b border-gray-200 dark:border-gray-800 sticky top-0 z-50 shadow-sm">
    {/* Left Section */}
    <div className="flex items-center gap-2 sm:gap-4">
      <a
        className="relative group cursor-pointer border-2 rounded-full border-blue-500"
        href="/chat"
      >
        <img
          src="/logo.png"
          alt="IUH Logo"
          className="w-8 h-8 sm:w-10 sm:h-10 rounded-full object-cover shadow-sm transition-all duration-200 group-hover:scale-105"
        />
      </a>
      <div className="flex flex-col">
        <h1 className="hidden sm:block text-lg sm:text-xl font-bold tracking-tight text-blue-500 dark:text-white">
          IUH AI TVTS
        </h1>
        <p className="hidden xs:block text-xs text-gray-500 dark:text-gray-400 font-medium">
          Phát triển bởi IUH AI Groups
        </p>
      </div>
    </div>

    <div className="flex items-center gap-2 sm:gap-3">
      <div className="relative group">
        <Button
          onClick={onNewChat}
          variant="ghost"
          size="icon"
          className="rounded-full hover:bg-blue-100 dark:hover:bg-blue-800 transition-colors hover:scale-110 p-2 sm:p-3 h-auto w-auto"
          aria-label="Trò chuyện mới"
        >
          <SquarePen className="w-7 h-7 sm:w-6 sm:h-6 text-blue-600 dark:text-blue-400" />
        </Button>
        <span className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 bg-gray-900 text-white text-xs rounded px-2 py-1 whitespace-nowrap pointer-events-none">
          Trò chuyện mới
        </span>
      </div>

      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            size="icon"
            className="rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors p-1 h-auto w-auto"
          >
            <Avatar className="h-10 w-10 sm:h-9 sm:w-9 border border-gray-200 dark:border-gray-700">
              <AvatarImage
                src={currentUser?.photoURL || ""}
                className="object-cover"
              />
              <AvatarFallback className="bg-blue-500 text-white text-sm font-medium">
                {currentUser?.displayName?.[0].toUpperCase()}
              </AvatarFallback>
            </Avatar>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent
          align="end"
          className="w-56 sm:w-60 mt-2 bg-white dark:bg-gray-900 rounded-lg shadow-xl border border-gray-200 dark:border-gray-800 overflow-hidden"
        >
          <div className="px-4 sm:px-5 py-3 sm:py-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20">
            <p className="text-sm font-semibold text-gray-800 dark:text-white truncate">
              {currentUser?.displayName || currentUser?.email}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Người dùng
            </p>
          </div>
          <DropdownMenuSeparator className="h-px bg-gray-200 dark:bg-gray-800" />
          <DropdownMenuItem
            onClick={onShowProfile}
            className="flex items-center gap-3 px-4 py-3 sm:py-2.5 text-sm cursor-pointer hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors duration-200"
          >
            <UserIcon className="w-5 h-5 sm:w-4 sm:h-4 text-blue-600 dark:text-blue-400" />
            <span className="font-medium">Tài khoản</span>
          </DropdownMenuItem>
          <DropdownMenuItem
            onClick={onLogout}
            className="flex items-center gap-3 px-4 py-3 sm:py-2.5 text-sm cursor-pointer hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors duration-200 text-red-600 dark:text-red-400"
          >
            <LogOut className="w-5 h-5 sm:w-4 sm:h-4" />
            <span className="font-medium">Đăng xuất</span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  </header>
);

export default ChatHeader;
