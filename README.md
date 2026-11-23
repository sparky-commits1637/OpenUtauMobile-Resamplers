# OpenUtauMobile-Resamplers

The app reads `index.json` and `index.json.sig` from this repo (main branch).
It only accepts a catalog signed with YOUR private key, and every file's sha256 must match.

One-time: `pip install cryptography`, then `python tools/publish.py keygen`.
Paste the printed public key into `PublicKeyPem` in the app. Keep `tools/private.pem` off GitHub.

To publish a resampler:
1. Put its `.sh` (and support files) in a folder, e.g. `my-resampler/`.
2. Add an entry to `index.json` (`url` is relative to `index.json`, or a full https URL).
3. Bump `version` when files change, then run `python tools/publish.py sign`.
4. Upload `index.json`, `index.json.sig` and the folder.

Name binaries with an extension (e.g. `.bin`): any extensionless file is treated as a resampler.
