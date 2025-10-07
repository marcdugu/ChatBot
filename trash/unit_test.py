# pytest -q
import pytest

from ChatBot_Proj import (
    check_if_faq_or_product,
    decide_task_nature,
    get_params_for_task,
)

def test_check_if_faq_or_product_basic_types_and_tokens():
    label, total_tokens = check_if_faq_or_product("What are your working hours?", simplified=True)
    assert isinstance(label, str)
    assert len(label.split()) == 1, "The label should be a single word, e.g., 'FAQ' or 'Product'."
    assert total_tokens <= 180

@pytest.mark.parametrize(
    "query,expected",
    [
        ("What is your return policy?", "FAQ"),
        ("Give me three examples of blue Tshirts you have available.", "Product"),
        ("How can I contact the user support?", "FAQ"),
        ("Do you have blue Dresses?", "Product"),
        ("Create a look suitable for a wedding party happening during dawn.", "Product"),
    ],
)
def test_check_if_faq_or_product_labels(query, expected):
    label, _ = check_if_faq_or_product(query, simplified=True)
    assert label == expected

def test_decide_task_nature_types_and_budget():
    # Use simplified=True to keep the test offline and deterministic
    label, total_tokens = decide_task_nature("What are your working hours?", simplified=True)
    assert isinstance(label, str)
    assert total_tokens >= 0

@pytest.mark.parametrize(
    "query,expected",
    [
        ("Give me two sneakers with vibrant colors.", "technical"),
        ("What are the most expensive clothes you have in your catalogue?", "technical"),
        ("I have a green Dress and want an accessory suggestion.", "creative"),
        ("Give me three trousers with vibrant colors you have in your catalogue.", "technical"),
        ("Create a look for a woman walking in a park on a sunny day. It must be fresh due to hot weather.", "creative"),
    ],
)
def test_decide_task_nature_labels(query, expected):
    label, total_tokens = decide_task_nature(query, simplified=True)
    assert label == expected
    assert total_tokens < 170

def test_get_params_for_task_returns_dict():
    out = get_params_for_task("technical")
    assert isinstance(out, dict)




