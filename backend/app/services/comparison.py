"""Deterministic, conservative document-version comparison."""
from typing import Any
FIELDS = ("name", "relative_name", "house_number", "age", "gender")

def _value(record: dict, field: str):
    v = record.get(field)
    if isinstance(v, dict): return v.get("value")
    return v

def _ref(record: dict): return record.get("record_id") or record.get("id") or record.get("serial_number")

def compare_records(old_records: list[dict], new_records: list[dict]) -> list[dict]:
    """Match stable voter IDs first; then unique serials. Ambiguous fallback matches require review."""
    old_used, new_used, changes = set(), set(), []
    def stable_key(r):
        voter_id = _value(r, "voter_id")
        return ("voter_id", str(voter_id).strip().upper()) if voter_id else None
    def serial_key(r):
        serial = _value(r, "serial_number")
        return ("serial", str(serial).strip()) if serial is not None else None
    old_map = {}
    for i, r in enumerate(old_records):
        k = stable_key(r)
        if k: old_map.setdefault(k, []).append(i)
    pairs = []
    new_map = {}
    for j, r in enumerate(new_records):
        k = stable_key(r)
        if k: new_map.setdefault(k, []).append(j)
    for k, oi in old_map.items():
        nj = new_map.get(k, [])
        if len(oi) == len(nj) == 1: pairs.append((oi[0], nj[0], "stable_identifier"))
    old_serials, new_serials = {}, {}
    for i,r in enumerate(old_records):
        if i not in {p[0] for p in pairs} and serial_key(r): old_serials.setdefault(serial_key(r), []).append(i)
    for j,r in enumerate(new_records):
        if j not in {p[1] for p in pairs} and serial_key(r): new_serials.setdefault(serial_key(r), []).append(j)
    for k, oi in old_serials.items():
        nj = new_serials.get(k, [])
        if len(oi) == len(nj) == 1:
            # Serial matching is provisional, not proof of identity.
            pairs.append((oi[0], nj[0], "serial_candidate"))
    for i,j,match_method in pairs:
        old_used.add(i); new_used.add(j)
        old,new=old_records[i],new_records[j]
        changed={f:{"old":_value(old,f),"new":_value(new,f)} for f in FIELDS if _value(old,f) != _value(new,f)}
        if changed:
            changes.append({"category":"modification","old_record_ref":_ref(old),"new_record_ref":_ref(new),"changed_fields":changed,
              "old_source_page":old.get("page_number"),"new_source_page":new.get("page_number"),"confidence":"medium" if match_method=="stable_identifier" else "low",
              "review_status":"needs_review","match_method":match_method,"human_review_required":True,
              "note":"Field differences are candidate changes, not proof of identity or wrongdoing."})
    # Same identifier with duplicates is ambiguous: don't silently pair them.
    for i,r in enumerate(old_records):
        if i not in old_used:
            ambiguous = bool(stable_key(r) and len(old_map.get(stable_key(r),[]))>1) or bool(serial_key(r) and len(old_serials.get(serial_key(r),[]))>1)
            changes.append({"category":"removal" if not ambiguous else "ambiguous_match","old_record_ref":_ref(r),"new_record_ref":None,"changed_fields":{},"old_source_page":r.get("page_number"),"new_source_page":None,"confidence":"low" if ambiguous else "medium","review_status":"needs_review","human_review_required":True,"note":"Potential removal; confirm against source evidence."})
    for j,r in enumerate(new_records):
        if j not in new_used:
            ambiguous = bool(stable_key(r) and len(new_map.get(stable_key(r),[]))>1) or bool(serial_key(r) and len(new_serials.get(serial_key(r),[]))>1)
            changes.append({"category":"addition" if not ambiguous else "ambiguous_match","old_record_ref":None,"new_record_ref":_ref(r),"changed_fields":{},"old_source_page":None,"new_source_page":r.get("page_number"),"confidence":"low" if ambiguous else "medium","review_status":"needs_review","human_review_required":True,"note":"Potential addition; confirm against source evidence."})
    return changes
