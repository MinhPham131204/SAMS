import React from "react";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import farmImage from "./image/farm.png";
import {Home} from 'lucide-react'

export default function HomePage() {
  const auth = useSelector((state) => state.auth);
  const navigate = useNavigate(); // Khởi tạo useNavigate

  const handleLogin = () => {
    navigate("/login"); // Điều hướng đến trang login
  };

  const handleStart = () => {
    if (auth.isAuthenticated) {
      navigate("/enviroment"); // Điều hướng đến trang ControlPanel
    } else {
      navigate("/login"); // Điều hướng đến trang login nếu chưa đăng nhập
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col relative z-0">
      {/* Header */}
      <div className="flex justify-between items-center px-6 py-4 border-b border-green-200">
        <div className="text-2xl font-bold text-green-700 flex items-center gap-2">
          SAMS - SMART AGRICULTURAL MONITORING SYSTEM
        </div>

        {/* Avatar or Login Button */}
        {auth.isAuthenticated ? (
          <Home className="text-3xl text-green-800" />
        ) : (
          <button
            className="bg-green-200 text-green-900 px-4 py-2 rounded-full hover:bg-green-300"
            onClick={handleLogin}
          >
            Đăng nhập
          </button>
        )}
      </div>

      {/* Banner Section */}
      <div
        className="flex flex-1 flex-col lg:flex-row items-center justify-between px-8 py-12 bg-green-50 bg-cover bg-center relative"
        style={{
          backgroundImage: `url(${farmImage})`,
        }}
      >
        {/* Overlay */}
        <div className="absolute inset-0 bg-black opacity-40 z-0"></div>

        {/* Left content */}
        <div className="max-w-2xl z-10 text-white relative">
          <h1 className="text-3xl font-bold drop-shadow">
            Trường Đại học Bách Khoa - ĐHQG TPHCM
            <br />
            Hệ thống chăm sóc cây thông minh
          </h1>

          <p className="text-lg mt-6 font-medium drop-shadow">
            Nơi bạn có thể chăm cây một cách dễ dàng hơn với:
          </p>
          <ul className="list-disc ml-6 mt-2 text-sm drop-shadow">
            <li>Giám sát độ ẩm, ánh sáng, nhiệt độ</li>
            <li>Tưới tiêu tự động</li>
            <li>Phân tích sâu bệnh bằng AI</li>
          </ul>

          <button
            onClick={handleStart} // Gọi handleStart khi nhấn "Bắt đầu ngay!"
            className="mt-8 px-6 py-3 bg-white text-green-800 font-semibold rounded-full text-lg hover:bg-green-100 transition shadow-md z-10 relative"
          >
            Bắt đầu ngay!
          </button>
        </div>
      </div>
    </div>
  );
}
