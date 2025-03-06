import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { User } from "firebase/auth";

interface ProfileDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  currentUser: User | null;
}

const ProfileDialog: React.FC<ProfileDialogProps> = ({
  open,
  onOpenChange,
  currentUser,
}) => (
  <Dialog open={open} onOpenChange={onOpenChange}>
    <DialogContent className="sm:max-w-md rounded-3xl shadow-2xl border border-gray-200 p-4 sm:p-6 bg-white max-w-[90vw]">
      <DialogHeader className="pb-3 sm:pb-4 border-b border-gray-100">
        <DialogTitle className="text-xl sm:text-2xl font-bold text-blue-600">
          Tài khoản
        </DialogTitle>
        <DialogDescription className="text-gray-500 text-sm sm:text-base mt-1">
          Thông tin tài khoản của bạn
        </DialogDescription>
      </DialogHeader>
      <div className="flex flex-col items-center gap-4 sm:gap-8 py-5 sm:py-8">
        <div className="relative group">
          <div className="absolute -inset-1 bg-blue-500 rounded-full blur-md opacity-70 group-hover:opacity-100 transition duration-300"></div>
          <Avatar className="h-20 w-20 sm:h-28 sm:w-28 border-4 border-white shadow-lg relative">
            <AvatarImage
              src={currentUser?.photoURL || ""}
              className="object-cover"
            />
            <AvatarFallback className="bg-blue-600 text-white text-xl sm:text-2xl font-bold">
              {currentUser?.displayName?.[0].toUpperCase()}
            </AvatarFallback>
          </Avatar>
        </div>
        <div className="text-center space-y-1 sm:space-y-2 w-full px-2">
          <h3 className="text-xl sm:text-2xl font-semibold text-black tracking-tight truncate">
            {currentUser?.displayName || "User"}
          </h3>
          <p className="text-gray-700 text-sm sm:text-base flex items-center justify-center gap-1.5 break-all">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w-4 sm:h-5 sm:w-5 flex-shrink-0"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
              <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
            </svg>
            <span className="truncate">{currentUser?.email}</span>
          </p>
        </div>
      </div>
      <div className="mt-1 sm:mt-2 pt-3 sm:pt-4 border-t border-gray-100 flex justify-end">
        <button
          className="px-3 sm:px-4 py-1.5 sm:py-2 rounded-full bg-blue-600 text-white font-medium text-sm
          hover:bg-blue-700 hover:shadow-lg transition-all duration-300
          transform hover:-translate-y-0.5 active:translate-y-0 active:shadow-md
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          onClick={() => onOpenChange(false)}
        >
          Đóng
        </button>
      </div>
    </DialogContent>
  </Dialog>
);

export default ProfileDialog;
