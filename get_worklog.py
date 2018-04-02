	# This script shows how to connect to a JIRA instance with a
# username and password over HTTP BASIC authentication.

from jira.client import JIRA
import sys,csv
import getpass
import progressbar

if len(sys.argv) < 3:
	print "USAGE: script <output.csv> <username>"
	sys.exit(1)

fname = sys.argv[1]


# By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK.
# See https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details.

options = {
    'server': 'https://contactless.atlassian.net'
}
password = getpass.getpass()
jira = JIRA(options=options, basic_auth=(sys.argv[2], password))    # a username/password tuple

# Get the mutable application properties for this server (requires jira-system-administrators permission)
#~ props = jira.application_properties()


pb_widgets = [progressbar.Percentage(), ' ', progressbar.ETA(), progressbar.Bar(left=" [", right="] "), progressbar.SimpleProgress()]
pb = progressbar.ProgressBar(widgets=pb_widgets, term_width=79).start()


with open(fname, "wt") as csvfile:
	writer = csv.writer(csvfile, delimiter=',',
	                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(["issue_id", "worklog_id", "author", "comment", "created", "started", "seconds"])


	limit = 100
	current_pos = 0

	while True:
		# Find all issues reported by the admin
		issues = jira.search_issues('worklogDate>"-120d"',startAt=current_pos, maxResults=limit)
		#~ issues = jira.search_issues('project=SOFT',maxResults=10000)

		if len(issues) == 0:
			break

		pb.maxval = issues.total

		for i, issue in enumerate(issues):
			for worklog in jira.worklogs(issue):
				row = [issue.id, worklog.id, worklog.author, getattr(worklog, 'comment',''), worklog.created, worklog.started, worklog.timeSpentSeconds]
				row = [unicode(x).encode('utf-8') for x in row]
				# print row
				writer.writerow(row)

			pb.update(current_pos + i)

		current_pos += len(issues)

pb.finish()