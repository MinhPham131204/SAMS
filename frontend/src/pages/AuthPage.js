import { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { loginSuccess } from "../reducers/authSlice";
import { fakeData } from "../data";

const AuthPage = () => {
  const [isSignup, setIsSignup] = useState(false);
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const navigate = useNavigate();
  const dispatch = useDispatch()

  const handleLogin = () => {
    if (username !== fakeData.login.username || password !== fakeData.login.password) {
      toast.error("Email hoặc mật khẩu không đúng!");
      return;
    }
    else {
      dispatch(loginSuccess({
        username: username,
        password: password,
      }))
      navigate("/")
      toast.success("Đăng nhập thành công!");
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h2 className="text-2xl font-semibold text-center mb-4">
          {isSignup ? "Đăng ký" : "Đăng nhập"}
        </h2>

        <div className="space-y-4">
          {isSignup &&
            <input
              type="email"
              placeholder="Email"
              className="w-full p-2 border rounded"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          }
          <input
            type="username"
            placeholder="Tên đăng nhập"
            className="w-full p-2 border rounded"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            type="password"
            placeholder="Mật khẩu"
            className="w-full p-2 border rounded"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleLogin()}
          />
          {isSignup &&
            <input
              type="password"
              placeholder="Nhập lại mật khẩu"
              className="w-full p-2 border rounded"
              value={passwordConfirm}
              onChange={(e) => setPasswordConfirm(e.target.value)}
            />
          }
          <button onClick={handleLogin} className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">
            {isSignup ? "Đăng ký" : "Đăng nhập"}
          </button>
        </div>

        <p className="text-center mt-4">
          {isSignup ? "Đã có tài khoản?" : "Chưa có tài khoản?"}{" "}
          <button
            className="text-blue-500 underline"
            onClick={() => setIsSignup(!isSignup)}
          >
            {isSignup ? "Đăng nhập" : "Đăng ký ngay"}
          </button>
        </p>
      </div>
    </div>
  );
};

export default AuthPage;
