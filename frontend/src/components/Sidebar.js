import { DiscAlbum, LogOut } from "lucide-react";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { logout } from "../reducers/authSlice";


export default function Sidebar(props) {
  const [expanded, setExpanded] = useState(false);
  const { routes } = props;
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const authState = useSelector((state) => state.auth)

  const handleLogout = () => {
    toast.info(
      <div>
        <p>Bạn có chắc muốn đăng xuất khỏi thiết bị này ?</p>
        <div className="mt-2 flex gap-2">
          <button
            onClick={() => {
              toast.dismiss();
              dispatch(logout())
              navigate('/login')
            }}
            className="px-3 py-1 bg-blue-500 text-white rounded"
          >
            Đăng xuất
          </button>
          <button
            onClick={() => toast.dismiss()}
            className="px-3 py-1 bg-gray-500 text-white rounded"
          >
            Hủy
          </button>
        </div>
      </div>,
      { position: "top-center", autoClose: false, closeOnClick: false }
    );
  }

  return (
    <div
      className={`fixed z-10 top-0 left-0 h-full bg-gray-900 text-white p-2 ${expanded ? "w-64" : "w-16"}`}
      onMouseEnter={() => setExpanded(true)}
      onMouseLeave={() => setExpanded(false)}
    >
      <div className="flex flex-col gap-4 mt-4">
        {routes.map((item, index) => (
          <Link
            key={index}
            to={item.path}
            className="flex items-center gap-3 p-3 hover:bg-gray-700 rounded-md"
          >
            {item.icon}
            {expanded && <span>{item.name}</span>}
          </Link>
        ))}

        {authState.isAuthenticated && <button
          onClick={handleLogout}
          className="flex items-center gap-3 p-3 hover:bg-gray-700 rounded-md"
        >
          <LogOut />
          {expanded && <span>Đăng xuất</span>}
        </button>}
      </div>

    </div>
  );
}
