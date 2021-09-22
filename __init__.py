from mycroft import MycroftSkill, intent_file_handler


class Createservice(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('createservice.intent')
    def handle_createservice(self, message):
        self.speak_dialog('createservice')


def create_skill():
    return Createservice()

