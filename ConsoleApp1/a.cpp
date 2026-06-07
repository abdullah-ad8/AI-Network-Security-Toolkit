/*#include <iostream>
using namespace std;



class node{
    public:
    int data;
    node* next;

};
class linkedlist{
    
    public:
    node*head=nullptr;
    void InsertAtEnd(int value){
        node* newnode=new node();
        newnode->data=value;
        newnode->next=nullptr;
        if(head==nullptr){
            head=newnode;
            return;
        }
        node*temp=head;
        while(temp->next!=nullptr){
            temp=temp->next;
        }
        temp->next=newnode;
    }
    node* Search(int value) { 
        node*temp=head;
        while(temp!=nullptr){
            if(temp->data==value){
                return temp;
            }
            temp=temp->next;
        }
        return nullptr;
    } 


    void Display() { // Display the list
        node* temp = head;
        while (temp != nullptr) {
        cout << temp->data << " -> ";
        temp = temp->next;
        }
        cout << "NULL" << endl;
    }
};

int main() {
    linkedlist list;
    list.InsertAtEnd(2);
    list.InsertAtEnd(7);
    list.InsertAtEnd(11);
    list.InsertAtEnd(6);
    list.InsertAtEnd(1);
    cout << "Current List: ";
    list.Display(); // Expected Output: 2 -> 7 -> 11 -> 6 -> 1 -> NULL
    int searchVal = 11;
    node* found = list.Search(searchVal);
    if (found) // Expected Output: 11 found in the list.
    cout << searchVal << " found in the list." << endl;
    else
    cout << searchVal << " is not found." << endl;
    return 0;
}*/
#include <iostream>
using namespace std;

class node{
    public:
    int data;
    node* next;

};
class linkedlist{
    
    public:
    node*head=nullptr;
    void InsertAtEnd(int value){
        node* newnode=new node();
        newnode->data=value;
        newnode->next=nullptr;
        if(head==nullptr){
            head=newnode;
            return;
        }
        node*temp=head;
        while(temp->next!=nullptr){
            temp=temp->next;
        }
        temp->next=newnode;
    }


    void insertbefore(int value,int adding){
        node*temp=head;
        while(temp!=nullptr&&temp->next->data!=value){
            temp=temp->next;
        }
            node*temp1=temp->next;
            temp->next->data=adding;
        while(temp!=nullptr){
            temp=temp->next;
            temp->next=temp1;
            temp=temp->next;
            temp1=temp->next;

        }

    }


    void Display() { // Display the list
        node* temp = head;
        while (temp != nullptr) {
        cout << temp->data << " -> ";
        temp = temp->next;
        }
        cout << "NULL" << endl;
    }
};

int main() {
    linkedlist list;
    list.InsertAtEnd(2);
    list.InsertAtEnd(7);
    list.InsertAtEnd(11);
    list.InsertAtEnd(6);
    list.InsertAtEnd(1);
    list.InsertAtEnd(5);
    list.insertbefore(1,66);
    cout << "Current List: ";
    list.Display(); // Expected Output: 2 -> 7 -> 11 -> 6 -> 1 -> NULL

    return 0;
}