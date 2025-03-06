import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { AlertCircle } from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import image from "../assets/images.png";
import { useAuth } from "../utils/useAuth";

export default function Login() {
  const { signInWithGoogle, currentUser } = useAuth();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (currentUser) {
      navigate("/chat");
    }
  }, [currentUser, navigate]);

  const handleGoogleSignIn = async () => {
    try {
      setError("");
      setLoading(true);
      await signInWithGoogle();
      navigate("/chat");
    } catch (error) {
      setError("Đăng nhập bằng Google thất bại: " + error);
    }
    setLoading(false);
  };

  return (
    <div className="h-screen flex items-center justify-center relative overflow-hidden bg-gradient-to-tr from-blue-500/5 via-white to-blue-500/10 max-h-[100dvh]">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -right-[40%] -top-[40%] w-[80%] h-[80%] rounded-full bg-blue-500/5 blur-3xl" />
        <div className="absolute -left-[20%] -bottom-[30%] w-[60%] h-[60%] rounded-full bg-blue-500/5 blur-3xl" />
      </div>

      <div className="w-full max-w-md px-4 py-2 relative">
        <Card className="w-full bg-white/90 backdrop-blur-xl p-5 sm:p-7 md:p-9 rounded-3xl border border-blue-500/10 shadow-xl shadow-blue-500/5">
          <div className="flex flex-col items-center mb-8 sm:mb-12">
            <div className="relative mb-6 flex items-center justify-center">
              <div className="w-24 h-24 bg-gradient-to-tr from-blue-500/10 to-blue-500/5 rounded-3xl flex items-center justify-center border border-blue-400/30 shadow-md shadow-blue-500/10">
                <img
                  src={image}
                  alt="IUH Logo"
                  className="w-16 h-16 object-contain drop-shadow-lg"
                />
              </div>
              <div className="absolute inset-0 rounded-full bg-blue-400/10 blur-2xl opacity-40 -z-10 animate-pulse" />
            </div>

            <h2 className="text-2xl sm:text-3xl text-gray-800 text-center mb-3 bg-clip-text text-transparent bg-gradient-to-r font-extrabold from-blue-500 to-blue-700">
              Đăng nhập IUH AI
            </h2>
            <p className="text-gray-600 text-center max-w-[280px] text-sm sm:text-base">
              Trợ lý thông minh cho sinh viên IUH
            </p>
          </div>

          {/* Error Alert */}
          {error && (
            <Alert
              variant="destructive"
              className="mb-7 bg-red-50/80 backdrop-blur-sm border-red-100 animate-shake"
            >
              <AlertCircle className="h-4 w-4" />
              <AlertDescription className="text-red-600 text-sm">
                {error}
              </AlertDescription>
            </Alert>
          )}

          {/* Login Button */}
          <Button
            className="w-full h-16 sm:h-18 bg-white hover:bg-gray-50 text-gray-800 border border-gray-200
           flex items-center justify-center gap-3 rounded-2xl text-lg font-medium my-4
           transition-all duration-300 hover:shadow-lg hover:scale-[1.02] active:scale-[0.98]"
            variant="outline"
            onClick={handleGoogleSignIn}
            disabled={loading}
          >
            {!loading ? (
              <>
                <div className="w-8 h-8 relative">
                  <img
                    src="/google.png"
                    alt="Google"
                    className="w-full h-full object-contain"
                  />
                </div>
                <span className="text-gray-800">Đăng nhập với Google</span>
              </>
            ) : (
              <div className="flex items-center gap-3">
                <div className="w-6 h-6 border-2 border-gray-600/20 border-t-gray-600 rounded-full animate-spin" />
                <span>Đang xử lý...</span>
              </div>
            )}
          </Button>

          {/* Footer */}
          <div className="mt-8 sm:mt-12 text-center">
            <div
              className="inline-flex items-center gap-2 px-3 py-2 sm:px-4 sm:py-3 rounded-full
            bg-gradient-to-r from-blue-500/5 to-blue-500/10 text-xs sm:text-sm text-blue-500
            border border-blue-500/10 transition-all duration-300 hover:shadow-md"
            >
              <svg
                className="w-3 h-3 sm:w-4 sm:h-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span>Được phát triển bởi IUH AI Groups</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
