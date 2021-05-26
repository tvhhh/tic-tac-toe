
def lock(session):
    session['wait'] = True

def release(session):
    session['wait'] = False

def lock_session(session):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not 'init' in session:
                return 'Session not initialized', 405
            if session['wait']:
                return 'Session is being locked', 405
            lock(session)
            ret_val = func(*args, **kwargs)
            release(session)
            return ret_val
        return wrapper
    return decorator
