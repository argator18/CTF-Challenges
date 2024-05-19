import {
    wrap,
    proxy
} from './comlink-4.3.1.js';

report.onclick = () => {
    location.pathname = '/report'
};

const sandbox = new class {
    box = wrap(new Worker('sandbox.js', {
        type: 'module'
    }));
    run(code) {
        return new Promise(async (resolve, reject) => {
            const errorHandler = proxy(reject);
            const result = await this.box.run(code, errorHandler);
            resolve(result);
        });
    }
}();

const query = new URLSearchParams(location.search);
var codeWithCustomToString = "7*7"
const code = query.get('code') ? ? codeWithCustomToString;
console.log(code)
var tmp = await sandbox.run(code);
console.log(tmp)
output.textContent = tmp