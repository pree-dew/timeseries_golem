import os
import click
import watchdog.events
import watchdog.observers

from functools import update_wrapper

class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, pattern, ctx):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=[pattern],
                                                             ignore_directories=True, case_sensitive=False)
        self.ctx = ctx

    def on_modified(self, event):
        print("Received modified event - % s." % event.src_path)
        print("reloading.....")
        self.ctx.obj["reload"] = True


def with_or_without_reload(f):
    @click.pass_context
    def wrapper(ctx, *args, **kwargs): 
        if kwargs["reload"]:
            if ctx.obj is None:
                ctx.obj = dict()

            src_path = os.path.dirname(kwargs["sg_file"])
            event_handler = Handler("*.json", ctx)
            observer = watchdog.observers.Observer()
            observer.schedule(event_handler, path=src_path, recursive=True)
            ctx.obj["observer"] = observer

        return f(ctx, **kwargs)
    return update_wrapper(wrapper, f)


