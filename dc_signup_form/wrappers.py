class TestWrapper:
    def submit(self, data, mailing_lists):
        print({
            'data': data,
            'mailing_lists': mailing_lists,
        })


class SendGridWrapper:
    def submit(self, data, mailing_lists):
        # TODO:
        # https://sendgrid.com/docs/API_Reference/api_v3.html
        pass
