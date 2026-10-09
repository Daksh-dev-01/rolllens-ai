import pytest
from app.services.safe_query import plan_question
@pytest.mark.parametrize("q", ["DROP TABLE voter_records", "how many records; DELETE FROM voter_records", "show names of voters", "SELECT * FROM voter_records"])
def test_reject_unsafe_or_personal(q):
    with pytest.raises(ValueError): plan_question(q)
def test_count_plan(): assert plan_question("How many records are present?").kind == "record_count"
def test_age_distribution_plan(): assert plan_question("age-group distribution").kind == "age_distribution"
def test_unverified_plan(): assert plan_question("How many records have unverified fields?").kind == "unverified_count"
def test_unsupported_question():
    with pytest.raises(ValueError): plan_question("Which voter has the oldest age?")
