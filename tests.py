import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_removing_choice_reduces_choices_count():
    question = Question(title='What is 2+2?')
    choice1 = question.add_choice('3', False)
    choice2 = question.add_choice('4', True)
    
    assert len(question.choices) == 2
    question.remove_choice_by_id(choice1.id)
    assert len(question.choices) == 1
    assert question.choices[0].text == '4'

def test_removing_nonexistent_choice_raises_error():
    question = Question(title='Test question')
    question.add_choice('Option A', True)
    
    with pytest.raises(Exception, match="Invalid choice id"):
        question.remove_choice_by_id(999)

def test_removing_all_choices_empties_choices_list():
    question = Question(title='Test question')
    question.add_choice('A', True)
    question.add_choice('B', False)
    question.add_choice('C', False)
    
    assert len(question.choices) == 3
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_setting_correct_choices_updates_choice_status():
    question = Question(title='Multiple correct answers')
    choice1 = question.add_choice('Option A', False)
    choice2 = question.add_choice('Option B', False)
    choice3 = question.add_choice('Option C', False)
    
    question.set_correct_choices([choice1.id, choice3.id])
    
    assert question.choices[0].is_correct == True
    assert question.choices[1].is_correct == False
    assert question.choices[2].is_correct == True

def test_correcting_selected_choices_returns_only_correct_ones():
    question = Question(title='Test question', max_selections=2)
    choice1 = question.add_choice('Wrong answer', False)
    choice2 = question.add_choice('Correct answer', True)
    choice3 = question.add_choice('Another wrong', False)
    
    selected_ids = [choice1.id, choice2.id]
    correct_selections = question.correct_selected_choices(selected_ids)
    
    assert len(correct_selections) == 1
    assert choice2.id in correct_selections
    assert choice1.id not in correct_selections

def test_correcting_selected_choices_with_no_correct_selections_returns_empty():
    question = Question(title='Test question', max_selections=2)
    choice1 = question.add_choice('Wrong answer 1', False)
    choice2 = question.add_choice('Correct answer', True)
    choice3 = question.add_choice('Wrong answer 2', False)
    
    selected_ids = [choice1.id, choice3.id]
    correct_selections = question.correct_selected_choices(selected_ids)
    
    assert len(correct_selections) == 0

def test_selecting_too_many_choices_raises_error():
    question = Question(title='Single choice question', max_selections=1)
    choice1 = question.add_choice('Option A', True)
    choice2 = question.add_choice('Option B', False)
    
    with pytest.raises(Exception, match="Cannot select more than 1 choices"):
        question.correct_selected_choices([choice1.id, choice2.id])

def test_question_with_custom_max_selections_allows_multiple_selections():
    question = Question(title='Multiple choice question', max_selections=3)
    choice1 = question.add_choice('A', True)
    choice2 = question.add_choice('B', True)
    choice3 = question.add_choice('C', False)
    
    selected_ids = [choice1.id, choice2.id, choice3.id]
    correct_selections = question.correct_selected_choices(selected_ids)
    
    assert len(correct_selections) == 2
    assert choice1.id in correct_selections
    assert choice2.id in correct_selections

def test_choice_ids_are_sequential_and_unique():
    question = Question(title='Test question')
    choice1 = question.add_choice('First choice', False)
    choice2 = question.add_choice('Second choice', True)
    choice3 = question.add_choice('Third choice', False)
    
    assert choice1.id == 1
    assert choice2.id == 2
    assert choice3.id == 3
    
    all_ids = [choice.id for choice in question.choices]
    assert len(all_ids) == len(set(all_ids))

def test_question_maintains_choice_order():
    question = Question(title='Order test')
    texts = ['First', 'Second', 'Third', 'Fourth']
    
    for text in texts:
        question.add_choice(text, False)
    
    for i, expected_text in enumerate(texts):
        assert question.choices[i].text == expected_text