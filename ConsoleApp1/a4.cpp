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

    // Push (Insert at the top/head)
    void Push(int layerId) {
        Node* newnode = new Node(layerId);
        newnode->next = top;
        top = newnode;
    }

    // Pop (Remove from the top/head)
    int Pop() {
        if (top == nullptr) {
            cout << "Stack is empty! Cannot pop.\n";
            return -1;  // sentinel value
        }

        Node* temp = top;
        top = top->next;
        int value = temp->data;
        delete temp;
        return value;
    }

    // Display
    void Display() {
        if (top == nullptr) {
            cout << "Stack is empty!\n";
            return;
        }

        Node* temp = top;
        cout << "Top -> ";
        while (temp != nullptr) {
            cout << temp->data;
            if (temp->next != nullptr) cout << " -> ";
            temp = temp->next;
        }
        cout << " -> Bottom\n";
    }
};


int main() {
    Stack material;
    cout << "--- Stack Operations (LIFO) ---\n";

    // Push/Add operations
    material.Push(101);
    material.Push(102);
    material.Push(103);

    cout << "After adding Layer 101, 102, 103:\n";
    material.Display();  // Expected: 103 → 102 → 101

    // Pop operations
    cout << "\nRemoving top layer: " << material.Pop() << endl; // 103
    cout << "Removing top layer: " << material.Pop() << endl; // 102

    cout << "\nStack after two removals:\n";
    material.Display(); // Expected: 101

    // Test empty stack condition
    cout << "\nRemoving top layer: " << material.Pop() << endl; // 101
    material.Pop(); // Should print "Stack is empty!"

    return 0;
}
