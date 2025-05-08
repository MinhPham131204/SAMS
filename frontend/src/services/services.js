const BASE_API_URL = "https://sams.akng.io.vn";

const Services = {
  // Lấy dữ liệu môi trường trong khoảng thời gian
  getEnviromentData: async (range_minute) => {
    return await fetch(`${BASE_API_URL}/getData/?range_minute=${range_minute}`, { method: "GET" });
  },

  // Lấy thông tin chung về tưới tiêu và thông gió
  getGeneralInfo: async () => {
    return await fetch(`${BASE_API_URL}/smart/general/`, { method: "GET" });
  },

  // Cập nhật chế độ (Thủ công / Tự động) của tưới tiêu hoặc thông gió
  updateMode: async (type, mode) => {
    return await fetch(`${BASE_API_URL}/smart/mode/`, {
      method: "PUT",
      redirect: "follow",
      body: JSON.stringify({ type, mode }),
    });
  },

  // Bật / Tắt thiết bị tưới tiêu hoặc thông gió (chỉ hoạt động khi ở chế độ Thủ công)
  updateDeviceState: async (type, state) => {
    return await fetch(`${BASE_API_URL}/smart/state/`, {
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
    return await fetch(`${BASE_API_URL}/smart/threshold/`, {
      method: "PUT",
      redirect: "follow",
      body: JSON.stringify({ sensorID, temp, hum, lig, soil }),
    });
  },
  // getGeneralInfo: async () => {
  //   return new Promise((resolve) => {
  //     setTimeout(() => {
  //       resolve({
  //         ok: true,
  //         status: 200,
  //         json: async () => mockData,
  //       });
  //     }, 500); // Giả lập độ trễ 500ms
  //   });
  // },

  // updateMode: async (type, mode) => {
  //   return new Promise((resolve) => {
  //     setTimeout(() => {
  //       mockData.data[type].mode = mode; // Cập nhật mode trong mock data
  //       resolve({ ok: true, status: 200, json: async () => ({ success: true, data: null }) });
  //     }, 300);
  //   });
  // },

  // updateDeviceState: async (type, state) => {
  //   return new Promise((resolve) => {
  //     setTimeout(() => {
  //       if (mockData.data[type].mode === 1) {
  //         resolve({
  //           ok: false,
  //           status: 400,
  //           json: async () => ({ success: false, error: "Bạn đang ở chế độ tự động, không thể thực hiện hành động này." }),
  //         });
  //       } else {
  //         mockData.data[type].device_state = state;
  //         resolve({ ok: true, status: 200, json: async () => ({ success: true, data: null }) });
  //       }
  //     }, 300);
  //   });
  // },

  // updateThreshold: async (type, threshold) => {
  //   return new Promise((resolve) => {
  //     setTimeout(() => {
  //       mockData.data[type].auto_threshold = threshold;
  //       resolve({ ok: true, status: 200, json: async () => ({ success: true, data: null }) });
  //     }, 300);
  //   });
  // },
  // Thêm sự kiện tưới nước
  addIrrigationEvent: async (eventData) => {
    return await fetch(`${BASE_API_URL}/irrigate-schedule/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(eventData),
    });
  },

  // Thêm sự kiện thông gió
  addVentilationEvent: async (eventData) => {
    return await fetch(`${BASE_API_URL}/ventilate-schedule/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(eventData),
    });
  },

};

export default Services;
