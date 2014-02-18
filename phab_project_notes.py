#!/usr/bin/env python

import sys

from phabricator import Phabricator

if len(sys.argv) == 1:
    print "Syntax: %s ProjectName" % sys.argv[0]
    sys.exit(1)

project_name = sys.argv[1]

phab = Phabricator()
phab.update_interfaces()
proj = phab.project


def phid_from_name(name):
    all_projects = proj.query()

    for phid in all_projects:
        if all_projects[phid]['name'] == name:
            return phid

projectPHID = phid_from_name(project_name)
tasks = phab.maniphest.find(
    projectPHIDs=[projectPHID],
)

print "Project %s" % project_name


# Currently unused, exists for reference
status = {
    '0': 'any',
    '1': 'open',
    '2': 'closed',
    '3': 'resolved',
    '4': 'wontfix',
    '5': 'invalid',
    '6': 'spite',
    '7': 'duplicate',
}


for task in tasks:
    # Include non-open tasks
    # "any" appears to also contain open tasks :(
    if tasks[task]['status'] in ['0', '2', '3']:
        print "P:%s %s %s" % (
            tasks[task]['priority'],
            tasks[task]['title'],
            tasks[task]['uri'],
        )
