// import { Button } from "@/components/ui/button";
// import { Card } from "@/components/ui/card";
// import { ArrowLeft, Facebook, Linkedin } from "lucide-react";
// import { Link } from "react-router-dom";
// import image from "../assets/images.png";

// export default function About() {
//   return (
//     <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white p-4 sm:p-8">
//       <div className="max-w-4xl mx-auto">
//         <div className="mb-8">
//           <Link to="/chat">
//             <Button variant="ghost" className="gap-2">
//               <ArrowLeft className="h-4 w-4" />
//               Quay lại chat
//             </Button>
//           </Link>
//         </div>

//         <div className="flex flex-col items-center mb-12">
//           <div className="w-20 h-20 bg-[#10a37f]/10 rounded-2xl flex items-center justify-center mb-4">
//             <img src={image} alt="IUH Logo" className="w-12 h-12" />
//           </div>
//           <h1 className="text-3xl font-bold text-gray-800 text-center">
//             IUH AI{" "}
//           </h1>
//           <p className="text-gray-600 mt-2 text-center">
//             Trợ lý AI thông minh cho sinh viên IUH
//           </p>
//         </div>

//         <div className="grid gap-8">
//           <Card className="p-6">
//             <h2 className="text-xl font-semibold mb-4">Về Dự Án</h2>
//             <p className="text-gray-600 leading-relaxed">
//               IUH AI là một dự án được phát triển bởi sinh viên Trường Đại học
//               Công nghiệp TP.HCM (IUH). Dự án này đang trong giai đoạn thử
//               nghiệm, với mục tiêu tạo ra một trợ lý AI thông minh có khả năng
//               hỗ trợ sinh viên trong việc tìm hiểu thông tin về trường, ngành
//               học và các vấn đề liên quan đến học tập.
//             </p>
//           </Card>

//           <Card className="p-6">
//             <h2 className="text-xl font-semibold mb-4">Tính Năng</h2>
//             <ul className="list-disc list-inside space-y-2 text-gray-600">
//               <li>Trả lời các câu hỏi về tuyển sinh</li>
//               <li>Cung cấp thông tin về các ngành học tại IUH</li>
//               <li>Hỗ trợ giải đáp thắc mắc về quy chế, quy định của trường</li>
//             </ul>
//           </Card>

//           <Card className="p-6">
//             <h2 className="text-xl font-semibold mb-4">Người Phát Triển</h2>
//             <div className="space-y-4">
//               <p className="text-gray-600">
//                 Dự án được phát triển bởi Nguyễn Thành Thuận - Sinh viên khoa
//                 Công nghệ Thông tin, IUH.
//               </p>
//               <div className="flex flex-wrap gap-4">
//                 <Button variant="outline" className="gap-2">
//                   <Linkedin className="h-4 w-4" />
//                   <a
//                     href="https://www.linkedin.com/in/nguyen-thanh-thuan/"
//                     target="_blank"
//                     rel="noopener noreferrer"
//                   >
//                     LinkedIn
//                   </a>
//                 </Button>
//                 <Button variant="outline" className="gap-2">
//                   <Facebook className="h-4 w-4" />
//                   <a
//                     href="https://www.facebook.com/nguyen.thanh.thuan.it"
//                     target="_blank"
//                     rel="noopener noreferrer"
//                   >
//                     Facebook
//                   </a>
//                 </Button>
//               </div>
//             </div>
//           </Card>

//           <Card className="p-6">
//             <h2 className="text-xl font-semibold mb-4">Chính Sách Bảo Mật</h2>
//             <div className="space-y-4">
//               <p className="text-gray-600">
//                 Chúng tôi cam kết bảo vệ thông tin của người dùng. Dữ liệu từ
//                 các cuộc trò chuyện sẽ được:
//               </p>
//               <ul className="list-disc list-inside space-y-2 text-gray-600 ml-4">
//                 <li>Bảo mật an toàn</li>
//                 <li>
//                   Chỉ được sử dụng cho mục đích cải thiện và phát triển AI
//                 </li>
//                 <li>Không chia sẻ cho bên thứ ba mà không có sự đồng ý</li>
//                 <li>Xử lý tuân theo các quy định về bảo vệ dữ liệu</li>
//               </ul>
//             </div>
//           </Card>
//           <Card className="p-6 bg-orange-50/50">
//             <h2 className="text-xl font-semibold mb-4 text-orange-700">
//               Lưu ý
//             </h2>
//             <p className="text-orange-600">
//               Dự án đang trong giai đoạn thử nghiệm. Các câu trả lời của AI có
//               thể chưa hoàn toàn chính xác. Vui lòng tham khảo thêm thông tin
//               chính thức từ website của trường hoặc liên hệ trực tiếp với phòng
//               tuyển sinh để có thông tin chính xác nhất.
//             </p>
//           </Card>
//         </div>
//       </div>
//     </div>
//   );
// }
