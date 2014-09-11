# Read in the user (Person name and id) and node (contributions) data

import json

with open('users.json', 'r') as f:
    db_users = json.load(f)
with open('nodes.json', 'r') as f:
    db_components = json.load(f)

import itertools as iter

# Collapse user information

people_dict = []

for user in db_users:
    people_dict.append({k: user[k] for k in ('fullname', '_id')})

for people in people_dict:
    people['group'] = 1

# Extract only projects that are registered, not deleted, public, and not a registration

project_total = []

for project in db_components:
    if project['category'] == 'project' and project['is_deleted'] == False and project['is_public'] == True and project['is_registration'] == False:
        project_total.append(project)

# Save only the relevant information (contributors, project id)

project_dict = []

for project in project_total:
    project_dict.append({k: project[k] for k in ('contributors', '_id', 'title')})

# Aggregate each large project as a single node based on project_size_cutoff

project_size_cutoff = 8

# If users are part of smaller projects, keep them as contributors on larger projects
# If they have only done large projects, then they are deleted

# Create a label for projects indicating if they are big or small

for project in project_dict:
    if len(project['contributors']) >= 8:
        project['project_size'] = 'big'
    else:
        project['project_size'] = 'small'

# Loop through and create a count of projects a user has participated in,
# where the number of fellow contributors are less than project_size_cutoff

for people in people_dict:
    people['num_small_cont'] = sum(
        1 for d in project_dict if len(d.get('contributors')) <= 8 and people['_id'] in d.get('contributors'))

# Looks like it worked but there are some errors upon an initial check. Wonder why...

# Get list of user ids to be removed

to_delete = []

for person in people_dict:
    if person['num_small_cont'] < 4:
        to_delete.append(person['_id'])

# Remove the to_delete ids from the contributor lists in projects

for project in project_dict:
    project['contributors'] = [x for x in project['contributors'] if x not in to_delete]

# Remove the to_delete ids from the user file

people_dict[:] = [d for d in people_dict if d.get('_id') not in to_delete]

# Add the big project contributor id to itself

for project in project_dict:
    if project['project_size'] == 'big':
        project['contributors'].append(project['_id'])

# Save clean project file for meta data

with open('clean_project.json', 'w') as f:
    json.dump(project_dict, f, indent = 4)

# Add the 'big' project ids to the user file
# fullname is title, _id is the id, and num_small_cont is 1

for project in project_dict:
    if project['project_size'] == 'big':
        new_dict = {'fullname': project['title'], '_id': project['_id'], 'num_small_cont':1, 'group':2}
        people_dict.append(new_dict)

# merge id number and translate into source and target (using numeric identifier string)

total_cont = []

for project in project_dict:

    links = []

    for people in people_dict:
        if people['_id'] in project['contributors']:
            links.append(people['_id'])

    total_cont.append(links)

# Create combinations of links for the json data set

id_cont = []

for cont_list in total_cont:
    if len(cont_list) > 1:
        id_cont.extend(list(iter.combinations(cont_list, 2)))

# Convert list of combination of links to dictionary format with from, to, and weight: 1

total_links = []

for link in id_cont:
    total_links.append({'source': link[0], 'target': link[1], 'size': 1})

# add an identifier string for each link  (i.e., "0", "1")

# make minor changes to create a json file of nodes and edges for network cleaning

for people in people_dict:
    people.pop('num_small_cont')
    people['id'] = people.pop('_id')
    people['label'] = people.pop('fullname')

output = {'nodes': people_dict, 'edges': total_links}

with open('clean_network.json', 'w') as f:
    json.dump(output, f, indent = 4)
