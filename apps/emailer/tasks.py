from emailer.engines import NewSupporterEngine

def send_support_email(supporter_id, promise_id):
    NewSupporterEngine(supporter_id, promise_id).send()