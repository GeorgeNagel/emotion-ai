from ai.core.obj import Object
from ai.core.action import Action


class Kill(Action):
    name = "Kill"

    @classmethod
    def register_viewer_beliefs(self, subject=None, obj=None, viewers=None):
        pass


class RemoveDisguise(Action):
    name = "RemoveDisguise"

    @classmethod
    def register_viewer_beliefs(self, subject=None, obj=None, viewers=None):
        disguised_subject_entity_id = subject.entity_id
        subject.disguised = False
        undisguised_subject_entity_id = subject.entity_id
        timestamp = 0
        belief_strength = 1
        for viewer in viewers:
            viewer.beliefs.set_entity_is_entity(
                timestamp, disguised_subject_entity_id,
                undisguised_subject_entity_id, belief_strength
            )


def apply_action(action=None, subject=None, obj=None, viewers=None):
    assert(issubclass(action, Action))
    assert(isinstance(subject, Object))
    assert(isinstance(obj, Object))
    assert(isinstance(viewers, list))
    for viewer in viewers:
        action.register_viewer_beliefs(
            subject=subject, obj=obj, viewers=viewers
        )
        prob = 1
        new_emotions = viewer.emotions_for_action(
            action, subject.entity_id, obj.entity_id, prob)
        viewer.emotions.extend(new_emotions)
