from six.moves import queue

class Scheduler(object):
    class Event(object):
        def __init__(self, time, component, fire=True):
            self.time = time
            self.component = component
            self.fire = fire

        def __lt__(self, other):
            return self.time < other.time

    def __init__(self, *components):
        self.event_queue = queue.PriorityQueue()

        for component in components:
            self.event_queue.put(Scheduler.Event(
                component.offset,
                component,
                True,
            ))

    def next(self):
        time = self.event_queue.queue[0].time

        awake = []
        asleep = []

        while self.event_queue.queue[0].time == time:
            event = self.event_queue.get()
            component = event.component

            if event.fire:
                next_time = event.time + component.sleep
                awake.append(component)
            else:
                next_time = event.time + component.interval
                asleep.append(component)

            self.event_queue.put(Scheduler.Event(next_time, component, not event.fire))

        for component in asleep:
            component.expose_output()

        for component in awake:
            component.collect_input()

        for component in awake:
            component.fire()
