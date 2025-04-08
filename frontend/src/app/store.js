import { applyMiddleware } from "redux";
import { configureStore } from "@reduxjs/toolkit";
import { thunk } from "redux-thunk";
import authReducer from "../reducers/authSlice";
import settingsReducer from "../reducers/settingsSlice";
import calendarReducer from "../reducers/calendarSlice";
const middleware = [thunk];

export const store = configureStore(
  {
    reducer: {
      auth: authReducer,
      settings: settingsReducer,
      calendar: calendarReducer,
    },
  },
  applyMiddleware(...middleware)
);
