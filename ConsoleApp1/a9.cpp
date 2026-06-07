/*#include <iostream>

class Node{
    public:
    int data;
    Node* left;
    Node* right;
    Node(int val){
        data=val;
        left=right=nullptr;
    }
};

class bst{
    public:
    Node*root;

    bst(){root=nullptr;}

    Node* insert(Node*temp,int item){
        if(temp==nullptr){
            Node*newnode=new Node(item);
            temp=newnode;
        }
        else if(item<temp->data){
            temp->left=insert(temp->left,item);
        }
        else{
            temp->right=insert(temp->right,item);
        }
        return temp;
    }
    void insert(int item){root=insert(root,item);}

    void preorder(Node*temp){//root,left,right
        if(temp==nullptr)
        return;
        std::cout<<temp->data<<'\t';
        preorder(temp->left);
        preorder(temp->right);

    }

    void inorder(Node*temp){//left,root,right
        if(temp==nullptr){return;}
        inorder(temp->left);
        std::cout<<temp->data<<'\t';
        inorder(temp->right);
    }

    void postorder(Node*temp){//left,right,root
        if(temp==nullptr){return;}
        postorder(temp->left);
        postorder(temp->right);
        std::cout<<temp->data<<'\t';
    }
    Node* search(Node* temp,int key){
        
    }
};

int main(){
    bst tree;
    tree.insert(45);
    tree.insert(15);
    tree.insert(79);
    tree.insert(90);
    tree.insert(10);
    tree.insert(55);
    tree.insert(12);
    tree.insert(20);
    tree.insert(50);

    tree.preorder(tree.root);
    std::cout<<"\n.......................................\n";
    tree.inorder(tree.root);
    std::cout<<"\n.......................................\n";
    tree.postorder(tree.root);
    std::cout<<"\n.......................................\n";

    return 0;
}*/

#include <iostream>


using namespace std;

class priorityqueue{
    private:
    int heap[100];
    int size=0;

    void shiftup(int i){
        while (i>0 && heap[(i-1)/2]<heap[i]){
            swap(heap[i],heap[(i-1)/2]);
            i=(i-1)/2;
        }
    }
};






int main(){

    return 0;
}