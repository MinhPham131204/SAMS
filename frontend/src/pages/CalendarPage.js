import { useDispatch, useSelector } from "react-redux";
import { setCurrentDate, setSelectedDate, addEvent, deleteEvent } from "../reducers/calendarSlice";
import { useState } from "react";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Services from "../services/services"
export default function CalendarPage() {
  const dispatch = useDispatch();
  const { currentDate, selectedDate, events } = useSelector((state) => state.calendar);
  const daysInMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();
  const firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay();

  const [eventTime, setEventTime] = useState("");
  const [eventType, setEventType] = useState("irrigation");

  const toDateString = new Date().toDateString();

  const handlePrevMonth = () => {
    dispatch(setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1)));
  };

  const handleNextMonth = () => {
    dispatch(setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1)));
  };

  const handleDateClick = (day) => {
    const dateKey = new Date(currentDate.getFullYear(), currentDate.getMonth(), day).toDateString();
    dispatch(setSelectedDate(dateKey));
  };

  const handleAddEvent = () => {
    if (!eventTime.trim() || !selectedDate) {
      toast.error("Vui lòng nhập đầy đủ thông tin!");
      return;
    }

    const [hour, minute] = eventTime.split(":").map(Number);
    const eventDateTime = new Date(`${selectedDate} ${hour+7}:${minute}:00`) //GMT +7

    dispatch(
      addEvent({
        date: selectedDate,
        hour,
        minute,
        action_type: eventType,
      })
    );
    console.log("test")
    console.log(eventTime);

    let bodyData;

    if (eventType === "irrigation") {
      // Body cho irrigation
      bodyData = {
        irrigatedTime: eventDateTime, // Gửi thời gian theo định dạng YYYY-MM-DD HH:MM:SS
        sensorID: 1, // SensorID mặc định là 1
         // Thêm thông tin cho irrigation nếu cần
      };
      Services.addIrrigationEvent(bodyData)
        .then(response => {
          console.log(response);
          if (response.ok) {
            toast.success("Sự kiện đã được thêm thành công!");
          } else {
            toast.error("Lỗi khi thêm sự kiện!");
          }
        })
        .catch(error => {
          console.error("Có lỗi xảy ra khi gọi API:", error);
        });
      setEventTime("");
      setEventType("irrigation")
    } else if (eventType === "ventilation") {
      // Body cho ventilation
      bodyData = {
        ventilatedTime: eventDateTime, // Gửi thời gian theo định dạng YYYY-MM-DD HH:MM:SS
        sensorID: 1, // SensorID mặc định là 1
         // Thêm thông tin cho ventilation nếu cần
      };
      Services.addVentilationEvent(bodyData)
        .then(response => {
          if (response.ok) {
            toast.success("Sự kiện đã được thêm thành công!");
          } else {
            toast.error("Lỗi khi thêm sự kiện!");
          }
        })
        .catch(error => {
          console.error("Có lỗi xảy ra khi gọi API:", error);
        });
        setEventTime("");
        setEventType("irrigation")
    }


  };

  const handleDeleteEvent = (id) => {
    dispatch(deleteEvent({ id: id }));
    toast.info("Sự kiện đã bị xoá!");
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow-lg rounded-lg">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6">Lịch & Lên lịch</h2>
      </div>

      {/* Điều hướng tháng */}
      <div className="flex justify-between items-center mb-4">
        <button onClick={handlePrevMonth} className="px-3 py-1 bg-gray-300 rounded">← Tháng trước</button>
        <h3 className="text-lg font-semibold">
          {currentDate.toLocaleString("default", { month: "long", year: "numeric" })}
        </h3>
        <button onClick={handleNextMonth} className="px-3 py-1 bg-gray-300 rounded">Tháng sau →</button>
      </div>

      {/* Lịch dạng bảng */}
      <div className="grid grid-cols-7 gap-2 text-center font-medium">
        {["CN", "T2", "T3", "T4", "T5", "T6", "T7"].map((day) => (
          <div key={day} className="p-2 bg-gray-200 rounded">{day}</div>
        ))}
        {Array(firstDayOfMonth).fill(null).map((_, index) => (
          <div key={index}></div>
        ))}
        {Array.from({ length: daysInMonth }, (_, index) => {
          const day = index + 1;
          const dateKey = new Date(currentDate.getFullYear(), currentDate.getMonth(), day).toDateString();
          const eventCount = events.filter(item => item.date == dateKey).length;
          return (
            <div
              key={day}
              onClick={() => handleDateClick(day)}
              className={`h-16 p-2 border rounded cursor-pointer 
                ${selectedDate === dateKey && toDateString === dateKey ? "bg-cyan-700 text-white"
                  : selectedDate === dateKey ? "bg-blue-500 text-white"
                    : toDateString === dateKey ? "bg-green-500 text-white"
                      : "hover:bg-gray-300"}`}
            >
              {day}
              {eventCount > 0 && <p className="text-xs">({eventCount} events)</p>}
            </div>
          );
        })}
      </div>

      {/* Thêm sự kiện */}
      {selectedDate && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold">Lên lịch cho: {selectedDate}</h3>
          <input
            type="time"
            value={eventTime}
            onChange={(e) => setEventTime(e.target.value)}
            className="border p-2 rounded w-full mt-2"
          />
          <select
            value={eventType}
            onChange={(e) => setEventType(e.target.value)}
            className="border p-2 rounded w-full mt-2"
          >
            <option value="irrigation">💧 Tưới nước</option>
            <option value="ventilation">🌬️ Thông gió</option>
          </select>
          <button
            onClick={handleAddEvent}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 mt-2"
          >
            Thêm sự kiện
          </button>
          <ul className="mt-4">
            {events
              .filter(event => event.date === selectedDate)
              .map((event, index) => (
                <li key={index} className="flex justify-between bg-gray-200 p-2 rounded mt-1">
                  <span>{event.date} - {event.hour}:{event.minute} - {event.action_type} {`--> ${event.status == 0 ? "waiting" : event.status == 1 ? "completed" : "fail"}`}</span>
                  <button
                    onClick={() => handleDeleteEvent(event.id)}
                    className="text-red-500 font-bold"
                  >
                    X
                  </button>
                </li>
              ))}
          </ul>
        </div>
      )}
    </div>
  );
}
