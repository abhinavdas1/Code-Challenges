import requests
from collections import defaultdict, deque, Counter
# I was not sure what the question meant by the most common Node 
# so I have tracked two things based on my understanding 
# The Node with the most children. (If multiple we get the closest one to the root)
# The node which appears the most on the graph
# IMPORTANT  - Also we do not need to store the graph locally for the solutions here 
# I did that to showcase how that functionality would work.
class Solution:
	graph = defaultdict(set)
	# We have been provided a starting Node for this exercise
	startingNodeID = "089ef556-dfff-4ff2-9733-654645be56fe"
	counter = Counter()
	totalNodes = 0

	# Constructor: Will traverse and form the graph locally
	def __init__(self):
		self.traverse()

	# For making the API request to fetch Node data 
	def getNode(self, nodeID: str):
		x = requests.get('https://nodes-on-nodes-challenge.herokuapp.com/nodes/' + nodeID)
		return x.json()[0]

	def traverse(self):
		# We will traverse in a BFS fashion using a q to iterate over Nodes
		# To mark already traversed nodes we will maintain a visited set
		# We will be utilizing the total elements in the visited set to get 
		# the total number of sets 
		q = deque()
		visited = set()
		q.append(self.startingNodeID)
		self.counter[self.startingNodeID] += 1

		# To track node with max Child Nodes
		maxChildren = 0


		# We keep traversing till we have no new nodes to traverse which means 
		# nothing left in the queue
		while len(q) >  0:
			currentNodeID = q.popleft()
			nodeVal = self.getNode(currentNodeID)
			visited.add(currentNodeID)


			# Track number of kids to get the Node with max Child Nodes
			if len(nodeVal["child_node_ids"]) > maxChildren:
				maxChildren = len(nodeVal["child_node_ids"])
				self.NodeWithMaxChildren = currentNodeID

			# traverse the child nodes and add to the queue if not 
			# visited before. 
			for childNodeID in nodeVal["child_node_ids"]:
				# Update counter to keep track of most common node
				self.counter[childNodeID] += 1
				# Update the Graph
				self.graph[currentNodeID].add(childNodeID)
				if childNodeID not in visited:
					q.append(childNodeID)

		# Update the total nodes in the 
		self.totalNodes = len(visited)


	def getTotalNodes(self):
		return self.totalNodes

	# For getting the most common Node ID 
	# I have looked at the number of times the node has appeared
	# within the child nodes. 
	def getMostCommonNodeID(self):
		return self.counter.most_common(1)


	def getNodeWithMaxChildren(self):
		return self.NodeWithMaxChildren



if __name__ == "__main__":
	sol = Solution()
	print("Total Nodes in the Graph: ", sol.getTotalNodes())
	print("Most Common Node ID: ", sol.getMostCommonNodeID())
	print("Node with Most Children: ", sol.getNodeWithMaxChildren())