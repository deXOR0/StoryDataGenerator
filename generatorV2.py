import os
import json
from better_terminal import *
from data_structure import *

STORIES_PATH = 'stories'
STORY_FILES = []
STORY_TEMPLATE = 'Story("{}", "{}", "{}", [{}])'
CHAPTER_TEMPLATE = 'Chapter("{}", "{}", [{}])'
COMPY_CONVERSATION_TEMPLATE = 'CompyConversationMessage("{}")'
USER_CONVERSATION_TEMPLATE = 'UserConversationMessage("{}")'
NARRATION_TEMPLATE = 'NarrationMessage("{}")'
COMPY_TRUE_TEMPLATE = 'CompyTrueMessage("{}")'
COMPY_FALSE_TEMPLATE = 'CompyFalseMessage("{}")'
REORDER_TEMPLATE = 'ReorderMessage("{}", [{}], [{}], {}, {}, {}'
SINGLE_CHOICE_TEMPLATE = 'SingleChoiceMessage("{}", [{}], "{}", {}, {}, {})'
MULTI_SELECT_TEMPLATE = 'MultiSelectMessage("{}", [{}], "{}", {}, {}, {})'

def build_story(title):
    story = Story(title)
    return story

def build_intro(story, intro):
    story.intro = intro

def build_chapter(story, chapter_title):
    story.chapters.append(Chapter(chapter_title))
    return story.chapters[-1]    

def build_narration(chapter, narration):
    chapter.messages.append(narration)

def build_conversation(chapter, conversations):
    for line in conversations:
        if line.startswith('C: '):
            chapter.messages.append(CompyConversationMessage(line.replace('C: ', '')))
        else:
            chapter.messages.append(UserConversationMessage(line.replace('U: ', '')))

def build_reorder(chapter):
    activity = ReorderMessage()
    chapter.messages.append(activity)
    return activity

def build_single_choice(chapter):
    activity = SingleChoiceMessage()
    chapter.messages.append(activity)
    return activity

def build_multi_select(chapter):
    activity = MultiSelectMessage()
    chapter.messages.append(activity)
    return activity

def build_repeating(activity):
    activity.repeating = True

def build_prompt(activity, prompt):
    activity.prompt = prompt

def build_options(activity, options):
    print(options)
    for option in options:
        activity.options.append(option)

def build_answer(activity, answer):
    if len(answer) > 1:
        for ans in answer:
            activity.answer.append(ans)
    else:
        activity.answer = answer

def build_true_response(activity, response):
    activity.true_response = CompyTrueMessage(response)

def build_false_response(activity, response):
    activity.false_response = CompyFalseMessage(response)

TAGS = {
    '<Story>': build_story, '<Intro>': build_intro, '<Chapter>': build_chapter, '<Narration>': build_narration, '<Conversation>': build_conversation, '<Reorder>': build_reorder, '<SingleChoice>': build_single_choice, '<MultiSelect>': build_multi_select, '<Repeating>': build_repeating, '<Prompt>': build_prompt, '<Options>': build_options, '<Answer>': build_answer, '<TrueResponse>': build_true_response, '<FalseResponse>': build_false_response
    }

def load_stories():
    global STORIES_PATH, STORY_FILES
    if not os.path.exists(STORIES_PATH):
        warning('Stories Directory is not found!')
        os.mkdir(STORIES_PATH)
        success('Stories Directory is created')
    else:
        success('Stories Directory is found')
    STORY_FILES = [os.path.join(STORIES_PATH, f) for f in os.listdir(STORIES_PATH) if os.path.isfile(os.path.join(STORIES_PATH, f))]
    
    if len(STORY_FILES) <= 0:
        error('No stories found on Stories Directory!')
        return False
    
    success('Story files are loaded')
    print(STORY_FILES)
    return True

def find_tag(line, data, tag):
    limit = len(data)
    while data[line] != tag:
        line += 1
        if line >= limit:
            exit()
    return line

def find_any_tag(line, data):
    limit = len(data)
    while not data[line].startswith('<'):
        line += 1
        if line >= limit:
            exit()
    tag = data[line] 
    return line, tag

def get_props(line, data):
    props = []

    while True:
        if len(data[line]) > 0 and not data[line].startswith('<'):
            props.append(data[line])
        line += 1
        if data[line].startswith('<'):
            break
    return line, props

def process_story(story_file):
    global TAGS, STORY_TEMPLATE, CHAPTER_TEMPLATE, COMPY_CONVERSATION_TEMPLATE, USER_CONVERSATION_TEMPLATE, NARRATION_TEMPLATE, COMPY_TRUE_TEMPLATE, COMPY_FALSE_TEMPLATE, REORDER_TEMPLATE, SINGLE_CHOICE_TEMPLATE, MULTI_SELECT_TEMPLATE

    story_data = ''
    with open(story_file, encoding='utf-8') as f:
        story_data = f.read().splitlines()
        check_tags(story_data)
        line = 0
        line, props = get_props(find_tag(line, story_data, '<Story>'), story_data)
        title = props[0]
        story = build_story(title)
        line, props = get_props(find_tag(line, story_data, '<Intro>'), story_data)
        intro = props[0]
        story.intro = intro
        while line < len(story_data):
            line, props = get_props(find_tag(line, story_data, '<Chapter>'), story_data)
            title = props[0]
            chapter = build_chapter(story, title)
            while (story_data[line] != '<Chapter>'):
                line, tag = find_any_tag(line, story_data)
                if tag == '<Conversation>':
                    line, props = get_props(find_tag(line, story_data, tag), story_data)
                    build_conversation(chapter, props)
                elif tag == '<Reorder>':
                    activity = build_reorder()
                    line, tag = find_any_tag(line, story_data)
                    if tag == '<Repeating>':
                        activity.repeating = True
                    
                    



        
            
        with open(f'{story_file}.json', encoding='utf-8', mode='w') as o:
            try:
                # print(story.to_json())
                o.write(json.dumps(story.to_json(), cls=CustomEncoder))
            except Exception as e:
                print(e)
        print('---End of Story---')

def check_tags(data):
    for line, d in enumerate(data):
        try:
            if d.startswith('<'):
                func = TAGS[d]
        except:
            error(f'[Line {line+1}]: {d} tag is not defined, maybe a typo?')
            exit()

if __name__ == '__main__':
    load_stories()
    for story_file in STORY_FILES:
        process_story(story_file)