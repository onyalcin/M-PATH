class Empathy:
    def __init__(self):
        self.emotion_queue = None

    def mimicry(self, emotion_data):  # TODO: add AU, au recognition
        au = emotion_data["au"]
        au_list = []
        for gesture, amount in au.items():
            behaviors = self.return_au_category(gesture)
            for behavior in behaviors:
                # in affectiva au are represented as percent*100, so we need to
                if hasattr(behavior, "amount"):
                    behavior.amount = str(float(behavior.amount) * round(amount / 100, 2))
                au_list.append(behavior)
        return au_list

    def affect_match(self, emotion_data, limit=0):  # TODO: add another with more limit
        if emotion_data != {}:
            e = emotion_data["emotions"]
            recognition = max(e, key=e.get)
            amount = e[recognition]
            if amount > limit:
                if recognition != 'neutral':
                    return recognition, amount
                else:
                    return None, None
            else:
                return None, None
        else:
            return None, None

    # TODO: add average or a mixture of emotions, it might be interesting to test

    def affect_match_max_window(self, emotion_queue):  # TODO: this requires a queue of emotions
        for i in range(0, len(emotion_queue), 10):
            moving_window = {k["emotion"]: k["value"] for k in emotion_queue[i:i+10]}
            e = max(moving_window, key=moving_window.get)
            amount = moving_window[e]
            return e, amount

    '''
    def emotion_regulation():
        raise NotImplementedError  # TODO: regulate back to your own mood and the goal mood!
    '''