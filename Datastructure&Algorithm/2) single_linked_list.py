class Node:
  def __init__(self, data):
    self.data = data
    self.next = None

  def __str__(self):
    return 'Data: ' + str(self.data)

class LinkedList:
  def __init__(self):
    self.head = None
 
  def __str__(self):
    msg = ''
    current_node = self.head
    while current_node is not None:
      msg += str(current_node.data)
      if current_node.next is not None:
        msg += ' -> '
      current_node = current_node.next
    if len(msg) == 0:
      msg = 'Empty linked list'
    return msg

  def insert(self, data):
    new_node = Node(data)
    if self.head is None:
      self.head = new_node
    else:
      last_node = self.head
      while last_node.next is not None:
        last_node = last_node.next
      last_node.next = new_node

  def search(self, target):
    result = None
    current_node = self.head
    while current_node is not None:
      if current_node.data == target:
        result = current_node
        break
      current_node = current_node.next
    return result

  def delete(self, target):
    prev_node = None
    current_node = self.head
    while current_node is not None:
      if current_node.data == target:
        if current_node == self.head:
          self.head = current_node.next
        else:
          prev_node.next = current_node.next
        break
      prev_node = current_node
      current_node = current_node.next

#do test 
linked_list = LinkedList()
linked_list.insert(12)
linked_list.insert(99)
linked_list.insert(37)
linked_list.insert(24)
linked_list.insert(56)
print(linked_list)

result = linked_list.search(24)
print(result)
print(linked_list.search(100))

linked_list.delete(12)
print(linked_list)
linked_list.delete(37)
print(linked_list)
linked_list.delete(56)
print(linked_list)
linked_list.delete(100)
print(linked_list)
