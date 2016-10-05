# This script shows how to connect to a JIRA instance with a
# username and password over HTTP BASIC authentication.

from jira.client import JIRA
import sys,csv

if len(sys.argv) < 4:
	print "USAGE: script <output.csv> <username> <password>"
	sys.exit(1)

fname = sys.argv[1]


# By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK.
# See https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details.

options = {
    'server': 'https://contactless.atlassian.net'
}

jira = JIRA(options=options, basic_auth=(sys.argv[2], sys.argv[3]))    # a username/password tuple

# Get the mutable application properties for this server (requires jira-system-administrators permission)
#~ props = jira.application_properties()

# Find all issues reported by the admin
issues = jira.search_issues('',maxResults=10000)
#~ issues = jira.search_issues('project=SOFT',maxResults=10000)
print len(issues)

with open(fname, "wt") as csvfile:
	writer = csv.writer(csvfile, delimiter=',',
	                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(["issue_id", "worklog_id", "author", "comment", "created", "started", "seconds"])

	for issue in issues:
		for worklog in jira.worklogs(issue):
			row = [issue.id, worklog.id, worklog.author, worklog.comment, worklog.created, worklog.started, worklog.timeSpentSeconds]
			row = [unicode(x).encode('utf-8') for x in row]
			print row
			writer.writerow(row)

