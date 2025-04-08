import { useSelector } from "react-redux";
import { Outlet, Navigate } from "react-router-dom";
import 'react-toastify'
import { toast } from "react-toastify";

const ProtectedRoute = () => {
  const authState = useSelector((state) => state.auth)

  if (authState.isAuthenticated){
    return <Outlet/>
  }
  else{
    toast.error("Bạn chưa đăng nhập")
    return <Navigate to="/login"/>
  }
};

export default ProtectedRoute;
