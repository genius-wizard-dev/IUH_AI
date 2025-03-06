import { Toaster } from "@/components/ui/toaster";
import {
  Navigate,
  Route,
  BrowserRouter as Router,
  Routes,
} from "react-router-dom";
import { PrivateRoute } from "./components/PrivateRoute";
// import About from "./page/About";
import Chat from "./page/Chat";
import Login from "./page/Login";
// import Register from "./page/Register";
import { AuthProvider } from "./utils/context";

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          {/* <Route path="/register" element={<Register />} /> */}
          <Route
            path="/chat"
            element={
              <PrivateRoute>
                <Chat />
              </PrivateRoute>
            }
          />
          {/* <Route path="/about" element={<About />} /> */}
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
        <Toaster />
      </AuthProvider>
    </Router>
  );
}

export default App;
