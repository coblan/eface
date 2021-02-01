import hashlib

def param_sign(key,params):
    "key一般为secerat"
    sign_str = ''
    for k,v in sorted(params.items(),key=lambda p:p[0]):
        if v:
            sign_str += '{key}={value}&'.format(key=k,value=v)
    sign_str = sign_str + 'key=' + key
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()        