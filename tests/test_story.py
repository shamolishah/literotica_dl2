from literotica_dl2.story import Story


def test_metadata(story: Story):
    assert story.title == "E-Beth Ch. 01"
    assert story.author == "bluedragonauthor"
    assert story.category == "Group Sex"
    assert story.description == "E-Beth from 'The Book of David' searches for happiness."
    assert story.pages == 7
    assert story.text[:10] == "****\n\nThe "
