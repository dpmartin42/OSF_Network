# Read in the cleaned data set and the project data set
import json

with open('clean_network.json', 'r') as f:
    clean_network = json.load(f)

nodes = clean_network['nodes']
edges = clean_network['edges']

# Need to get the names of all collaborators of the users

for the_node in nodes:

    single_collab = []

    for the_edge in edges:

        if the_node['id'] in the_edge['source']:
            single_collab.append(the_edge['target'])

        if the_node['id'] in the_edge['target']:
            single_collab.append(the_edge['source'])

    the_node['collab_id'] = single_collab

# Remove ids of project nodes as collaborators

project_people = []

for the_node in nodes:
    if the_node['group'] == 2:
        project_people.append(the_node['id'])

for the_node in nodes:

    for the_collab in the_node['collab_id']:
        if the_collab in project_people:
            the_node['collab_id'].remove(the_collab)

# Order the collaborators by number of projects and then remove duplicates

for the_node in nodes:

    d = {}
    for i in the_node['collab_id']:
        d[i] = d.get(i, 0) + 1
    the_node['collab_id'] = sorted(d, key=d.get, reverse=True)

# Record the collaborator name in the same order as their id

for the_node in nodes:

    the_node['collab_name'] = []
    the_node['project_name'] = []
    the_node['project_id'] = []

    for the_collab in the_node['collab_id']:

        for the_match in nodes:

            if(the_match['id'] == the_collab):
                the_node['collab_name'].append(the_match['label'])

# Need to get the names of all projects

with open('clean_project.json', 'r') as f:
    projects = json.load(f)

for the_project in projects:

    for the_node in nodes:
        if the_node['id'] in the_project['contributors']:
            the_node['project_name'].append(the_project['title'])
            the_node['project_id'].append(the_project['_id'])

# Add metadata to the nodes component after network calculations (need to do this for both!)

with open('Network/data/osfData.json', 'r') as f:
    the_network = json.load(f)

for the_user in the_network['nodes']:

    for the_match in nodes:

        if the_user['id'] == the_match['id']:
            the_user['collab_name'] = the_match['collab_name']
            the_user['project_name'] = the_match['project_name']
            the_user['group'] = the_match['group']
            the_user['collab_id'] = the_match['collab_id']
            the_user['project_id'] = the_match['project_id']

with open('clean_network_with_metadata.json', 'w') as f:
    json.dump(the_network, f, indent = 4)
