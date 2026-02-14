import {configs} from "@eslint/js";
import axios from "axios";

const baseURL = "http://localhost:8080";

export const http = axios.create({
    baseURL,
    timeout: 10000,
})

http.interceptors.request.use((config) => {
    const token = sessionStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

http.interceptors.response.use(
    (r) => r,
    (err) => {
        if (err?.response?.status === 401) {
            sessionStorage.removeItem("token");
            sessionStorage.removeItem("user_id");
            window.location.href = "/login";
        }
        return Promise.reject(err);
    }
);