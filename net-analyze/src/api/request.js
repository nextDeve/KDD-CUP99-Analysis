import axios from "axios";
import nprogress from "nprogress";
import "nprogress/nprogress.css";

const request = axios.create({
    baseURL: '/api',
    timeout: 5000,
})

//请求拦截器
request.interceptors.request.use((config) => {
    nprogress.start()
    return config;
})
request.interceptors.response.use((res) => {
    nprogress.done()
    return res;
}, (error) => {
    console.log(error)
    return Promise.reject(new Error('fail'));
})

export default request;