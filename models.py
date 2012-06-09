from mongokit import Document


class BasePart(Document):
    use_dot_notation = True


class Intro(BasePart):
    structure = {
        'text': unicode,
    }


class Adjective(BasePart):
    structure = {
        'text': unicode,
    }


class Prefix(BasePart):
    structure = {
        'text': unicode,
    }


class Suffix(BasePart):
    structure = {
        'text': unicode,
        'case': unicode,
    }
    validators = {
        'case': lambda x: x in [u'm', u'w', u's', u'p'],
    }


class Action(BasePart):
    structure = {
        'action_s': unicode,
        'action_p': unicode,
        'text': unicode,
    }
