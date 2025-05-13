import wasmtime
import base64

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
    global wasm_memory
    # Always read the latest memory buffer
    memory = wasm_memory.read(store, 0, wasm_memory.data_len(store))
    return memory

def get_string_from_wasm0(ptr, len_):
    memory = get_uint8_memory0()
    return bytes(memory[ptr:ptr+len_]).decode('utf-8')

def __wbg_get_imports():
    imports = {}
    imports["wbg"] = {}

    def __wbindgen_object_drop_ref(arg0):
        take_object(arg0)
    imports["wbg"]["__wbindgen_object_drop_ref"] = __wbindgen_object_drop_ref

    def __wbindgen_object_clone_ref(arg0):
        ret = add_heap_object(get_object(arg0))
        return ret
    imports["wbg"]["__wbindgen_object_clone_ref"] = __wbindgen_object_clone_ref

    def __wbg_log_233cc96097d5ec7d(arg0, arg1):
        print(get_string_from_wasm0(arg0, arg1))
    imports["wbg"]["__wbg_log_233cc96097d5ec7d"] = __wbg_log_233cc96097d5ec7d

    def __wbg_buffer_085ec1f694018c4f(arg0):
        obj = get_object(arg0)
        if isinstance(obj, wasmtime._memory.Memory):
            # Get the raw memory buffer
            memory = get_uint8_memory0()
            # Create a new bytearray from the entire memory
            ret = add_heap_object(bytearray(memory))
        else:
            # If it's already a bytearray or bytes, create a copy
            ret = add_heap_object(bytearray(obj))
        return ret
    imports["wbg"]["__wbg_buffer_085ec1f694018c4f"] = __wbg_buffer_085ec1f694018c4f

    def __wbg_newwithlength_e5d69174d6984cd7(arg0):
        # Create a new bytearray of the specified length
        ret = add_heap_object(bytearray(arg0))
        return ret
    imports["wbg"]["__wbg_newwithlength_e5d69174d6984cd7"] = __wbg_newwithlength_e5d69174d6984cd7

    def __wbg_newwithbyteoffsetandlength_6da8e527659b86aa(arg0, arg1, arg2):
        # Get the buffer from the object at arg0
        buffer = get_object(arg0)
        if isinstance(buffer, wasmtime._memory.Memory):
            # Get the raw memory buffer
            memory = get_uint8_memory0()
            # Create a new bytearray from the memory slice
            ret = add_heap_object(bytearray(memory[arg1:arg1+arg2]))
        else:
            # If it's already a bytearray or bytes, create a copy
            ret = add_heap_object(bytearray(buffer[arg1:arg1+arg2]))
        return ret
    imports["wbg"]["__wbg_newwithbyteoffsetandlength_6da8e527659b86aa"] = __wbg_newwithbyteoffsetandlength_6da8e527659b86aa

    def __wbg_new_8125e318e6245eed(arg0):
        # Get the buffer from the object at arg0
        buffer = get_object(arg0)
        if isinstance(buffer, wasmtime._memory.Memory):
            # Get the raw memory buffer
            memory = get_uint8_memory0()
            # Create a new bytearray from the entire memory
            ret = add_heap_object(bytearray(memory))
        else:
            # If it's already a bytearray or bytes, create a copy
            ret = add_heap_object(bytearray(buffer))
        return ret
    imports["wbg"]["__wbg_new_8125e318e6245eed"] = __wbg_new_8125e318e6245eed

    def __wbg_length_72e2208bbc0efc61(arg0):
        ret = len(get_object(arg0))
        return ret
    imports["wbg"]["__wbg_length_72e2208bbc0efc61"] = __wbg_length_72e2208bbc0efc61

    def __wbg_set_5cf90238115182c3(arg0, arg1, arg2):
        target = get_object(arg0)
        source = get_object(arg1)
        
        # Convert to bytearray for modification
        if isinstance(target, bytes):
            target = bytearray(target)
            heap[arg0] = target
        
        # Ensure source is in the right format
        if isinstance(source, bytes):
            source = bytearray(source)
        
        # Perform the copy
        target[arg2:arg2+len(source)] = source
        return 0
    imports["wbg"]["__wbg_set_5cf90238115182c3"] = __wbg_set_5cf90238115182c3

    def __wbindgen_throw(arg0, arg1):
        raise Exception(get_string_from_wasm0(arg0, arg1))
    imports["wbg"]["__wbindgen_throw"] = __wbindgen_throw

    def __wbindgen_memory():
        ret = add_heap_object(wasm_memory)
        return ret
    imports["wbg"]["__wbindgen_memory"] = __wbindgen_memory

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

def refresh_uint8_memory0():
    global cached_uint8_memory0, wasm_memory
    memory = wasm_memory.read(store, 0, wasm_memory.data_len(store))
    cached_uint8_memory0 = memory

def falcon_keypair(_seed):
    global store
    seed_ref = add_heap_object(_seed)
    ret = wasm['falconKeypair'](store, seed_ref)
    # Refresh memory after WASM call
    refresh_uint8_memory0()
    # if 0 <= ret < len(heap):
    #     print(f"Heap object at ret ({ret}): {heap[ret]}")
    # else:
    #     print(f"Returned index {ret} is out of heap bounds!")
    return KeyPair._wrap(ret)

# KeyPair class
class KeyPair:
    def __init__(self):
        self.__wbg_ptr = None
    
    @staticmethod
    def _wrap(ptr):
        ptr = int(ptr >> 0)
        obj = KeyPair()
        obj.__wbg_ptr = ptr
        return obj
    
    def __destroy_into_raw(self):
        ptr = self.__wbg_ptr
        self.__wbg_ptr = 0
        return ptr
    
    def free(self):
        ptr = self.__destroy_into_raw()
        wasm['__wbg_keypair_free'](store, ptr)

    @property
    def public(self):
        ret = wasm['keypair_public'](store, self.__wbg_ptr)
        value = take_object(ret)
        if isinstance(value, int):
            # Assume this is a pointer to WASM memory, try to read a reasonable length (e.g., 897 for Falcon-512)
            memory = get_uint8_memory0()
            # You may need to adjust the length depending on your key size
            key_len = 897
            key_bytes = memory[value:value+key_len]
            return bytes(key_bytes)
        return value
    
    @property
    def secret(self):
        ret = wasm['keypair_secret'](store, self.__wbg_ptr)
        value = take_object(ret)
        if isinstance(value, int):
            # Assume this is a pointer to WASM memory, try to read a reasonable length (e.g., 1281 for Falcon-512)
            memory = get_uint8_memory0()
            key_len = 1281
            key_bytes = memory[value:value+key_len]
            return bytes(key_bytes)
        return value


seed_bytes = bytes.fromhex("e95afe2bfb5f361b4571e4de191d9af2de88d14ca3c34158fc9e9222746e986fa4ad4c577f80335d96f1c06a3db0e6b7")
seed = bytearray(seed_bytes)
keypair = falcon_keypair(seed)
print('Generated keypair')

# Get public and secret keys
public_key = keypair.public
secret_key = keypair.secret
print(f"seed: {list(seed)}")

print('Public key length:', len(public_key))
print('Secret key length:', len(secret_key))
print('Public key:', public_key[:100].hex())

# Clean up
# keypair.free()
