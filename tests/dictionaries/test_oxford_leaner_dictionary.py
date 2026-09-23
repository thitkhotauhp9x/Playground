from app.libs.dictionaries.oxford_leaner_dictionary import OxfordLearnerDictionary


def test_hello_phonetic_br() -> None:
    dictionary = OxfordLearnerDictionary(word="hello")
    assert dictionary.phonetic_br() == "/həˈləʊ/"
