import { expose } from './comlink-4.3.1.js';

expose({
    run(code, errorHandler) {
        try {
            return eval(code);
        } catch (error) {
            errorHandler(error);
        }
    }
});
