#include <iostream>
using namespace std;
// Node structure for the linked list implementation
class Node {
public:
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};
// === Part 1: Stack Class Implementation (LIFO) ===
class Stack {
private:
    Node* top; // Pointer to the top of the stack
public:
    Stack() : top(nullptr) {} // Constructor
    // Destructor to free memory
    ~Stack() {
        Node* current = top;
        while (current != nullptr) {
            Node* temp = current;
            current = current->next;
            delete temp;
        }
    }
    // TODO: Implement Push (Insert at the top/head)
    void Push(int layerId) {
        Node*newnode=new Node(layerId);
            newnode->next=top;
            top=newnode;
        
        // LIFO: Add a new node at the beginning of the list (new top)
        // ...
    }
    // TODO: Implement Pop (Remove from the top/head)
    int Pop() {
        Node*temp=top;
        if(top==nullptr){return -1;}
        int a=temp->data;
        top=top->next;
        delete temp;
        return a;

        // LIFO: Remove the node from the beginning of the list (old top)
        // ...
    }
    // TODO: Implement Display
    void Display() {
        Node*temp=top;
        while(temp != nullptr){
            cout<<temp->data<<" -> ";
            temp=temp->next;
        }
        cout<<"NULL";
        // Print layers from top to bottom
        // ...
    }
};
// === Part 2: Queue Class Implementation (FIFO) ===
class Queue {
private:
    Node* front; // Pointer to the front of the line (Dequeue)
    Node* rear;  // Pointer to the back of the line (Enqueue)
public:
    Queue() : front(nullptr), rear(nullptr) {} // Constructor
    // Destructor to free memory
    ~Queue() {
        Node* current = front;
        while (current != nullptr) {
            Node* temp = current;
            current = current->next;
            delete temp;
        }
    }
    // TODO: Implement Enqueue (Insert at the rear/tail)
    void Enqueue(int customerId) {
        Node* newnode= new Node(customerId);
        if(rear==nullptr){
            front=rear=newnode;
        }
        else{
            rear->next=newnode;
            rear=newnode;
        }

        // FIFO: Add a new node at the end of the list (new rear)
        // ...
    }
    // TODO: Implement Dequeue (Remove from the front/head)
    int Dequeue() {
        if(front==nullptr){return -1;}
        Node*temp=front;
        int d=temp->data;
        front=front->next;
        if(front== nullptr){
            rear=nullptr;
        }
        delete temp;
        return d;
        
        // FIFO: Remove the node from the beginning of the list (old front)
        // ...
    }
    // TODO: Implement Display
    void Display() {
        Node* temp=front;
        while(temp!=nullptr){
            cout<<temp->data<< " -> ";
            temp=temp->next;
        }
        cout<<"NULL";
        // Print customers from front to back
        // ...
    }
};
int main() {
    Queue marketLine;
    cout << "--- Queue Operations (FIFO) ---\n";

    // Enqueue/Add operations
    marketLine.Enqueue(501); 
    marketLine.Enqueue(502); 
    marketLine.Enqueue(503); 
    
    cout << "After customers 501, 502, 503 joined the line:\n";
    marketLine.Display(); 

    // Dequeue operations
    cout << "\nFinished transaction for customer: " << marketLine.Dequeue() << endl; 
    cout << "Queue after one transaction:\n";
    marketLine.Display(); 

    cout << "\nFinished transaction for customer: " << marketLine.Dequeue() << endl; 
    
    // Empty the queue
    cout << "Finished transaction for customer: " << marketLine.Dequeue() << endl; 

    // Test empty queue condition
    cout << "\nAttempting to dequeue from empty queue: " << marketLine.Dequeue() << endl; 

    return 0;
}