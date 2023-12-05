# K07VN_Crypto #
https://github.com/TNK-ADMIN/K07VN_Crypto

* Vẫn hoạt động ổn định cho tới hiện tại
* Sử dụng Python >= 3.6

## **Installation** ##
```
pip install K07VN_Crypto
```
hoặc bạn có thể install từ github: 
```
pip install git+https://github.com/TNK-ADMIN/K07VN_Crypto@master
```

# **Usage** #

## Cơ Bản ##

Về cơ bản bạn chỉ cần install và import thư viện
```
from K07VN_Crypto import Crypto
```

Và sau đó có thể gán cho 1 biến hoặc không rồi sử dụng`
> ### Generate Key ###

```
crypto_instance = Crypto()

private_key, public_key = Crypto.generate_key()

plaintext = "Hello, World!"
encrypted_text = crypto_instance.encrypt(plaintext)
print("Encrypted:", encrypted_text)

decrypted_text = crypto_instance.decrypt(encrypted_text)
print("Decrypted:", decrypted_text)
```

> ### Custom Key ###

```
public_key = """\
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCCXBKdgaHDJGAe9lk8Y0osRTEe
VT7s6n2POfJSPVRnj4pIBu3x2oqFlyuyZlxQfhBCOaK3kagiclePQFGuIt39r/j9
UgmXucae6XVDMRJYjCLBFvX5A93iKtuxYHs7PiHsH7B92Rc0xhKNmcyVhGoicrqd
qcReN1CExmVpSt0yJwIDAQAB
-----END PUBLIC KEY-----"""

private_key = """\
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCCXBKdgaHDJGAe9lk8Y0osRTEeVT7s6n2POfJSPVRnj4pIBu3x
2oqFlyuyZlxQfhBCOaK3kagiclePQFGuIt39r/j9UgmXucae6XVDMRJYjCLBFvX5
A93iKtuxYHs7PiHsH7B92Rc0xhKNmcyVhGoicrqdqcReN1CExmVpSt0yJwIDAQAB
AoGAbVS1VB5lwhme+DjajLglfE2nrW4HcYIVPmt2HZ1MTfLoIhKVu9LzfKlVv7Dz
2ZpxHmniW50w63sEjqN+HdMmZKyVHM/zvy2Sb1Soz+AJQ8xzL6Lw1KWpXuIObA5P
zfNyQt1AZFuqCamBsKmCHhgpSqypCKtxx5q+PBsbTg1rSeECQQC6cWPEkchWTD13
5f/UDs5qCcubQ3JBxLFtUImLDDoNjD1QtOzK0n9+05sD6YTKZXbrq6bhqf5m0rzJ
0ZUCmnCRAkEAsv5WJhnuyIsLsGhKkIZ1UfLluLopd0tHhK7riyM+j4SJf955FVFp
i29R2DhiKXFUms2Q/VOy3CsgBXK2rjBTNwJBALOG7+yd++ytKRtEy1zkjPoqSHZP
MbwGrFp4jJjpwxS8j2YhcUmz+7SiCchwmb9SiHpSJTVyvVdBYSxstTF2iSECQA2u
58MN5HUsO/6GWnzl6n4TRYBzqsvV02fPP25piVTLWv+NcFAy4xCnt+gBl293nHIh
GN5k0Z2HJnGELXbvds0CQQCIR5KG1o0Tb5ZCB0PoHZEVvBbSh0qLRkNwA5IO4npU
j26wV8QxpL9EAadJssR+X1Rky551qWPgWOc1RA2bBzXQ
-----END RSA PRIVATE KEY-----"""
plaintext = "Hello, World!"
encrypted_text = crypto_instance.encrypt(plaintext)
print("Encrypted:", encrypted_text)

decrypted_text = crypto_instance.decrypt(encrypted_text)
print("Decrypted:", decrypted_text)
```


# **Kết thúc** #

## Contact ##

Zalo: 0964243159

Telegram: @tnk_k07vn
