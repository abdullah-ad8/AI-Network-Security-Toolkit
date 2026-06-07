 #include <iostream>
 #include <fstream>
 #include <string>
 using namespace std;
 #define nullptr NULL


 class Node {                        // Node class for Doubly Linked List
 public:
    int x,y;
    Node* next;
    Node(int row,int column) {                 // Constructor to initialize a new node
        x = row;
        y = column;
        next = nullptr;
    }
 };


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
    void Push(int r,int c) {
        Node*newnode=new Node(r,c);
        newnode->next=top;
        top=newnode;

        // LIFO: Add a new node at the beginning of the list (new top)
    }
    bool Pop(int r,int c) {
            if (top == nullptr) {
            return false;  // sentinel value
        }
        Node*temp=top;
        top=top->next;
        r=temp->x;
        c=temp->y;
        delete temp;
        return true;

        // LIFO: Remove the node from the beginning of the list (old top)
    }
    void startlocation(int r,int c,char**maze){
        Node*starter=new Node(r,c);



    }
};


void matrix_size(string filename,int row,int col){
        ifstream file(filename);  // Open the file
        string line;

        if (!file) {
            cout << "Could not open the file!" << endl;
            return ;
        }
        while (getline(file, line)) {
            if (line.empty()) continue; 

            if (row== 0) {
                col = line.length();
            }
            row++;
        }
        
        file.close();

        cout << "column: " << col << '\n';
        cout << "row: " << row << '\n';

    }


void read_maze(string filename, char** maze, int rows, int cols, int &startRow, int &startCol) {
        ifstream file(filename);
        if (!file) {
            cout << "Error opening file!" << endl;
            return;
        }

        string line;
        for (int i = 0; i < rows; i++) {
            if (getline(file, line)) { 
                for (int j = 0; j < cols; j++) {
                    maze[i][j] = line[j];

                    if (maze[i][j] == 'S') {
                        startRow = i;
                        startCol = j;
                    }
                }
            }
        }
        file.close();
    }

void search(string filename, char** maze, int rows, int cols, int &startRow, int &startCol) {


}










int main(){

    int rows = 0;
    int cols = 0;
    string filename="file1.txt";

    matrix_size(filename, rows, cols);

    char** maze = new char*[rows];
    for(int i = 0; i < rows; ++i) {
        maze[i] = new char[cols];
    }
    return 0;
}