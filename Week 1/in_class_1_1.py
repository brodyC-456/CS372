
s = "Hi 🙂"
print_bytes = lambda string: print(' '.join(f'{b:02x}' for b in string))

print_bytes(s.encode("utf-8"))
#Output: 48 69 20 f0 9f 99 82
#print_bytes(s.encode("ascii")), output: error, ascii not recognized as a string encoder

print_bytes(s.encode("utf-16"))
#Output: ff fe 48 00 69 00 20 00 3d d8 42 de, This is much longer than the utf-8 string and the hex values are different

encoded = s.encode("utf-16")
#print(encoded.decode("utf-8")), Throws an error due to an invalid starting byte.
print(encoded.decode("utf-16")) # decodes correctly!