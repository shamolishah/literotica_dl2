class Story:
    def __init__(self,story_id: str) -> None:
        self.url: str = f"https://www.literotica.com/s/{story_id}"
        self.fp = ""
        self.author = ""
        self.category = ""
        self.description = ""
        self.num_pages = 0
        self.text = []
        self.title = ""
