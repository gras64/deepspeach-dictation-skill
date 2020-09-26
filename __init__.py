from mycroft import MycroftSkill, intent_file_handler


class DeepspeachDictation(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('dictation.deepspeach.intent')
    def handle_dictation_deepspeach(self, message):
        self.speak_dialog('dictation.deepspeach')


def create_skill():
    return DeepspeachDictation()

