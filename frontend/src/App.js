import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import { ThermometerSun, CalendarDays, Droplets, Settings, Home } from "lucide-react";
import EnviromentTracking from "./pages/EnviromentTracking";
import ControlPanel from "./pages/ControlPanel";
import ProtectedRoute from "./components/ProtectedRoute";
import AuthPage from "./pages/AuthPage";
import HomePage from "./pages/HomePage";
import { store } from './app/store';
import { Provider } from 'react-redux';
import { ToastContainer } from 'react-toastify';
import SystemSettings from "./pages/SystemSettings";
import CalendarPage from "./pages/CalendarPage";


const routes = [
  {
    name: "Trang chủ",
    icon : <Home />,
    path: "/",
    page: <HomePage/> // Không cần bảo vệ cho trang này
  },
  {
    name: "Theo dõi môi trường",
    icon: <ThermometerSun />,
    path: "/enviroment",
    page: <EnviromentTracking />
  },
  {
    name: "Tưới tiêu - Thông gió",
    icon: <Droplets />,
    path: "/control-pannel",
    page: <ControlPanel/>
  },
  {
     name: "Lên lịch và nhắc nhở",
     icon: <CalendarDays />,
     path: "/scheduler",
     page: <CalendarPage/>
   },
   {
   name: "Cài đặt hệ thống",
    icon: <Settings />,
    path: "/system",
   page: <SystemSettings/>
  }
];

export default function App() {
  return (
    <Provider store={store}>
      <Router>
        <div className="relative flex">
          <Sidebar routes={routes} />
          <div className="p-6 flex-1 ml-16"> 
            <Routes>
              <Route path="/login" element={<AuthPage />} />
              {/* HomePage không cần bảo vệ */}
              <Route path="/" element={<HomePage />} />  
              <Route element={<ProtectedRoute />}>
                {routes.slice(1).map((route) => {
                  return <Route key={route.name} path={route.path} element={route.page} />
                })}
              </Route>
            </Routes>
          </div>
        </div>
      </Router>
      <ToastContainer
        position="top-center"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
      />
    </Provider>
  );
}
