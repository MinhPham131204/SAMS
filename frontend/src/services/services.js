const BASE_API_URL = process.env.REACT_APP_API_ENDPOINT;

const Services = {



  // Lấy dữ liệu môi trường trong khoảng thời gian
  getEnviromentData: async (range_minute) => {
    return await fetch(`${BASE_API_URL}/enviroment/get?range_minute=${range_minute}`, { method: "GET" });
  },



  // Lấy thông tin chung về tưới tiêu và thông gió
  getGeneralInfo: async () => {
    return await fetch(`${BASE_API_URL}/control/get`, { method: "GET" });
  },

  // Cập nhật chế độ (Thủ công / Tự động) của tưới tiêu hoặc thông gió
  updateMode: async (type, mode) => {
    return await fetch(`${BASE_API_URL}/control/mode/update`, {
      method: "PUT",
      redirect: "follow",
      body: JSON.stringify({ type, mode }),
    });
  },

  // Bật / Tắt thiết bị tưới tiêu hoặc thông gió (chỉ hoạt động khi ở chế độ Thủ công)
  updateDeviceState: async (type, state) => {
    return await fetch(`${BASE_API_URL}/control/device_state/update`, {
      method: "PUT",
      redirect: "follow",
      body: JSON.stringify({ type, state }),
    });
  },

  // Cập nhật ngưỡng tự động (threshold)
  updateThreshold: async (type, threshold) => {
    const sensorID = 1;
    const temp = threshold["temp"];
    const hum = threshold["hum"];
    const lig = threshold["lig"];
    const soil = threshold["soil"];
    return await fetch(`${BASE_API_URL}/control/threshold/update`, {
      method: "PUT",
      redirect: "follow",
      body: JSON.stringify({ sensorID, temp, hum, lig, soil }),
    });
  },


  // Thêm sự kiện tưới nước
  addIrrigationEvent: async (eventData) => {
    return await fetch(`${BASE_API_URL}/irrigate-schedule`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(eventData),
    });
  },

  // Thêm sự kiện thông gió
  addVentilationEvent: async (eventData) => {
    return await fetch(`${BASE_API_URL}/ventilate-schedule`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(eventData),
    });
  },

  // Dự đoán bệnh lá lúa
  predictRiceLeafDisease: async (image) => {
    return await fetch(`${BASE_API_URL}/disease/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "image/jpeg",
      },
      body: image,
    });
  },
};

export default Services;
