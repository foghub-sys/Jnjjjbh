"""Kaspa primitives used by the audit: address encoding, coinbase payload parsing, header hashing."""
import hashlib
import struct

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def _polymod(values):
    c = 1
    for d in values:
        c0 = c >> 35
        c = ((c & 0x07FFFFFFFF) << 5) ^ d
        if c0 & 0x01: c ^= 0x98F2BC8E61
        if c0 & 0x02: c ^= 0x79B76D99E2
        if c0 & 0x04: c ^= 0xF33E5FB3C4
        if c0 & 0x08: c ^= 0xAE2EABE2A8
        if c0 & 0x10: c ^= 0x1E4F43E470
    return c ^ 1


def _conv8to5(data):
    out, acc, bits = [], 0, 0
    for b in data:
        acc = (acc << 8) | b
        bits += 8
        while bits >= 5:
            bits -= 5
            out.append((acc >> bits) & 31)
    if bits:
        out.append((acc << (5 - bits)) & 31)
    return out


def encode_address(version, payload, prefix="kaspa"):
    data = _conv8to5(bytes([version]) + payload)
    checksum = _polymod([ord(c) & 31 for c in prefix] + [0] + data + [0] * 8)
    csum = [(checksum >> 5 * (7 - i)) & 31 for i in range(8)]
    return prefix + ":" + "".join(CHARSET[d] for d in data + csum)


def script_to_address(script: bytes):
    """Standard script public keys (script version 0) -> address; None for non-standard scripts."""
    if len(script) == 34 and script[0] == 0x20 and script[33] == 0xAC:
        return encode_address(0, script[1:33])
    if len(script) == 35 and script[0] == 0x21 and script[34] == 0xAB:
        return encode_address(1, script[1:34])
    if len(script) == 35 and script[0] == 0xAA and script[1] == 0x20 and script[34] == 0x87:
        return encode_address(8, script[2:34])
    return None


def parse_coinbase_payload(payload_hex):
    """Coinbase payload layout (consensus CoinbaseManager):
    blue_score u64 LE | subsidy u64 LE | script_version u16 LE | script_len u8 | script | extra_data."""
    p = bytes.fromhex(payload_hex)
    blue_score, subsidy, script_version = struct.unpack_from("<QQH", p, 0)
    slen = p[18]
    script = p[19:19 + slen]
    extra = p[19 + slen:]
    return {
        "blueScore": blue_score,
        "subsidy": subsidy,
        "scriptVersion": script_version,
        "script": script,
        "extra": extra,
        "minerAddress": script_to_address(script) if script_version == 0 else None,
        "minerInfo": extra.decode("utf-8", "replace"),
    }


def header_hash(h):
    """Recompute the block hash from header fields (consensus/core/src/hashing/header.rs)."""
    m = hashlib.blake2b(digest_size=32, key=b"BlockHash")
    m.update(struct.pack("<H", h["version"]))
    parents = h["parentsByLevel"]
    m.update(struct.pack("<Q", len(parents)))
    for level in parents:
        m.update(struct.pack("<Q", len(level)))
        for p in level:
            m.update(bytes.fromhex(p))
    for k in ("hashMerkleRoot", "acceptedIdMerkleRoot", "utxoCommitment"):
        m.update(bytes.fromhex(h[k]))
    m.update(struct.pack("<QIQQQ", int(h["timestamp"]), int(h["bits"]), int(h["nonce"]), int(h["daaScore"]), int(h["blueScore"])))
    bw = bytes.fromhex(h["blueWork"]).lstrip(b"\x00")
    m.update(struct.pack("<Q", len(bw)) + bw)
    m.update(bytes.fromhex(h["pruningPoint"]))
    return m.hexdigest()
