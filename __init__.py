import re
import time
from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message
from mycroft import FallbackSkill


class DeepspeachDictation(FallbackSkill):
    def __init__(self):
        #MycroftSkill.__init__(self)
        super(DeepspeachDictation, self).__init__()

    def initialize(self):
        self.characters_value = self.translate_namedvalues('character.value')
        #self.log.info("value: "+str(self.characters_value))
        self.utter = ""

    @intent_file_handler('dictation.deepspeach.intent')
    def handle_dictation_deepspeach(self, message):
        self.speak_dialog('dictation.deepspeach')
        self.start_loop()
    
    def start_loop(self):
        self.register_fallback(self.handler_utterance, 1)
        #self.add_event('recognizer_loop:utterance',
        #            self.handler_utterance)
        self.add_event('recognizer_loop:record_end',
                    self.recognizer_handler)
        self.bus.emit(Message('mycroft.mic.listen'))


    def recognizer_handler(self):
        time.sleep(5) #bad
        self.bus.emit(Message('mycroft.mic.listen'))

    def handler_utterance(self, message):

        if message.data.get('utterance'):
            msg = message.data.get('utterance')
            if self.voc_match(msg, "stop"):
                self.stop_loop()
            utter = self.utter+msg
            utter = self.replace_caracters(utter)
            if self.voc_match(msg, "delete.last.sentence"):
                utter = re.findall(r'(#+\s?.*)|(^[,.: ]*)', '', utter, flags=re.M)
            if self.voc_match(msg, "delete.last.word"):
                pass
            if self.voc_match(msg, "read.out"):
                self.speak(''.join(utter))
            utter = ''.join(utter)
            self.log.info(str(utter))
            self.gui.clear()
            self.enclosure.display_manager.remove_active()
            self.gui.show_text(utter)
            #self.speak("erkenne: "+str(utter))
            self.utter = utter
        return True
    
    def replace_caracters(self, utter):
        words = utter.split(" ")
        self.log.info(str(self.characters_value))
        for character in self.characters_value:
            self.log.info(str(character))
            utter = utter.replace(" "+character+" ", self.characters_value[character]+" ")
        return utter

    def stop_loop(self):
        #self.remove_event('recognizer_loop:utterance')
        self.remove_event('recognizer_loop:record_end')
        self.remove_fallback(self.handler_utterance)
        self.gui.clear()
        self.enclosure.display_manager.remove_active()
        self.gui.show_text("send: "+utter)
        self.speak("send: "+self.utter) ######################################################## Send data
        self.utter = ""

    def shutdown(self):
        super(DeepspeachDictation, self).shutdown()
        self.remove_fallback(self.handler_utterance)
        self.remove_event('recognizer_loop:utterance')
        self.remove_event('recognizer_loop:record_end')


def create_skill():    
    return DeepspeachDictation()

