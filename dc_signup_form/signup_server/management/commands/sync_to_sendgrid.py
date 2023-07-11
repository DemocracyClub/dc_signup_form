import sys
import time
from django.core.management.base import BaseCommand
from django.db.models import Q, Func, F
from dc_signup_form.signup_server.models import SignupQueue
from dc_signup_form.signup_server.wrappers import DCSendGridWrapper, SendGridAPIError


class Command(BaseCommand):
    def get_unique_mailing_lists(self):
        return (
            SignupQueue.objects.all()
            .filter(added=False)
            .values("mailing_lists")
            .distinct("mailing_lists")
        )

    def get_new_users(self, mailing_lists):
        return (
            SignupQueue.objects.all()
            .filter(
                ~Q(email="testy.mctest@democracyclub.org.uk"),
                added=False,
                mailing_lists=mailing_lists,
            )
            .annotate(email_lower=Func(F("email"), function="lower"))
            .distinct("email_lower")
        )

    def handle(self, *args, **kwargs):
        # Assume we're going to finish sucessfully.
        # If any errors happen, we'll set an error code
        exit_code = 0

        # The easiest way to add new accounts to SendGrid is to batch
        # all of the users who will be added to the same combination
        # of mailing lists in a single API call
        mailing_lists = self.get_unique_mailing_lists()

        sendgrid = DCSendGridWrapper()

        for lsts in mailing_lists:
            # new signups for this combination of mailing lists
            new_users = self.get_new_users(lsts["mailing_lists"])

            # add users to contacts db
            try:
                response = sendgrid.add_users(
                    sendgrid.get_users_payload([user.data for user in new_users])
                )
            except SendGridAPIError:
                continue

            # It is possible some of the emails we've just POSTed worked
            # and some may have failed
            if response["error_count"] > 0:
                # If there were any failures
                # log them and exit with a non-zero status
                # so we know to deal with it
                exit_code = 1
                for error in response["errors"]:
                    self.stderr.write(error["message"])

            # We still need to press on and add the ones that worked
            # to the relevant mailing lists.
            # We'll add any non-failed emails to each list in turn
            for mailing_list in lsts["mailing_lists"]:
                if mailing_list in sendgrid.SENDGRID_LISTS:
                    if response["persisted_recipients"]:
                        sendgrid.add_users_to_lists(
                            response["persisted_recipients"],
                            sendgrid.SENDGRID_LISTS[mailing_list],
                        )
                else:
                    exit_code = 1
                    self.stderr.write("'%s' not found in SENDGRID_LISTS" % mailing_list)

                # have a little rest and make sure we don't hit the rate limits
                time.sleep(1.6)

            # mark all the ones that worked as done
            for i, user in enumerate(new_users):
                if i not in response["error_indices"]:
                    user.added = True
                    user.save()

            # have a little rest and make sure we don't hit the rate limits
            time.sleep(1.6)

        sys.exit(exit_code)
