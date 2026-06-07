#include <iostream>

using namespace std;

class Node{
    public:
    int data;
    Node*left;
    Node*right;
    Node(int d){
        data=d;
        left=right=nullptr;
    }
};

class tree{
    public:
    Node* root;
    tree(){root = nullptr;}

    Node* insert(Node* t,int data){
        if(t == nullptr){
            Node* newnode=new Node(data);
            t =newnode;
            return t;
        }
        else if(data<t->data){
            t->left=insert(t->left,data);
        }
        else{
            t->right=insert(t->right,data);
        }
        return t;
        }
    void insert(int data){
        root=insert(root,data);
    }

    void display_postorder(Node* temp){
        if(temp==nullptr){return;}
        display_postorder(temp->left);
        display_postorder(temp->right);
        cout<<temp->data<<'\n';

        
    }

};

int main(){
    tree t1;
    t1.insert(45);
    t1.insert(15);
    t1.insert(30);
    t1.insert(49);

    t1.display_postorder(t1.root);


    return 0;
}