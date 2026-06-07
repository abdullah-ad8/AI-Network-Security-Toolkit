#include <iostream>


 #include <iostream>
 using namespace std;
 #define nullptr NULL
 class Node {                        // Node class for Doubly Linked List
 public:
    int data;
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
    void InsertAtEnd(int value) {
        Node* newNode = new Node(value);
        if (head == nullptr) {      // If the head is empty, then it fill the head.
            head = newNode;
            return;
        }
                                    
        Node* temp = head;
 while (temp->next != nullptr)   // Traverse to the end of the list
            temp = temp->next;
        temp->next = newNode;       // It will add the new node at the end of the list.
        newNode->previous = temp;   // Set the previous pointer of the new node
    }
 public:
 LinkedList() {                  // Constructor to initialize the linked list with so
        head = nullptr;
        int values[] = {2, 7, 11, 6, 1, 22, 39, 3};
        for (int i = 0; i < 8; i++)
            InsertAtEnd(values[i]);
    }
 ~LinkedList() {                 // Destructor to free memory
        Node* current = head;
        while (current != nullptr) {
            Node* temp = current;
            current = current->next;
            delete temp;
        }
    }
        Node* Search(int value) { 
        Node*temp=head;
        while(temp!=nullptr){
            if(temp->data==value){
                return temp;
            }
            temp=temp->next;
        }
        return nullptr;
        }     //TODO: Implement Search function


        /*bool Delete(int value) {
            Node*temp=head;
        while(temp!=nullptr){
            if(value==head->data){
               head=head->next;
               delete head->previous;
               head->previous=nullptr;
               return true;          
            }
         else if(temp->data==value){
                temp->previous->next=temp->next;
                return true;
            }
            temp=temp->next;
        }
        return false;        

         }  */    //TODO: Implement Delete function

        bool Delete(int value) { 
            Node*temp=Search(value);
            Node*temp1=head;
               if(temp==head){
                head=head->next;
                delete temp1;
                temp1=nullptr;
               return true;
                }
               else {
                temp->previous->next=temp->next;
                return true;
                }
            
            return false;
        
         } 
        



 void Display() {                // Display the list
        Node* temp = head;
        while (temp != nullptr) {
            cout << temp->data << " -> ";
            temp = temp->next;
        }
        cout << "NULL" << endl;
    }
 };

 int main() {
    LinkedList list;
 int deleteVal = 1;
 if (list.Delete(deleteVal))     // Expected Output: Number 1 is deleted from the lis
        cout << "Number " << deleteVal << " is deleted from the list." << endl;
    else
        cout << "Number " << deleteVal << " is deleted from the list." << endl;
    cout << "Current List: ";
 list.Display();                 // Expected Output: 2 -> 7 -> 11 -> 6 -> 22 -> 39 ->
    return 0;
 }