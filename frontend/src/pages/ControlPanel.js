import React, { useEffect, useState } from "react";
import Services from "../services/services";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const ControlPanel = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
 
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await Services.getGeneralInfo();
      if (res.ok) {
        const result = await res.json();
     
        if (result.success) {
        
          setData(result.data);
       
         
        } else {
          toast.error("Lỗi khi lấy dữ liệu");
        }
      } else {
        toast.error(`Lỗi server: ${res.status}`);
      }
    } catch (error) {
      toast.error("Lỗi kết nối");
    }
    setLoading(false);
  };

  const handleModeChange = async (type) => {
    const newMode = data[type].mode === 0 ? 1 : 0;
    try {
      const res = await Services.updateMode(type, newMode);
      if (res.ok) {
        toast.success("Cập nhật chế độ thành công!");
        setData((prev) => ({ ...prev, [type]: { ...prev[type], mode: newMode } }));
      } else {
        const errorData = await res.json();
        toast.error(errorData.error || `Lỗi server: ${res.status}`);
      }
    } catch (error) {
      toast.error("Lỗi kết nối");
    }
  };

  const handleToggleDevice = async (type) => {

    const newstate = data[type].device_state === false ? true : false;
    console.log(data[type].device_state)
    console.log(newstate)
    try {
      const res = await Services.updateDeviceState(type, newstate);
 
      if (res.ok) {
        toast.success("Cập nhật trạng thái thành công!");
        setData((prev) => ({ ...prev, [type]: { ...prev[type], device_state: newstate } }));
        
      } else {
        const errorData = await res.json();
        toast.error(errorData.error || `Lỗi server: ${res.status}`);
      }
    } catch (error) {
      toast.error("Lỗi kết nối");
    }
  };

  const handleThresholdUpdate = async (type, threshold) => {
    try {
      const res = await Services.updateThreshold(type, threshold);
      if (res.ok) {
        toast.success("Cập nhật ngưỡng thành công!");
        setData((prev) => ({ ...prev, [type]: { ...prev[type], auto_threshold: threshold } }));
      } else {
        toast.error("Lỗi cập nhật ngưỡng");
      }
    } catch (error) {
      toast.error("Lỗi kết nối");
    }
  };

  if (loading) return <p className="text-center text-gray-500">Đang tải dữ liệu...</p>;
 
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
      <ControlColumn
        title="Tưới tiêu"
        type="irrigation"
        data={data.irrigation}
        onModeChange={handleModeChange}
        onToggleDevice={handleToggleDevice}
        onThresholdUpdate={handleThresholdUpdate}
      />
      <ControlColumn
        title="Thông gió"
        type="ventilation"
        data={data.ventilation}
        onModeChange={handleModeChange}
        onToggleDevice={handleToggleDevice}
        onThresholdUpdate={handleThresholdUpdate}
      />
    </div>
  );
};

const ControlColumn = ({ title, type, data, onModeChange, onToggleDevice, onThresholdUpdate }) => {
  const [threshold, setThreshold] = useState(data.auto_threshold);

  useEffect(() => {
    setThreshold(data.auto_threshold);
  }, [data.auto_threshold]);

  return (
    <div className="p-6 bg-white shadow-md rounded-lg">
      <h2 className="text-lg font-semibold mb-4">{title}</h2>

      {/* Nút Toggle Chế Độ */}
      {/* <div className="flex items-center justify-between mb-4">
        <span className="text-gray-700">Chế độ</span>
        <div className="flex justify-end items-center gap-5">
          <span className={`text-gray-700 ${data.mode === 0 && 'font-bold'}`}>Thủ công</span>
          <button
            onClick={() => onModeChange(type)}
            className={`w-16 h-8 rounded-full transition-colors ${data.mode === 1 ? "bg-green-500" : "bg-gray-300"
              } relative`}
          >
            <span
              className={`absolute left-1 top-1 w-6 h-6 bg-white rounded-full shadow-md transform transition-transform ${data.mode === 1 ? "translate-x-8" : ""
                }`}
            ></span>
          </button>
          <span className={`text-gray-700 ${data.mode === 1 && 'font-bold'}`}>Tự động</span>
        </div>
      </div> */}

     {/* Hiển thị trạng thái thiết bị (Luôn hiện, không chỉnh sửa nếu Auto) */}
      <div className="flex items-center justify-between">
        <span className="text-gray-700">Trạng thái thiết bị</span>
        <div className="flex justify-end items-center gap-5">
          <span className={`text-gray-700 ${!data.device_state && 'font-bold'}`}>Off</span>
          
          <button
            onClick={() => {
              if (data.mode === 0) {
                onToggleDevice(type);
              } else {
                toast.warn("Đang ở chế độ tự động, không thể thay đổi trạng thái!");
              }
            }}
            disabled={data.mode === 1}
            className={`w-16 h-8 rounded-full transition-colors 
              ${data.device_state ? "bg-green-500" : "bg-gray-300"} 
              relative 
              ${data.mode === 1 && "opacity-50 cursor-not-allowed"}`}
          >
            <span
              className={`absolute left-1 top-1 w-6 h-6 bg-white rounded-full shadow-md transform transition-transform 
                ${data.device_state ? "translate-x-8" : ""}`}
            ></span>
          </button>
          
          <span className={`text-gray-700 ${data.device_state && 'font-bold'}`}>On</span>
        </div>
      </div>


      {/* Cài đặt Threshold (Chỉ hiện nếu chế độ là Tự động) */}
      {data.mode === 1 && (
        <div className="mt-4">
          <h3 className="text-md font-semibold mb-2">Cài đặt Threshold</h3>
          {Object.keys(threshold).map((key) => (
            <div key={key} className="flex justify-between items-center mb-2">
              <span className="capitalize">{key}</span>
              <div className="flex space-x-2">
                <input
                  type="number"
                  className="w-16 p-1 border rounded-md"
                  value={threshold[key].min}
                  onChange={(e) =>
                    setThreshold({ ...threshold, [key]: { ...threshold[key], min: Number(e.target.value) } })
                  }
                />
                <span>-</span>
                <input
                  type="number"
                  className="w-16 p-1 border rounded-md"
                  value={threshold[key].max}
                  onChange={(e) =>
                    setThreshold({ ...threshold, [key]: { ...threshold[key], max: Number(e.target.value) } })
                  }
                />
              </div>
            </div>
          ))}
          <button
            onClick={() => onThresholdUpdate(type, threshold)}
            className="mt-3 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
          >
            Lưu chỉnh sửa
          </button>
        </div>
      )}
    </div>
  );
};


export default ControlPanel;
