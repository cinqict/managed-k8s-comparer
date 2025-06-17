import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.DUMMY_APP_IP ? `http://${__ENV.DUMMY_APP_IP}` : 'http://localhost:8080';

export let options = {
    vus: 10, // number of virtual users
    duration: '30s', // total test duration
};

export default function () {
    // Health check
    let res = http.get(`${BASE_URL}/health`);
    check(res, { 'health is 200': (r) => r.status === 200 }) || console.error('Health failed:', res.status, res.body);

    // Write endpoint
    res = http.post(`${BASE_URL}/write`, JSON.stringify({ content: 'Hello from k6!' }), {
        headers: { 'Content-Type': 'application/json' },
    });
    check(res, { 'write is 200': (r) => r.status === 200 }) || console.error('Write failed:', res.status, res.body);

    // Read endpoint
    res = http.get(`${BASE_URL}/read`);
    check(res, { 'read is 200': (r) => r.status === 200 }) || console.error('Read failed:', res.status, res.body);

    sleep(1);
}