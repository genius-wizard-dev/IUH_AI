import { Brain } from "lucide-react";

const WelcomeMessage: React.FC = () => (
  <div className="flex flex-col items-center justify-center mt-10 sm:mt-6 text-center px-4 space-y-10">
    {/* Icon Section */}
    <div className="relative group">
      <div className="w-20 h-20 bg-gradient-to-br from-blue-50 via-blue-100 to-blue-200 dark:from-blue-900/50 dark:via-blue-800/50 dark:to-blue-900/50 rounded-3xl flex items-center justify-center shadow-lg ring-8 ring-blue-100/50 dark:ring-blue-900/20 transition-all duration-300 group-hover:scale-105">
        <Brain className="w-12 h-12 text-blue-500 dark:text-blue-300 transition-transform duration-300 group-hover:rotate-12" />
      </div>
      <span className="absolute -top-1 -right-1 w-4 h-4 bg-blue-400 rounded-full border-2 border-white dark:border-black animate-ping opacity-60" />
      <span className="absolute -top-1 -right-1 w-4 h-4 bg-blue-500 rounded-full animate-pulse opacity-80" />
    </div>

    {/* Content Section */}
    <div className="space-y-8 max-w-2xl">
      <p className="text-2xl text-blue-500 dark:text-gray-300 leading-relaxed font-semibold mx-auto max-w-md">
        Trợ lý AI thông minh từ IUH, sẵn sàng hỗ trợ bạn mọi thắc mắc về tuyển
        sinh!
      </p>

      {/* Suggestion Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-lg mx-auto">
        {[
          {
            title: "Thông tin tuyển sinh",
            desc: "Tìm hiểu ngành học, điểm chuẩn, học phí...",
          },
          {
            title: "Quy trình xét tuyển",
            desc: "Hướng dẫn đăng ký và quy trình xét duyệt",
          },
        ].map((item, idx) => (
          <div
            key={idx}
            className="relative bg-white dark:bg-gray-800/50 p-5 rounded-2xl shadow-md border border-gray-100/50 dark:border-gray-700/30 hover:border-blue-300 dark:hover:border-blue-500/50 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2 group"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-900/20 opacity-0 group-hover:opacity-100 rounded-2xl transition-opacity duration-300" />
            <h3 className="relative z-10 text-lg font-semibold text-gray-900 dark:text-gray-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
              {item.title}
            </h3>
            <p className="relative z-10 text-sm text-gray-500 dark:text-gray-400 mt-2 leading-relaxed">
              {item.desc}
            </p>
          </div>
        ))}
      </div>
    </div>
  </div>
);

export default WelcomeMessage;
