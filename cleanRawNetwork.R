####################
# Dan Martin
# Get Network Information
####################

rm(list = ls())

# set working directory here

require(igraph)
require(jsonlite)

myData <- fromJSON("clean_network.json")

# Encode accents and gsub some numbers

Encoding(myData$nodes$label) <- "latin1"

myData$nodes$label <- gsub("\024|\034|\035", "", myData$nodes$label)
myData$nodes$label <- gsub(":", "-", myData$nodes$label)

# Add an hacek to Stephan's name

myData$nodes$label <- gsub("`t\033", "Ště", myData$nodes$label)

# Remove single nodes

myData$nodes <- myData$nodes[myData$nodes$id %in% myData$edges$source | myData$nodes$id %in% myData$edges$target, ]

myNet <- graph.data.frame(myData$edges[, c("source", "target")], directed = FALSE)

# Add size to nodes using betweenness centrality

nodeSize <- data.frame(id = names(betweenness(myNet)), size = betweenness(myNet)^(1/2), stringsAsFactors = FALSE)
myData$nodes <- merge(myData$nodes, nodeSize, by = "id")

##############################
# Calculate communities using 
# the fast greedy algorithm
# in igraph

# Remove multiple edges and combine for weights

E(myNet)$weight <- 1

myNet <- simplify(myNet, edge.attr.comb = list(weight = "sum"))

# groups <- fastgreedy.community(myNet)

forceLayout <- layout.fruchterman.reingold(myNet)

# heights, circle, fruchmin reingold
# add in options, and the default. Then I can just override them with whatever is chosen

plot(myNet, vertex.size=5, vertex.label=NA,layout=forceLayout)

myData$nodes$x <- forceLayout[, 1]
myData$nodes$y <- forceLayout[, 2]

# plot(myNet, layout = forceLayout)

myData$edges <- get.data.frame(myNet)
myData$edges$weight <- myData$edges$weight^(1/2)

################
# Fix structure 
# for sigma.js

# Add string id to edges
names(myData$edges) <- c("source", "target", "size")
myData$edges$id <- as.character(0:(nrow(myData$edges) - 1))
myData$edges <- myData$edges[, c("id", "source", "target", "size")]

# Make all people dark blue (#013567) and all projects light blue (#669ACC)

myData$nodes$color <- NA

myData$nodes[myData$nodes$group == 1, ]$color <- '#013567'
myData$nodes[myData$nodes$group == 2, ]$color <- '#669ACC'

myData$edges$color <- '#666666'

# Add original cluster colors

myData$nodes$originalColor <- myData$nodes$color
myData$edges$originalColor <- myData$edges$color

# Save names for search capabilities in json

write(toJSON(myData$nodes$label, pretty = TRUE),
append = FALSE,
file = "Network/data/osfNames.json")

# Save as a new json file

write(toJSON(myData, pretty = TRUE),
append = FALSE,
file = "Network/data/osfData.json")




