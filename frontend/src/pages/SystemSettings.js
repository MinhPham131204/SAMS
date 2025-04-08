import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { toast } from "react-toastify";
import { updateSettings } from "../reducers/settingsSlice";

const SystemSettings = () => {
  const [selectedTab, setSelectedTab] = useState("temperature");
  const dispatch = useDispatch();

  // State lưu cài đặt hệ thống
  const {
    temperatureThreshold,
    humidityThreshold,
    soilMoistureThreshold,
    lightIntensityThreshold,
  } = useSelector((state) => state.settings);

  // Xử lý thay đổi input
  const handleChange = (e) => {
    const { name, value } = e.target;
    dispatch(updateSettings({
      name: name,
      value: value
    }))
  };
  // Xử lý thay đổi input
  const handleUpdate = (e) => {
    toast.success("Cập nhật thành công")
  };


  return (
    <div className="flex-1 h-full p-6">
      <h1 className="text-2xl font-bold">Cài đặt hệ thống</h1>
      <div className="mt-6">
        <h3 className="mt-6 text-xl font-base mb-4">Ngưỡng nhiệt độ cảnh báo (độ C)</h3>
        <input
          type="number"
          name="temperatureThreshold"
          value={temperatureThreshold}
          onChange={handleChange}
          className="w-full p-2 border rounded-md"
        />
        <h3 className="mt-6 text-xl font-base mb-4">Ngưỡng độ ẩm không khí cảnh báo (%)</h3>
        <input
          type="number"
          name="humidityThreshold"
          value={humidityThreshold}
          onChange={handleChange}
          className="w-full p-2 border rounded-md"
        />
        <h3 className="mt-6 text-xl font-base mb-4">Ngưỡng độ ẩm đất cảnh báo (%)</h3>
        <input
          type="number"
          name="soilMoistureThreshold"
          value={soilMoistureThreshold}
          onChange={handleChange}
          className="w-full p-2 border rounded-md"
        />
        <h3 className="mt-6 text-xl font-base mb-4">Cường độ ánh sáng cảnh báo (lux)</h3>
        <input
          type="number"
          name="lightIntensityThreshold"
          value={lightIntensityThreshold}
          onChange={handleChange}
          className="w-full p-2 border rounded-md"
        />
        <button
          name="temperature"
          onClick={handleUpdate}
          className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          Cập nhật
        </button>
      </div>
    </div>
  );
};

export default SystemSettings;
