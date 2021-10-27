class Task:

    def __init__(self, id, title, description, done):
        self.id = id
        self.title = title
        self.description = description
        self.done = done

    def set_id(self, id):
        self.id = id

    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description = description

    def set_done(self, done):
        self.done = done
