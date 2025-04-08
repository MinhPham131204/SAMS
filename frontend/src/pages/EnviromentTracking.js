import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";
import { toast } from "react-toastify";
import { ThermometerSun, Droplets, Sun } from "lucide-react";
import Services from "../services/services";
const timeRanges = [
  { label: "1 phút", value: 1 },
  { label: "5 phút", value: 5 },
  { label: "15 phút", value: 15 },
  { label: "1 giờ", value: 60 },
  { label: "3 giờ", value: 180 },
  { label: "6 giờ", value: 360 },
  { label: "12 giờ", value: 720 },
  { label: "24 giờ", value: 1440 },
];

export default function EnviromentTracking() {
  const [data, setData] = useState([]);
  const [rangeMinute, setRangeMinute] = useState(1);

  useEffect(() => {
    const update_enviroment_data = async () => {
      const res = await Services.getEnviromentData(rangeMinute);
      if (res.status === 200) {
        const data = await res.json();
        const formattedData = data.data.map((item) => ({
          ...item,
          timestamp: item.timestamp.split(" ")[1], // Lấy phần giờ phút giây
        }));
        setData(formattedData.reverse());
      } else {
        toast.error("Lấy dữ liệu thất bại");
        console.log(res);
      }
    };
  
    update_enviroment_data(); // Gọi ngay lập tức khi rangeMinute thay đổi
  
    const interval = setInterval(update_enviroment_data, 3000);
  
    return () => clearInterval(interval); // Xóa interval cũ khi rangeMinute thay đổi
  }, [rangeMinute]); // 🔥 Thêm rangeMinute vào đây để cập nhật khi thay đổi



  const Chart = ({ title, data, dataKey, unit, lineColor, icon }) => (
    <div className="bg-white shadow-lg rounded-lg p-4">
      <div className="text-2xl flex items-center justify-start ml-8">
        {icon}
        <h3 className="text-center text-lg font-semibold text-gray-600 ml-2">{title}</h3>
        <p className=" ml-3 text-lg font-semibold">{data.length > 0 ? data.at(-1)[dataKey] : ""} {unit}</p>
      </div>

      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey={dataKey} stroke={lineColor} strokeWidth={2} isAnimationActive={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Theo dõi môi trường</h1>
      {/* Dropdown chọn khoảng thời gian */}
      <div className="mb-4 flex justify-center items-center">
        <p className="text-xl font-semibold text-gray">Xem dữ liệu qua </p>
        <select
          className="ml-3 px-4 py-2 border rounded-lg shadow-md focus:ring focus:ring-blue-300"
          value={rangeMinute}
          onChange={(e) => setRangeMinute(Number(e.target.value))}
        >
          {timeRanges.map((range) => (
            <option key={range.value} value={range.value}>
              {range.label}
            </option>
          ))}
        </select>
      </div>
      <div className="grid grid-cols-1 gap-6 p-4 md:grid-cols-2 mt-6">
        <Chart title="Nhiệt độ" unit="°C" icon={<ThermometerSun />} data={data} dataKey="temperature" stroke="text-red-500" lineColor="#FF5733" />
        <Chart title="Độ ẩm không khí" unit="%" icon={<Droplets />} data={data} dataKey="humidity" stroke="text-blue-500" lineColor="#1E90FF" />
        <Chart title="Cường độ ánh sáng" unit="lux" icon={<Sun />} data={data} dataKey="light" stroke="text-yellow-500" lineColor="#FFC107" />
        <Chart title="Độ ẩm đất" unit="%" icon={<Droplets />} data={data} dataKey="soil" stroke="text-green-500" lineColor="#28A745" />
      </div>
    </div>
  );
}