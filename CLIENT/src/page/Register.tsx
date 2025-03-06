// import { Alert, AlertDescription } from "@/components/ui/alert";
// import { Button } from "@/components/ui/button";
// import {
//   Card,
//   CardContent,
//   CardDescription,
//   CardHeader,
//   CardTitle,
// } from "@/components/ui/card";
// import { AlertCircle, Chrome } from "lucide-react";
// import { useState } from "react";
// import { Link, useNavigate } from "react-router-dom";
// import { useAuth } from "../util/useAuth";

// export default function Register() {
//   const { signInWithGoogle } = useAuth();
//   const [error, setError] = useState("");
//   const [loading, setLoading] = useState(false);
//   const navigate = useNavigate();

//   const handleGoogleSignIn = async () => {
//     try {
//       setError("");
//       setLoading(true);
//       await signInWithGoogle();
//       navigate("/chat");
//     } catch (error) {
//       setError("Failed to sign up with Google");
//     }
//     setLoading(false);
//   };

//   return (
//     <div className="container mx-auto flex items-center justify-center min-h-screen px-4">
//       <div className="w-full max-w-md space-y-4">
//         <Card className="border-2">
//           <CardHeader className="space-y-3">
//             <CardTitle className="text-2xl text-center">
//               Create Account
//             </CardTitle>
//             <CardDescription className="text-center">
//               Sign up with your Google account to get started
//             </CardDescription>
//           </CardHeader>
//           <CardContent>
//             {error && (
//               <Alert variant="destructive" className="mb-4">
//                 <AlertCircle className="h-4 w-4" />
//                 <AlertDescription>{error}</AlertDescription>
//               </Alert>
//             )}
//             <Button
//               type="button"
//               variant="outline"
//               size="lg"
//               className="w-full h-12 text-base"
//               onClick={handleGoogleSignIn}
//               disabled={loading}
//             >
//               <Chrome className="mr-2 h-5 w-5" />
//               {loading ? "Creating account..." : "Sign up with Google"}
//             </Button>
//           </CardContent>
//         </Card>
//         <div className="text-center text-sm">
//           Already have an account?{" "}
//           <Link
//             to="/login"
//             className="font-medium text-primary hover:underline"
//           >
//             Sign in
//           </Link>
//         </div>
//       </div>
//     </div>
//   );
// }
