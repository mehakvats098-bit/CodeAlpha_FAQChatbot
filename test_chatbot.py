
from chatbot import get_response


def test_admission_question():
    result = get_response("How do I join this college?")
    assert result["known"] is True
    assert "admission" in result["answer"].lower()


def test_fees_question():
    result = get_response("Tell me about the fee structure")
    assert result["known"] is True


def test_admit_card_question():
    result = get_response("I lost my hall ticket")
    assert result["known"] is True


def test_scholarship_question():
    result = get_response("Can I get financial assistance?")
    assert result["known"] is True


def test_portal_question():
    result = get_response("The college portal isn't working")
    assert result["known"] is True


if __name__ == "__main__":
    tests = [
        test_admission_question,
        test_fees_question,
        test_admit_card_question,
        test_scholarship_question,
        test_portal_question,
    ]

    passed = 0

    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
            passed += 1
        except AssertionError:
            print(f"FAIL: {test.__name__}")

    print(f"\nResults: {passed}/{len(tests)} tests passed.")
