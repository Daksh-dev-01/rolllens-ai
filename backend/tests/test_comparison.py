from app.services.comparison import compare_records

def test_modification_detected():
    old=[{"record_id":"a","voter_id":"ID1","name":"Ravi","age":30,"page_number":2}]
    new=[{"record_id":"b","voter_id":"ID1","name":"Ravi","age":31,"page_number":3}]
    out=compare_records(old,new)
    assert len(out)==1 and out[0]["category"]=="modification" and out[0]["changed_fields"]["age"]=={"old":30,"new":31}
def test_addition_removal():
    out=compare_records([{"record_id":"a","voter_id":"A"}],[{"record_id":"b","voter_id":"B"}])
    assert {x["category"] for x in out} == {"addition","removal"}
def test_null_identifiers_conservative():
    out=compare_records([{"record_id":"a","name":"Same"}],[{"record_id":"b","name":"Same"}])
    assert len(out)==2 and all(x["human_review_required"] for x in out)
def test_spelling_difference_requires_review():
    out=compare_records([{"voter_id":"ID1","name":"Smyth"}],[{"voter_id":"ID1","name":"Smith"}])
    assert out[0]["category"]=="modification" and out[0]["human_review_required"]
def test_duplicate_identifiers_are_ambiguous():
    out=compare_records([{"voter_id":"X"},{"voter_id":"X"}],[{"voter_id":"X"}])
    assert any(x["category"]=="ambiguous_match" for x in out)
