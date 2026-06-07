
#include <iostream>
#include <algorithm> // for swap

using namespace std;

class PriorityQueue {
private:
    int* heapArr;  // Pointer to the array
    int capacity;  // Total size of the array
    int count;     // Current number of elements

    // Helper: Resize the array when full (Double the size)
    void resize() {
        int newCapacity = capacity * 2;
        int* newArr = new int[newCapacity];

        // Copy old data
        for (int i = 0; i < count; i++) {
            newArr[i] = heapArr[i];
        }

        // Delete old memory
        delete[] heapArr;
        
        // Update pointers
        heapArr = newArr;
        capacity = newCapacity;
    }

    void heapifyUp(int index) {
        // While not root AND current > parent
        while (index > 0 && heapArr[index] > heapArr[(index - 1) / 2]) {
            int parentIndex = (index - 1) / 2;
            swap(heapArr[index], heapArr[parentIndex]);
            index = parentIndex; 
        }
    }

    void heapifyDown(int index) {
        int leftChild = 2 * index + 1;
        int rightChild = 2 * index + 2;
        int largest = index;

        // Check bounds with 'count' instead of .size()
        if (leftChild < count && heapArr[leftChild] > heapArr[largest]) {
            largest = leftChild;
        }

        if (rightChild < count && heapArr[rightChild] > heapArr[largest]) {
            largest = rightChild;
        }

        if (largest != index) {
            swap(heapArr[index], heapArr[largest]);
            heapifyDown(largest);
        }
    }

public:
    // Constructor: Allocate initial memory
    PriorityQueue(int initCap = 10) {
        capacity = initCap;
        count = 0;
        heapArr = new int[capacity];
    }

    // Destructor: Clean up memory to prevent leaks
    ~PriorityQueue() {
        delete[] heapArr;
    }

    void push(int value) {
        // Check if array is full
        if (count == capacity) {
            resize();
        }

        // Insert at the end (index = count)
        heapArr[count] = value;
        heapifyUp(count);
        count++;
    }

    void pop() {
        if (count == 0) {
            cout << "Queue is empty!" << endl;
            return;
        }

        // Move the last element to the root
        heapArr[0] = heapArr[count - 1];
        count--; // Decrease size (effectively removing the last element)

        // Fix the heap
        if (count > 0) {
            heapifyDown(0);
        }
    }

    int top() {
        if (count == 0) throw runtime_error("Queue is empty");
        return heapArr[0];
    }

    bool empty() {
        return count == 0;
    }
    
    void print() {
        for (int i = 0; i < count; i++) {
            cout << heapArr[i] << " ";
        }
        cout << endl;
    }
};

int main() {
    PriorityQueue pq;

    pq.push(10);
    pq.push(30);
    pq.push(20);
    
    cout << "Top: " << pq.top() << endl; // 30

    pq.pop(); // Remove 30
    cout << "Top after pop: " << pq.top() << endl; // 20

    return 0;
}