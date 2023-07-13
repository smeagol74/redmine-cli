import shutil
from collections import defaultdict
from datetime import datetime
from textwrap import wrap

from redmine.journal import Journal
import click


class Issue:
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get("id")
        self.subject = kwargs.get("subject")
        self.tracker = kwargs.get("tracker")
        self.project = kwargs.get("project")
        self.status = kwargs.get("status")
        self.priority = kwargs.get("priority")
        self.author = kwargs.get("author")
        self.assigned_to = kwargs.get("assigned_to", defaultdict(str))
        self.done = kwargs.get("done")
        self.start_date = kwargs.get("start_date")
        self.due_date = kwargs.get("due_date")
        self.created_on = kwargs.get("created_on")
        self.description = kwargs.get("description", "")
        self.journals = kwargs.get("journals")
        self.done_ratio = kwargs.get("done_ratio")
        self.statuses = kwargs.get("statuses")
        self.priorities = kwargs.get("priorities")
        self.users = kwargs.get("users")

    def __repr__(self):
        return f"Issue({self.id}, {self.subject})"

    def __str__(self):
        issue = self.get_header()

        if self.journals:
            issue += self.get_journals()

        return issue

    def get_header(self):
        header = f"Issue #{self.id} - {self.subject}\n\n"

        created_on = datetime.fromisoformat(self.created_on)
        header += (
            f"Reported by {self.author['name']} on "
            f"{created_on.date()} {created_on.time()}\n\n"
        )

        header += f"Project: {self.project['name']}\n"
        header += f"Tracker: {self.tracker['name']}\n"
        header += f"Status: {self.status['name']}\n"
        header += f"Priority: {self.priority['name']}\n"

        if self.assigned_to is not None:
            header += f"Assigned to: {self.assigned_to['name']}\n"
        if self.start_date is not None:
            header += f"Start date: {self.start_date}\n"
        if self.due_date is not None:
            header += f"Due date: {self.due_date}\n"
        if self.done is not None:
            header += f"Done: {self.done}\n"

        if self.description is not None:
            description = wrap(self.description, width=79)
            header += "\n"
            for d in description:
                header += f"{d}\n"

        return header

    def get_journals(self):
        journals = ""
        for journal in self.journals:
            journals += str(
                Journal(
                    **journal,
                    statuses=self.statuses,
                    priorities=self.priorities,
                    users=self.users,
                )
            )

        return journals

    def as_row(self, show_assignee=False, show_project=True, show_priority=False, show_status=False, show_done_ratio=False, width=None):
        row = click.style(f"{self.id:>6} ", fg='green')
        l = width if width else shutil.get_terminal_size()[0]
        if show_project:
            row += f"{self.project['name']:21.20} "
            l -= 23
        if show_priority:
            row += f"{self.priority['name']:<8} "
            l -= 9
        if show_status:
            row += f"{self.status['name']:<19} "
            l -= 20
        if show_done_ratio:
            row += f"{self.done_ratio:>3}% "
            l -= 5
        if show_assignee:
            row += f"{self.assigned_to['name']:<21} "
            l -= 22
        l -= 6
        row += f"{self.subject:<{l}.{l}}"

        return row


class IssueStatus:
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")

    def __str__(self):
        return f"{self.id:<3} {self.name}"
