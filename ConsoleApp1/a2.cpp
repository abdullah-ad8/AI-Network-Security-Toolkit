 #include <iostream>
 using namespace std;
 class Node {                        
public:
 int data;
 // Node class for Doubly Linked List
    Node* next;
    Node* previous;
    Node(int val) {                 // Constructor to initialize a new node
        data = val;
        next = nullptr;
        previous = nullptr;
    }
 };
 class LinkedList {                  // Class for Doubly Linked List
 private:
    Node* head;
 public:
 LinkedList() { head = nullptr; } // Constructor to initialize an empty list
 ~LinkedList() {                 // Destructor to free memory
        Node* current = head;
        while (current != nullptr) {
            Node* temp = current;
            current = current->next;
            delete temp;
        }
    }
        void InsertAtEnd(int value) {
            Node*newnode=new Node(value);
            if(head==nullptr){
                head=newnode;
                return;
            }
            Node*temp=head;
            while(temp -> next!=nullptr){
                temp=temp->next;
            }
            temp->next=newnode;
            newnode->previous = temp;
            
         }     // TODO: Implement this function
 void Display() {                    // Display the list
        Node*temp = head;
        while (temp != nullptr) {
            cout << temp->data << " -> ";
            temp = temp->next;
        }
        cout << "NULL" << endl;
    }
 };

  int main() {
    LinkedList list;
    list.InsertAtEnd(2);
    list.InsertAtEnd(7);
    list.InsertAtEnd(11);
    list.InsertAtEnd(6);
    list.InsertAtEnd(1);
    cout << "Current List: ";
list.Display();                 // Expected Output: 2 -> 7 -> 11 -> 6 -> 1 -> NULL
    return 0;
 }