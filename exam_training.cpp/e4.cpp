#include <iostream>
using namespace std;
class Node {
public:
    int data;
    Node* next;
    Node(int val) {
        data = val;
        next = nullptr;
    }
};
class LinkedList {
private:
    Node* head;
public:
    LinkedList() : head(nullptr) {}
    ~LinkedList() {
        Node* current = head;
        while (current != nullptr) {
            Node* temp = current;
            current = current->next;
            delete temp;
        }
    }
    void InsertAtEnd(int value) {
        Node* newNode = new Node(value);
        if (head == nullptr) {
            head = newNode;
            return;
        }
        Node* current = head;
        while (current->next != nullptr) {
            current = current->next;
        }
        current->next = newNode;
    }
    class Iterator { 
    private:
        Node* current;
    public:
        Iterator(Node* p) : current(p) {}
        // TODO: Deferencing Operator (Data Access)
        int& operator*() { 
            return current->data;
         }
        // TODO: Prefix Increment Operator (Traversal)
        Iterator& operator++() { 
            if(current!=nullptr){current=current->next;}
            return *this;
         }
        // TODO: Equality Operator (Comparison)
        bool operator==(const Iterator& other) const { 
            if(*this==other){
                return true;
            }
            return false;
         }
        // TODO: Inequality Operator (Comparison)
        bool operator!=(const Iterator& other) const { 
            if(*this!=other){
                return true;
            }
            return false;
         }
    };
    
    // TASK: Implement begin() and end() methods.
    Iterator begin() { return Iterator(head); }
    Iterator end() { return Iterator(nullptr); }
};


int main() {
    LinkedList list;
    
    // Insert Data
    list.InsertAtEnd(10);
    list.InsertAtEnd(20);
    list.InsertAtEnd(30);
    list.InsertAtEnd(40);
    cout << "Iterating through the list using the custom Iterator:" << endl;
    
    // Test 1: Traversal
    for (LinkedList::Iterator it = list.begin(); it != list.end(); ++it) {
        cout << *it << " "; 
    }
    cout << endl; // Expected Output: 10 20 30 40 
    // Test 2: Data modification (via reference returned by operator*)
    LinkedList::Iterator secondNode = list.begin();
    ++secondNode; 
    
    cout << "Original second element: " << *secondNode << endl; // Expected: 20
    
    *secondNode = 25; // Modify value
    
    cout << "Updated list: ";
    for (LinkedList::Iterator it = list.begin(); it != list.end(); ++it) {
        cout << *it << " "; 
    }
    cout << endl; // Expected Output: 10 25 30 40 
    return 0;
}