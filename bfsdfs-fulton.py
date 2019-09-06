"""

  Ethan Fulton
  CSC 463
  HW1 - DFS, BFS

"""

import pandas as pd
import queue

def main():
  file_name = input("Please enter the filename and extension ('Enter' for default): ")
  if(file_name == ""):
    file_name = "BFS_DFS.csv"

  bad_input = True
  graph = pd.read_csv(file_name)
  graph = graph.fillna(0)
  num_nodes = len(graph.index)
  start_message = "Enter start node (1 - " + str(num_nodes) + "): "
  end_message = "Enter an end node (1 - " + str(num_nodes) + "): "
  show_steps_message = "Show steps of traversal? (y/n) "
  start_node = 0
  end_node = 0

  while bad_input:
    start_node = int(input(start_message))
    if start_node >= 1 and start_node <= num_nodes:
      bad_input = False
  bad_input = True
  while bad_input:
    end_node = int(input(end_message))
    if end_node >= 1 and end_node <= num_nodes:
      bad_input = False
  bad_input = True
  while bad_input:
    show_steps = input(show_steps_message)
    if show_steps == "y" or show_steps == "Y" or show_steps == "Yes" or show_steps == "yes":
      show_steps = True
      bad_input = False
    elif show_steps == "n" or show_steps == "N" or show_steps == "No" or show_steps == "no":
      show_steps = False
      bad_input = False
    else: show_steps = input(show_steps_message)

  bfs_result = bfs(graph, start_node, end_node, show_steps)
  if bfs_result[0] == True:
    print("BFS path:")
    print(*bfs_result[1], sep=" - ")
  else: print("No BFS path found")

  dfs_results = dfs(graph, start_node, end_node, show_steps)
  if dfs_results[0] == True:
    print("DFS path:")
    print(*dfs_results[1], sep = " - ")
  else: print ("No DFS path found")

"""

  build a list that contains the path in the given graph from start node to
  end node

"""
def build_path(graph, start_node, end_node):
  path = [end_node]
  j = end_node - 1
  while j != start_node - 1:
    path.append(graph.loc[j, "Parent"] + 1)
    j = graph.loc[j, "Parent"]
  path.reverse()
  return path

"""

  Perform a Breadth-First Search on the given graph and
  return a list of two items, the first is a boolean that is true if a path was
  found and the second is another list that contains the found path

"""
def bfs(g, start_node, end_node, show_steps):
  path_exisits = False
  graph = g.copy()
  graph.insert(len(graph.columns), "Viewed", False)
  graph.insert(len(graph.columns), "Parent", 0)

  q = queue.Queue()
  q.put(start_node)
  graph.loc[start_node - 1, "Viewed"] = True

  while q.empty() == False:
    current_node = q.get() - 1
    i = 1
    while graph.iloc[current_node, i] != 0:
      if graph.loc[graph.iloc[current_node, i]-1, "Viewed"] == False:
        if show_steps == True:
          print("Checking node ", graph.iloc[current_node, i])
        graph.loc[graph.iloc[current_node, i]-1, "Viewed"] = True
        graph.loc[graph.iloc[current_node, i]-1, "Parent"] = current_node
        q.put(int(graph.iloc[current_node, i]))
        if graph.iloc[current_node, i] == end_node:
          q.queue.clear()
          path_exists = True
          break
      i += 1

  path = build_path(graph, start_node, end_node)
  return [path_exists, path]


"""

  Perform an Iterative Depth-First Search on the given graph and
  return a list of two items, the first is a boolean that is true if a path was
  found and the second is another list that contains the found path

"""
def dfs(g, start_node, end_node, show_steps):
  path_exists = False
  graph = g.copy()
  graph.insert(len(graph.columns), "Viewed", False)
  graph.insert(len(graph.columns), "Parent", 0)
  s = [start_node]
  graph.loc[start_node - 1, "Viewed"] = True

  while s:
    current_node = s[-1] - 1
    del s[-1]
    if show_steps == True:
      print("checking node ", current_node + 1)
    if current_node + 1 == end_node:
      path_exists = True
      break
    i = 1
    while graph.iloc[current_node, i] != 0:
      if graph.loc[graph.iloc[current_node, i]-1, "Viewed"] == False:
        graph.loc[graph.iloc[current_node, i]-1, "Viewed"] = True
        graph.loc[graph.iloc[current_node, i]-1, "Parent"] = current_node
        s.append(int(graph.iloc[current_node, i]))
      i += 1
  path = build_path(graph, start_node, end_node)
  return [path_exists, path]

main()
