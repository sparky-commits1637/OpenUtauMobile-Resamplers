"""Run on your own device. pip install cryptography
  python publish.py keygen     -> makes private.pem (KEEP SECRET, never upload) and prints the public key
  python publish.py sign       -> fills every sha256 in index.json, then writes index.json.sig
"""
import sys, json, hashlib, os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "private.pem")
INDEX = os.path.join(HERE, "index.json")

if sys.argv[1:] == ["keygen"]:
    key = ec.generate_private_key(ec.SECP256R1())
    open(KEY, "wb").write(key.private_bytes(serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    print(key.public_key().public_bytes(serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo).decode())
    print("Paste the public key into ResamplerCatalogService.PublicKeyPem.")
elif sys.argv[1:] == ["sign"]:
    data = json.load(open(INDEX, encoding="utf-8"))
    for r in data["resamplers"]:
        for f in r["files"]:
            if "://" in f["url"]:
                print("skip hash (remote url):", f["url"]); continue
            f["sha256"] = hashlib.sha256(open(os.path.join(HERE, f["url"]), "rb").read()).hexdigest()
    raw = json.dumps(data, indent=2).encode("utf-8")
    open(INDEX, "wb").write(raw)
    key = serialization.load_pem_private_key(open(KEY, "rb").read(), None)
    open(INDEX + ".sig", "wb").write(key.sign(raw, ec.ECDSA(hashes.SHA256())))
    print("Signed. Upload index.json, index.json.sig and the resampler folders.")
else:
    print(__doc__)
