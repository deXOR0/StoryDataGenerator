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
    # print(options)
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
    # print(STORY_FILES)
    return True

story = None
chapter = None
activity = None
func = None

def process_story(story_file):
    global TAGS, STORY_TEMPLATE, CHAPTER_TEMPLATE, COMPY_CONVERSATION_TEMPLATE, USER_CONVERSATION_TEMPLATE, NARRATION_TEMPLATE, COMPY_TRUE_TEMPLATE, COMPY_FALSE_TEMPLATE, REORDER_TEMPLATE, SINGLE_CHOICE_TEMPLATE, MULTI_SELECT_TEMPLATE, story, chapter, activity, func

    story_data = ''
    with open(story_file, encoding='utf-8') as f:
        story_data = f.read().splitlines()
        props = []
        for line, data in enumerate(story_data):
            line += 1
            # print(line, data)
            if data.startswith('<'):
                if func:
                    if func.__name__ == 'build_story':
                        # print('build_story', props)
                        story = None
                        story = func(props[0])
                    elif func.__name__ == 'build_intro':
                        # print('build_story', props)
                        func(story, props[0])
                    elif func.__name__ == 'build_chapter':
                        # print('build_story', props)
                        chapter=None
                        chapter = func(story, props[0])
                    elif func.__name__ == 'build_narration':
                        # print('build_story', props)
                        func(chapter, props[0])
                    elif func.__name__ == 'build_conversation':
                        # print('build_story', props)
                        func(chapter, props)
                    elif func.__name__ == 'build_reorder':
                        # print('build_story', props)
                        activity = None
                        activity = func(chapter)
                    elif func.__name__ == 'build_single_choice':
                        # print('build_story', props)
                        activity = None
                        activity = func(chapter)
                    elif func.__name__ == 'build_multi_select':
                        # print('build_story', props)
                        activity = None
                        activity = func(chapter)
                    elif func.__name__ == 'build_repeating':
                        # print('build_story', props)
                        func(activity)
                    elif func.__name__ == 'build_prompt':
                        # print('build_story', props)
                        func(activity, props[0])
                    elif func.__name__ == 'build_options':
                        # print('build_story', props)
                        print(props)
                        func(activity, props)
                    elif func.__name__ == 'build_answer':
                        # print('build_story', props)
                        func(activity, props)
                    elif func.__name__ == 'build_true_response':
                        # print('build_story', props)
                        func(activity, props[0])
                    elif func.__name__ == 'build_false_response':
                        # print('build_story', props)
                        func(activity, props[0])

                    func = None
                    props = []
                try:
                    func = TAGS[data]
                except:
                    error(f'[Line {line}]: {data} tag is not defined, maybe a typo?')
                    exit()
            else:
                if len(data) > 0:
                    # print('Props data', props)
                    props.append(data)

        print(story)
            
        with open(f'{story_file}.swift', encoding='utf-8', mode='w') as o:
            try:
                # print(story.to_json())
                # o.write(json.dumps(story.to_json(), cls=CustomEncoder))
                # o.writelines(story)
                # print(story)
                pass
            except Exception as e:
                print(e)
        print('---End of Story---')

if __name__ == '__main__':
    load_stories()
    for story_file in STORY_FILES:
        process_story(story_file)