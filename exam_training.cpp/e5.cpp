#include <iostream>
#include <string>
#define nullptr NULL  // For compatibility with older C++ standards
using namespace std;
class TreeNode {
public:
    string value;
    TreeNode* left;
    TreeNode* right;
    TreeNode(string val) : value(val), left(nullptr), right(nullptr) {}
};
class ExpressionTree {
private:
    TreeNode* root;
    // TODO: YOUR TASK: RECURSIVE DELETE METHOD
    void deleteTree(TreeNode* node) {
        if (node == nullptr) { return;}
        deleteTree(node->left);
        deleteTree(node->right);
        delete node;
    }

    // TODO: YOUR TASK: RECURSIVE EVALUATION METHOD
    double evaluateRecursive(TreeNode* node) {
        if(node==nullptr){return -1;}

        if(node->left==nullptr && node->right==nullptr){
            return stod(node->value);
        }
        double left=evaluateRecursive(node->left);
        double right=evaluateRecursive(node->right);
        if(node->value=="*"){return left*right;}
        if(node->value=="+"){return left+right;}

    }
   
public:
    ExpressionTree() : root(nullptr) {}
    // Destructor
    ~ExpressionTree() {
        deleteTree(root);
    }
    
    // Tree Creation (For Testing)
    void setRoot(TreeNode* node) {
        root = node;
    }
    // User-facing evaluation method
    double evaluate() {
        if (root == nullptr) return 0.0;
        return evaluateRecursive(root);
    }
};

int main() {
// Expression: (2 * 3) + 5
// Expected Result: 11.0
// Leaves (Numbers)
TreeNode* node2 = new TreeNode("2");
TreeNode* node3 = new TreeNode("3");
TreeNode* node5 = new TreeNode("5");
// Internal Node (Multiplication)
TreeNode* nodeMul = new TreeNode("*");
nodeMul->left = node2;
nodeMul->right = node3; 
// Root Node (Addition)
TreeNode* rootNode = new TreeNode("+");
rootNode->left = nodeMul;
rootNode->right = node5;
ExpressionTree tree;
tree.setRoot(rootNode);
cout << "--- Expression Tree Evaluation Test ---\n";
double result = tree.evaluate();
    cout << "Expression: (2 * 3) + 5\n";
    cout << "Result: " << result << endl; // Expected: 11.0
    // The deleteTree() method is called when the 'tree' object goes out of scope, clearing 
    return 0;
}