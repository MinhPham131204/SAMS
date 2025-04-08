import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  temperatureThreshold: 30,
  humidityThreshold: 60,
  soilMoistureThreshold: 40,
  lightIntensityThreshold: 5000,
};

// Tạo slice
const settingsSlice = createSlice({
  name: "settings",
  initialState,
  reducers: {
    updateSettings: (state, action) => {
      state[action.payload.name] = action.payload.value;
    }
  },
});

// Xuất actions và reducer
export const { updateSettings } = settingsSlice.actions;
export default settingsSlice.reducer;
