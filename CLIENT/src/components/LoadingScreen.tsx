import { Loader2 } from "lucide-react";

const LoadingScreen: React.FC = () => (
  <div className="fixed inset-0 flex items-center justify-center bg-white">
    <div className="text-center space-y-4 bg-white/10 backdrop-blur-xl p-6 rounded-2xl shadow-lg border border-blue-800/30">
      <div className="h-14 w-14 bg-blue-600/20 rounded-full flex items-center justify-center mx-auto">
        <Loader2 className="h-7 w-7 animate-spin text-blue-500" />
      </div>
      <h2 className="text-xl font-medium text-blue-600">Đang kết nối...</h2>
      <p className="text-sm text-black">Vui lòng đợi trong giây lát</p>
    </div>
  </div>
);

export default LoadingScreen;
