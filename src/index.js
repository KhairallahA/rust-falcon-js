const fs = require('fs');
const base64_arraybuffer_1 = require("base64-arraybuffer");

// Read the WASM file as a buffer
const wasmFile = fs.readFileSync('./module.wasm');
const wasmUtf = wasmFile.toString('utf8');
const wasmBase64 = (0, base64_arraybuffer_1.decode)(wasmUtf);

// console.log(Buffer.from(wasmBase64).toString('hex'));

let cachedUint8Memory0 = null;
let wasm = undefined;

// Initialize the WASM module
function init() {
    if (wasm !== undefined) return wasm;
    
    const imports = __wbg_get_imports();
    __wbg_init_memory(imports);
    
    const instance = new WebAssembly.Instance(new WebAssembly.Module(wasmBase64), imports);
    return __wbg_finalize_init(instance);
}

// Initialize the module
init();

// Heap management
const heap = new Array(128).fill(undefined);
heap.push(undefined, null, true, false);

function getObject(idx) {
    return heap[idx];
}

let heap_next = heap.length;

function dropObject(idx) {
    if (idx < 132) return;
    heap[idx] = heap_next;
    heap_next = idx;
}

function takeObject(idx) {
    const ret = getObject(idx);
    dropObject(idx);
    return ret;
}

function addHeapObject(obj) {
    if (heap_next === heap.length) heap.push(heap.length + 1);
    const idx = heap_next;
    heap_next = heap[idx];
    heap[idx] = obj;
    return idx;
}

// Text decoder setup
const cachedTextDecoder = typeof TextDecoder !== "undefined"
    ? new TextDecoder("utf-8", { ignoreBOM: true, fatal: true })
    : {
        decode: () => {
            throw Error("TextDecoder not available");
        },
    };

if (typeof TextDecoder !== "undefined") {
    cachedTextDecoder.decode();
}

// Memory management
function getUint8Memory0() {
    if (cachedUint8Memory0 === null || cachedUint8Memory0.byteLength === 0) {
        cachedUint8Memory0 = new Uint8Array(wasm.memory.buffer);
    }
    return cachedUint8Memory0;
}

function getStringFromWasm0(ptr, len) {
    ptr = ptr >>> 0;
    return cachedTextDecoder.decode(getUint8Memory0().subarray(ptr, ptr + len));
}

// Falcon keypair generation
function falconKeypair(_seed) {
    const ret = wasm.falconKeypair(addHeapObject(_seed));
    return KeyPair.__wrap(ret);
}

// KeyPair class
class KeyPair {
    static __wrap(ptr) {
        ptr = ptr >>> 0;
        const obj = Object.create(KeyPair.prototype);
        obj.__wbg_ptr = ptr;
        return obj;
    }

    __destroy_into_raw() {
        const ptr = this.__wbg_ptr;
        this.__wbg_ptr = 0;
        return ptr;
    }

    free() {
        const ptr = this.__destroy_into_raw();
        wasm.__wbg_keypair_free(ptr);
    }

    get public() {
        const ret = wasm.keypair_public(this.__wbg_ptr);
        return takeObject(ret);
    }

    get secret() {
        const ret = wasm.keypair_secret(this.__wbg_ptr);
        return takeObject(ret);
    }
}

// WebAssembly imports
function __wbg_get_imports() {
    const imports = {};
    imports.wbg = {};
    
    imports.wbg.__wbindgen_object_drop_ref = function(arg0) {
        takeObject(arg0);
    };
    
    imports.wbg.__wbindgen_object_clone_ref = function(arg0) {
        const ret = getObject(arg0);
        return addHeapObject(ret);
    };
    
    imports.wbg.__wbg_log_233cc96097d5ec7d = function(arg0, arg1) {
        console.log(getStringFromWasm0(arg0, arg1));
    };
    
    imports.wbg.__wbg_buffer_085ec1f694018c4f = function(arg0) {
        const ret = getObject(arg0).buffer;
        return addHeapObject(ret);
    };
    
    imports.wbg.__wbg_newwithbyteoffsetandlength_6da8e527659b86aa = function(arg0, arg1, arg2) {
        const ret = new Uint8Array(getObject(arg0), arg1 >>> 0, arg2 >>> 0);
        return addHeapObject(ret);
    };
    
    imports.wbg.__wbg_new_8125e318e6245eed = function(arg0) {
        const ret = new Uint8Array(getObject(arg0));
        return addHeapObject(ret);
    };
    
    imports.wbg.__wbg_newwithlength_e5d69174d6984cd7 = function(arg0) {
        const ret = new Uint8Array(arg0 >>> 0);
        return addHeapObject(ret);
    };
    
    imports.wbg.__wbg_length_72e2208bbc0efc61 = function(arg0) {
        const ret = getObject(arg0).length;
        return ret;
    };
    
    imports.wbg.__wbg_set_5cf90238115182c3 = function(arg0, arg1, arg2) {
        getObject(arg0).set(getObject(arg1), arg2 >>> 0);
    };
    
    imports.wbg.__wbindgen_throw = function(arg0, arg1) {
        throw new Error(getStringFromWasm0(arg0, arg1));
    };
    
    imports.wbg.__wbindgen_memory = function() {
        const ret = wasm.memory;
        return addHeapObject(ret);
    };
    
    return imports;
}

function __wbg_init_memory(imports, maybe_memory) {}

function __wbg_finalize_init(instance) {
    wasm = instance.exports;
    cachedUint8Memory0 = null
    return wasm;
}

// Export the functions and classes
module.exports = {
    falconKeypair
};