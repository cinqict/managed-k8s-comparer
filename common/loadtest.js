import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    vus: 10, // number of virtual users
    duration: '30s', // total test duration
};

export default function () {
    // Health check
    let res = http.get('http://37.59.218.5/health');
    check(res, { 'health is 200': (r) => r.status === 200 }) || console.error('Health failed:', res.status, res.body);

    // Write endpoint
    res = http.post('http://37.59.218.5/write', JSON.stringify({ content: 'Hello from k6!' }), {
        headers: { 'Content-Type': 'application/json' },
    });
    check(res, { 'write is 200': (r) => r.status === 200 }) || console.error('Write failed:', res.status, res.body);

    // Read endpoint
    res = http.get('http://37.59.218.5/read');
    check(res, { 'read is 200': (r) => r.status === 200 }) || console.error('Read failed:', res.status, res.body);

    sleep(1);
}