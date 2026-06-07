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
        Node*temp1=new Node(value);
        if(head==nullptr){
            head=temp1;
            return;
        }
        Node*temp=head;
        while(temp->next!=nullptr){
            temp=temp->next;
        }
        temp->next=temp1;
        temp->next->next=nullptr;



    }     // TODO: Implement this function
    Node* Search(int value) {
        Node*temp=head;
        while(temp->next != nullptr){
            if(temp->data==value){
                return temp;
                break;
            }
            temp=temp->next;
        }
        return nullptr; 
     }         // TODO: Implement this function
    void InsertSorted(int value) {
        Node*newnode=new Node(value);

        if(head==nullptr|| value<head->data){
            newnode->next=head;
            head=newnode;
            return;
        }

        Node*temp=head;
        while(temp->next != nullptr&& temp->next->data< value){
            temp=temp->next;
        }

        newnode->next=temp->next;
        temp->next=newnode;
        
     }    // TODO: Implement this function
     
    void Display() {                    // Display the list
        Node* temp = head;
        while (temp != nullptr) {
            cout << temp->data << " -> ";
            temp = temp->next;
        }
        cout << "NULL" << endl;
    }
};

int main() {
    LinkedList list2;
    list2.InsertSorted(10);
    list2.InsertSorted(5);
    list2.InsertSorted(15);
    list2.InsertSorted(12);
    list2.InsertSorted(3);

    cout << "Current List: ";
list2.Display();                // Expected Output: 3 -> 5 -> 10 -> 12 -> 15 -> NULL
    return 0;
}