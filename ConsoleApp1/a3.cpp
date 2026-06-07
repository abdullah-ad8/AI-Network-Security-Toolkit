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
    }
    // TODO: Implement Pop (Remove from the top/head)
    int Pop() {
            if (top == nullptr) {
            cout << "Stack is empty! Cannot pop.\n";
            return -1;  // sentinel value
        }
        Node*temp=top;
        top=top->next;
        int tt=temp->data;
        delete temp;
        return tt;

        // LIFO: Remove the node from the beginning of the list (old top)
    }
    // TODO: Implement Display
    void Display() {
        Node*temp=top;
        while(temp!=nullptr){
            cout<<temp->data;
            temp=temp->next;
        }

        // Print layers from top to bottom
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
        Node*newnode=new Node(customerId);
        if (front == nullptr) {
            front=newnode;
            return;
        }
        Node*temp=front;
        while(temp->next!=nullptr){
            temp=temp->next;
        }
        temp->next=newnode;
        newnode->next=nullptr;

        // FIFO: Add a new node at the end of the list (new rear)
    }
    // TODO: Implement Dequeue (Remove from the front/head)
    int Dequeue() {
        if (front == nullptr) {
            cout << "queue is empty! Cannot pop.\n";
            return -1;  // sentinel value
        }
        Node*temp=front;   
        front = front->next;
        int value=temp->data;
        delete temp;
        return value;
        
        // FIFO: Remove the node from the beginning of the list (old front)
    }
    // TODO: Implement Display
    void Display() {
        Node*temp=front;
        while(temp!=nullptr){
            cout<<temp->data<<endl;
            temp=temp->next;
        }

        // Print customers from front to back
    }
 };




int main() {
    Queue marketLine;
    cout << "--- Queue Operations (FIFO) ---\n";
    // Enqueue/Add operations
    marketLine.Enqueue(501); // Customer A
    marketLine.Enqueue(502); // Customer B (joins after A)
    marketLine.Enqueue(503); // Customer C (joins after B)
    cout << "After customers 501, 502, 503 joined the line:\n";
    marketLine.Display(); // Expected: Front -> 501, 502, 503 <- Back
    cout << "\nQueue after two transactions:\n";
    marketLine.Display(); // Expected: Front -> 503 <- Back
    
    // Dequeue/Finish transaction operation
    cout << "\nFinished transaction for customer: " << marketLine.Dequeue() << endl; //
    cout << "Finished transaction for customer: " << marketLine.Dequeue() << endl; // E
    // Test empty queue condition
    cout << "\nFinished transaction for customer: " << marketLine.Dequeue() << endl; //
    // The next dequeue should handle the empty queue case
    // (e.g., return a sentinel value like -1 or print "Queue is Empty")
    marketLine.Dequeue();
    return 0;
}





