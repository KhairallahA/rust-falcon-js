import wasmtime
import base64
import os

# Read the WASM file as UTF-8 string
with open('./module.wasm', 'r', encoding='utf-8') as wasm_file:
    wasm_utf = wasm_file.read()
# Decode from base64
wasm_bytes = base64.b64decode(wasm_utf)

# Global variables
cached_uint8_memory0 = None
wasm = None
wasm_memory = None

# Heap management similar to JS version
heap = [None] * 128 + [None, None, True, False]
heap_next = len(heap)

def get_object(idx):
    return heap[idx]

def drop_object(idx):
    global heap_next
    if idx < 132:
        return
    heap[idx] = heap_next
    heap_next = idx

def take_object(idx):
    ret = get_object(idx)
    drop_object(idx)
    return ret

def add_heap_object(obj):
    global heap_next
    if heap_next == len(heap):
        heap.append(len(heap) + 1)
    idx = heap_next
    heap_next = heap[idx]
    heap[idx] = obj
    return idx

# Memory management functions
def get_uint8_memory0():
    global cached_uint8_memory0, wasm
    if cached_uint8_memory0 is None or len(cached_uint8_memory0) == 0:
        cached_uint8_memory0 = bytearray(wasm.memory.buffer)
    return cached_uint8_memory0

def get_string_from_wasm0(ptr, len_):
    memory = get_uint8_memory0()
    return bytes(memory[ptr:ptr+len_]).decode('utf-8')

def __wbg_get_imports():
    imports = {
        "wbg": {
            "__wbindgen_object_drop_ref": lambda arg0: take_object(arg0),
            "__wbindgen_object_clone_ref": lambda arg0: add_heap_object(get_object(arg0)),
            "__wbg_log_233cc96097d5ec7d": lambda arg0, arg1: print(get_string_from_wasm0(arg0, arg1)),
            "__wbg_buffer_085ec1f694018c4f": lambda arg0: add_heap_object(get_object(arg0)),
            "__wbg_newwithbyteoffsetandlength_6da8e527659b86aa": lambda arg0, arg1, arg2: add_heap_object(
                bytearray(wasm_memory.read(store, arg1, arg2))
            ),
            "__wbg_new_8125e318e6245eed": lambda arg0: add_heap_object(
                bytearray(wasm_memory.read(store, 0, wasm_memory.data_len(store)))
            ),
            "__wbg_newwithlength_e5d69174d6984cd7": lambda arg0: add_heap_object(bytearray(arg0)),
            "__wbg_length_72e2208bbc0efc61": lambda arg0: len(get_object(arg0)),
            "__wbg_set_5cf90238115182c3": lambda arg0, arg1, arg2: get_object(arg0).__setitem__(slice(arg2, arg2 + len(get_object(arg1))), get_object(arg1)),
            "__wbindgen_throw": lambda arg0, arg1: (_ for _ in ()).throw(Exception(get_string_from_wasm0(arg0, arg1))),
            "__wbindgen_memory": lambda: add_heap_object(wasm_memory),
        }
    }
    return imports

def __wbg_init_memory(imports, maybe_memory):
    pass

def __wbg_finalize_init(instance, store):
    global wasm, cached_uint8_memory0, wasm_memory
    wasm = instance.exports(store)
    cached_uint8_memory0 = None
    wasm_memory = wasm["memory"]
    return wasm

def init():
    global wasm, store, wasm_memory
    if wasm is not None:
        return wasm
    
    # Create store and imports
    store = wasmtime.Store()
    imports = __wbg_get_imports()
    
    # Create module from the WebAssembly bytes
    module = wasmtime.Module(store.engine, wasm_bytes)
    
    # Create linker
    linker = wasmtime.Linker(store.engine)
    
    # Define functions with proper signatures
    for namespace, funcs in imports.items():
        for func_name, func_impl in funcs.items():
            # Special handling for known void functions
            if func_name in ['__wbindgen_object_drop_ref', '__wbg_set_5cf90238115182c3', 
                            '__wbindgen_throw', '__wbg_log_233cc96097d5ec7d']:
                # Create void function
                param_count = func_impl.__code__.co_argcount
                param_types = [wasmtime.ValType.i32()] * param_count
                func_type = wasmtime.FuncType(param_types, [])
                
                # Create a wrapper that ensures no return value
                def create_void_wrapper(f):
                    def wrapper(*args):
                        f(*args)
                        # Explicitly return nothing for wasmtime
                    return wrapper
                
                wrapped_func = create_void_wrapper(func_impl)
                wasm_func = wasmtime.Func(store, func_type, wrapped_func)
            else:
                # Create function with i32 return
                param_count = func_impl.__code__.co_argcount
                param_types = [wasmtime.ValType.i32()] * param_count
                func_type = wasmtime.FuncType(param_types, [wasmtime.ValType.i32()])
                
                # Create a wrapper that ensures a return value
                def create_return_wrapper(f):
                    def wrapper(*args):
                        result = f(*args)
                        return result if result is not None else 0
                    return wrapper
                
                wrapped_func = create_return_wrapper(func_impl)
                wasm_func = wasmtime.Func(store, func_type, wrapped_func)
            
            # Define the function in the linker
            linker.define(store, namespace, func_name, wasm_func)
    
    instance = linker.instantiate(store, module)
    wasm = instance.exports(store)
    wasm_memory = wasm["memory"]
    return __wbg_finalize_init(instance, store)


init()

def falcon_keypair(_seed):
    global store
    print("Exports:", [name for name in wasm.keys()])
    ret = wasm['falconKeypair'](store, add_heap_object(_seed))
    print(f"seed_ref: {add_heap_object(_seed)}")
    print(f"ret: {ret}")
    return KeyPair._wrap(ret)

# KeyPair class
class KeyPair:
    def __init__(self):
        self.__wbg_ptr = None
    
    @staticmethod
    def _wrap(ptr):
        ptr = int(ptr & 0xFFFFFFFF)  # >>> 0 equivalent in Python
        obj = KeyPair()
        obj.__wbg_ptr = ptr
        return obj
    
    def __destroy_into_raw(self):
        ptr = self.__wbg_ptr
        self.__wbg_ptr = 0
        return ptr
    
    def free(self):
        ptr = self.__destroy_into_raw()
        if ptr != 0:
            wasm['__wbg_keypair_free'](store, ptr)
    
    @property
    def public(self):
        if self.__wbg_ptr is None:
            raise ValueError("KeyPair has been freed")
        ret = wasm['keypair_public'](store, self.__wbg_ptr)
        return take_object(ret)
    
    @property
    def secret(self):
        if self.__wbg_ptr is None:
            raise ValueError("KeyPair has been freed")
        ret = wasm['keypair_secret'](store, self.__wbg_ptr)
        return take_object(ret)


seed_bytes = bytes.fromhex("e95afe2bfb5f361b4571e4de191d9af2de88d14ca3c34158fc9e9222746e986fa4ad4c577f80335d96f1c06a3db0e6b7")
seed = bytearray(seed_bytes)
# print(seed)
keypair = falcon_keypair(seed)
print('Generated keypair')

# Get public and secret keys
public_key = keypair.public
secret_key = keypair.secret

print('Public key length:', len(public_key))
print('Secret key length:', len(secret_key))
print('Public key:', list(public_key)[:100])  # First 100 bytes
print('Secret key:', list(secret_key)[:100])  # First 100 bytes

# Clean up
keypair.free()