#include <iostream>
#include <string>
#define nullptr NULL
using namespace std;
// Node Structure
class Node {
public:
    int ID, priority;
    Node* next;
    Node(int id, int p) : ID(id), priority(p), next(nullptr) {}
};
// Priority Queue Class
class PriorityQueue {
private:
    Node* head;
public:
    PriorityQueue() : head(nullptr) {}
    // TODO: Destructor to prevent memory leaks
    ~PriorityQueue() {
        while(head!=nullptr){
            Node*temp=head;
            head=head->next;
            delete temp;
        }
    }
    // TODO: YOUR TASK: Insert node in sorted order (Highest to Lowest)
    void push(int id, int p) {
        Node* newnode=new Node(id,p);
        if(head==nullptr||head->priority<p){
            newnode->next=head;
            head=newnode;
            return;
        }
        Node*temp=head;
        while(temp->next!=nullptr&&temp->next->priority<p){
            temp=temp->next;
        }
        newnode->next=temp->next;
        temp->next=newnode;
    }
    // TODO: YOUR TASK: Remove and return the highest priority (from head)
    Node* pop() {
        if(head==nullptr){return nullptr;}
        Node*temp=head;
        head=head->next;
        return temp;

    }
    bool isEmpty() {
        return head == nullptr;
    }
};



int main() {
    PriorityQueue er;
    // Adding patients with different priorities
    // A higher number indicates a more critical condition
    er.push(1, 30);
    er.push(2, 10);
    er.push(3, 100);
    er.push(4, 50);
    er.push(6, 80);
    // After these pushes, the internal linked list should be:
    // [100] -> [80] -> [50] -> [30] -> [10] -> NULL
    cout << "--- Hospital ER: Treating Patients by Priority ---" << endl;
    
    int counter = 1;
    while (!er.isEmpty()) {
        Node* patient = er.pop();
        cout << "Treatment #" << counter << " | Patient Priority: [" << patient->ID << ", "<<'\n' ;
        counter++;
    }
    /* EXPECTED OUTPUT:
       Treatment #1 | Patient Priority: [3, 100]
       Treatment #2 | Patient Priority: [6, 80]
       Treatment #3 | Patient Priority: [4, 50]
       Treatment #4 | Patient Priority: [1, 30]
       Treatment #5 | Patient Priority: [2, 10]
    */
    return 0;
}


/*
        Node* temp=new Node(id,p);
        if(head==nullptr || p>head->priority){
            temp->next=head;
            head=temp;
            return;
        }
        Node*temp1=head;
        while(temp1->next != nullptr && temp1->next->priority>=p){
            temp1=temp1->next;
        }
        temp->next=temp1->next;
        temp1->next=temp;
*/

/*
        if(head==nullptr){return nullptr;}
            Node* temp=head;
            head=head->next;
        return temp; 
*/