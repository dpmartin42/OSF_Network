Creating the OSF Collaborator Network Using Sigma.js
---

Use this repo to clean and create the OSF collaborator network following these steps:

1. Update nodes.json and users.json and place in the OSF_Network folder
2. Run clean_network.py - this file creates the json of nodes and edges
3. Run cleanRawNetwork - this file calculatates node size, edge weight, and coordinates for the layout
4. Run prep_metadata - this file merges user metadata in the clean R network output
5. After this a SimpleHTTPServer should work on index.html inside the network folder
