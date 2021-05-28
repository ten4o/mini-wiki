class DB:
    def __init__(self):
        self.self = self

    def insert_topic(self, title: str, body: str, tag_list: list[str]):
        print('insert_topic')