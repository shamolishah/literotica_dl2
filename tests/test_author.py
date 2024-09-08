from literotica_dl2.author import Author


def test_metadata(author: Author):
    assert author.slug == "aurelius1982"
    assert author.author_name == "aurelius1982"
    assert len(author.series) == 9
    assert len(author.individual_stories) == 5
