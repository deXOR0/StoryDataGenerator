import json

class CompyConversationMessage:
    
    text = ''

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'CompyConversationMessage("{self.text}")'
    
    def to_json(self):
        return dict(text=self.text)

class UserConversationMessage:
    
    text = ''

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'UserConversationMessage("{self.text}")'
    
    def to_json(self):
        return dict(text=self.text)

class CompyFalseMessage:
    
    text = ''

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'CompyFalseMessage("{self.text}")'
    
    def to_json(self):
        return dict(text=self.text)

class CompyTrueMessage:
    
    text = ''

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'CompyTrueMessage("{self.text}")'
    
    def to_json(self):
        return dict(text=self.text)

class NarrationMessage:
    
    text = ''

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'NarrationMessage("{self.text}")'
    
    def to_json(self):
        return dict(text=self.text)

class MultiSelectMessage:
    
    prompt = ''
    options = []
    answer = []
    true_response = CompyTrueMessage('')
    false_response = CompyFalseMessage('')
    repeating = False

    def __repr__(self):
        return f'MultiSelectMessage("{self.prompt}", {self.options}, {self.answer}, {self.true_response}, {self.false_response}, {"true" if self.repeating else "false"})'
    
    def to_json(self):
        return dict(prompt=self.prompt, options=self.options, answer=self.answer, true_response=self.true_response, false_response=self.false_response, repeating=self.repeating)

class ReorderMessage:
    
    prompt = ''
    options = []
    answer = []
    true_response = CompyTrueMessage('')
    false_response = CompyFalseMessage('')
    repeating = False

    def __repr__(self):
        return f'ReorderMessage("{self.prompt}", {self.options}, {self.answer}, {self.true_response}, {self.false_response}, {"true" if self.repeating else "false"})'

    def to_json(self):
        return dict(prompt=self.prompt, options=self.options, answer=self.answer, true_response=self.true_response, false_response=self.false_response, repeating=self.repeating)

class SingleChoiceMessage:
    
    prompt = ''
    options = []
    answer = ''
    true_response = CompyTrueMessage('')
    false_response = CompyFalseMessage('')
    repeating = False

    def __repr__(self):
        return f'SingleChoiceMessage("{self.prompt}", {self.options}, "{self.answer}", {self.true_response}, {self.false_response}, {"true" if self.repeating else "false"})'
    
    def to_json(self):
        return dict(prompt=self.prompt, options=self.options, answer=self.answer, true_response=self.true_response, false_response=self.false_response, repeating=self.repeating)

class Chapter:

    title = ''
    logo = ''
    messages = []

    def __init__(self, title):
        self.title = title
        self.logo = title
    
    def __repr__(self):
        return f'Chapter("{self.title}", "{self.logo}", {self.messages})'
    
    def to_json(self):
        return dict(title=self.title, logo=self.logo, messages=self.messages)

class Story:

    title = ''
    intro = ''
    logo = ''
    chapters = []

    def __init__(self, title):
        self.title = title
        self.logo = title
    
    def __str__(self):
        return f'Story("{self.title}", "{self.intro}", "{self.logo}", {self.chapters})'

    def __repr__(self):
        return f'Story("{self.title}", "{self.intro}", "{self.logo}", {self.chapters})'
    
    def to_json(self):
        return dict(title=self.title, intro=self.intro, logo=self.logo, chapters=self.chapters)

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        else:
            return json.JSONEncoder.default(self, obj)