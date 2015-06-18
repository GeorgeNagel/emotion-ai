from ai.core.obj import Object
from ai.core.action import Action


class Kill(Action):
    name = "Kill"


def apply_action(action=None, subject=None, obj=None, viewers=None):
    assert(issubclass(action, Action))
    assert(isinstance(subject, Object))
    assert(isinstance(obj, Object))
    assert(isinstance(viewers, list))
    for viewer in viewers:
        prob = 1
        new_emotions = viewer.emotions_for_action(
            action, subject, obj, prob)
        viewer.emotions.extend(new_emotions)
