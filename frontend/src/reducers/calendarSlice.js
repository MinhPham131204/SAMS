import { createSlice, miniSerializeError } from "@reduxjs/toolkit";

const initialState = {
  currentDate: new Date(),
  selectedDate: null,
  events: [],
};

const calendarSlice = createSlice({
  name: "calendar",
  initialState,
  reducers: {
    setCurrentDate: (state, action) => {
      state.currentDate = action.payload;
    },
    setSelectedDate: (state, action) => {
      state.selectedDate = action.payload;
    },
    addEvent: (state, action) => {
      const {date, hour, minute, name, action_type} = action.payload;
      const id = Date.now().toString();
      state.events.push({
        id: id,
        date,
        hour,
        minute,
        name,
        action_type,
        status: 0,
      });
    },
    deleteEvent: (state, action) => {
      state.events = state.events.filter((item) => item.id !== action.payload.id);
    },
  },
});

export const { setCurrentDate, setSelectedDate, addEvent, deleteEvent } = calendarSlice.actions;
export default calendarSlice.reducer;
