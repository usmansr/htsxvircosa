raw_data = [

    # ── 0: SINGLY LINKED LIST ──────────────────────────────────────
    ("""struct Node { int data; Node* next; };
       Node* head = NULL;
       void insert(int val) { Node* n = new Node(); n->data = val; n->next = head; head = n; }""", 0),

    ("""struct Node { int data; Node* next; Node(int d): data(d), next(NULL){} };
       void printList(Node* head) { while(head) { cout<<head->data<<" "; head=head->next; } }""", 0),

    ("""Node* deleteNode(Node* head, int key) {
         if(!head) return NULL;
         if(head->data==key) { Node* tmp=head->next; delete head; return tmp; }
         head->next = deleteNode(head->next, key); return head; }""", 0),

    ("""void reverseList(Node*& head) {
         Node *prev=NULL, *curr=head, *nxt;
         while(curr) { nxt=curr->next; curr->next=prev; prev=curr; curr=nxt; }
         head=prev; }""", 0),

    ("""int lengthList(Node* head) {
         int count=0;
         while(head!=NULL) { count++; head=head->next; }
         return count; }""", 0),

    ("""Node* search(Node* head, int key) {
         while(head) { if(head->data==key) return head; head=head->next; }
         return NULL; }""", 0),

    ("""void appendNode(Node*& head, int val) {
         Node* newNode = new Node(val);
         if(!head) { head=newNode; return; }
         Node* tmp=head;
         while(tmp->next) tmp=tmp->next;
         tmp->next=newNode; }""", 0),

    ("""struct Node { int data; Node* next; };
       Node* createNode(int data) { Node* n=new Node; n->data=data; n->next=NULL; return n; }""", 0),

    ("""void insertAfter(Node* prev, int data) {
         Node* newNode = new Node();
         newNode->data = data;
         newNode->next = prev->next;
         prev->next = newNode; }""", 0),

    ("""void deleteList(Node*& head) {
         Node* curr = head;
         while(curr) { Node* nxt = curr->next; delete curr; curr = nxt; }
         head = NULL; }""", 0),

    # ── 1: DOUBLY LINKED LIST ──────────────────────────────────────
    ("""struct Node { int data; Node* prev; Node* next; };
       void insertFront(Node*& head, int val) {
           Node* n=new Node(); n->data=val; n->prev=NULL; n->next=head;
           if(head) head->prev=n; head=n; }""", 1),

    ("""struct DNode { int data; DNode* prev; DNode* next;
           DNode(int d): data(d), prev(nullptr), next(nullptr){} };""", 1),

    ("""void deleteDNode(Node*& head, Node* del) {
         if(del->prev) del->prev->next = del->next;
         else head = del->next;
         if(del->next) del->next->prev = del->prev;
         delete del; }""", 1),

    ("""void printReverse(Node* tail) {
         while(tail) { cout<<tail->data<<" "; tail=tail->prev; } }""", 1),

    ("""Node* insertEnd(Node* tail, int val) {
         Node* n = new Node(); n->data=val; n->next=NULL; n->prev=tail;
         if(tail) tail->next=n;
         return n; }""", 1),

    ("""// Doubly linked list with both head and tail pointers
       struct DLL { Node* head; Node* tail;
           void pushFront(int v);
           void pushBack(int v);
           void popFront();
           void popBack(); };""", 1),

    ("""void swapNodes(Node* a, Node* b) {
         // update prev and next pointers for doubly linked list swap
         if(a->prev) a->prev->next = b;
         if(b->next) b->next->prev = a;
         Node* tmp = a->next; a->next = b->next; b->next = tmp;
         tmp = a->prev; a->prev = b->prev; b->prev = tmp; }""", 1),

    ("""struct Node { int data; Node* next; Node* prev;
           Node(int d): data(d), prev(NULL), next(NULL){} };
       Node* head = NULL;
       Node* tail = NULL;""", 1),

    ("""void insertAfterNode(Node* node, int val) {
         Node* newNode = new Node(val);
         newNode->next = node->next;
         newNode->prev = node;
         if(node->next) node->next->prev = newNode;
         node->next = newNode; }""", 1),

    ("""int countDLL(Node* head) {
         int c=0;
         while(head) { c++; head=head->next; }
         return c;
         // prev pointers allow backward traversal
         }""", 1),

    # ── 2: STACK ───────────────────────────────────────────────────
    ("""stack<int> st;
       st.push(10); st.push(20); st.push(30);
       cout << st.top(); st.pop();""", 2),

    ("""int stack[100]; int top=-1;
       void push(int v){ stack[++top]=v; }
       int pop(){ return stack[top--]; }
       int peek(){ return stack[top]; }""", 2),

    ("""bool isBalanced(string s) {
         stack<char> st;
         for(char c : s) {
             if(c=='(') st.push(c);
             else if(c==')') { if(st.empty()) return false; st.pop(); }
         }
         return st.empty(); }""", 2),

    ("""// Stack using linked list
       struct Stack { Node* top; int size;
           void push(int v){ Node* n=new Node(v); n->next=top; top=n; size++; }
           int pop(){ int v=top->data; Node* tmp=top; top=top->next; delete tmp; return v; } };""", 2),

    ("""string reverseString(string s) {
         stack<char> st;
         for(char c : s) st.push(c);
         string res="";
         while(!st.empty()) { res+=st.top(); st.pop(); }
         return res; }""", 2),

    ("""int evaluatePostfix(string expr) {
         stack<int> st;
         for(char c : expr) {
             if(isdigit(c)) st.push(c-'0');
             else { int b=st.top();st.pop(); int a=st.top();st.pop();
                    if(c=='+') st.push(a+b);
                    else if(c=='-') st.push(a-b);
                    else if(c=='*') st.push(a*b); }
         } return st.top(); }""", 2),

    ("""class Stack {
         int arr[1000]; int topIdx;
       public:
         Stack(): topIdx(-1){}
         void push(int x){ arr[++topIdx]=x; }
         int pop(){ return arr[topIdx--]; }
         bool isEmpty(){ return topIdx==-1; }
         int top(){ return arr[topIdx]; } };""", 2),

    ("""void pushElement(int* stack, int& top, int val) { stack[++top] = val; }
       int popElement(int* stack, int& top) { return stack[top--]; }
       bool isStackEmpty(int top) { return top == -1; }""", 2),

    ("""// DFS using explicit stack instead of recursion
       void dfsIterative(int start) {
         stack<int> st; st.push(start);
         while(!st.empty()) {
             int node = st.top(); st.pop();
             visited[node] = true;
             for(int nb : adj[node]) if(!visited[nb]) st.push(nb); } }""", 2),

    ("""// Stack overflow check
       bool isFull(int top, int capacity) { return top == capacity - 1; }
       void safePush(int* stack, int& top, int cap, int val) {
           if(!isFull(top, cap)) stack[++top] = val;
           else cout << \"Stack Overflow\"; }""", 2),

    # ── 3: QUEUE ───────────────────────────────────────────────────
    ("""queue<int> q;
       q.push(1); q.push(2); q.push(3);
       cout << q.front(); q.pop();""", 3),

    ("""int q[100]; int front=0, rear=-1;
       void enqueue(int v){ q[++rear]=v; }
       int dequeue(){ return q[front++]; }
       bool isQueueEmpty(){ return front>rear; }""", 3),

    ("""// BFS using queue
       void bfs(int start) {
         queue<int> q; q.push(start); visited[start]=true;
         while(!q.empty()) {
             int node=q.front(); q.pop();
             for(int nb : adj[node]) { if(!visited[nb]) { visited[nb]=true; q.push(nb); } } } }""", 3),

    ("""struct Queue { int arr[100]; int front, rear;
           Queue(): front(0), rear(-1){}
           void enqueue(int v){ arr[++rear]=v; }
           int dequeue(){ return arr[front++]; }
           bool isEmpty(){ return front>rear; } };""", 3),

    ("""// Circular queue
       int cq[MAX]; int f=0, r=0;
       void enqueue(int v){ cq[r]=v; r=(r+1)%MAX; }
       int dequeue(){ int v=cq[f]; f=(f+1)%MAX; return v; }""", 3),

    ("""// Queue using two stacks
       stack<int> s1, s2;
       void enqueue(int v){ s1.push(v); }
       int dequeue() {
           if(s2.empty()) while(!s1.empty()){ s2.push(s1.top()); s1.pop(); }
           int v=s2.top(); s2.pop(); return v; }""", 3),

    ("""class Queue {
         int data[500]; int head, tail;
       public:
         Queue(): head(0), tail(0){}
         void push(int x){ data[tail++]=x; }
         int pop(){ return data[head++]; }
         int front(){ return data[head]; }
         bool empty(){ return head==tail; } };""", 3),

    ("""// Level order traversal uses a queue
       void levelOrder(Node* root) {
         if(!root) return;
         queue<Node*> q; q.push(root);
         while(!q.empty()) {
             Node* curr = q.front(); q.pop();
             cout << curr->data << \" \";
             if(curr->left)  q.push(curr->left);
             if(curr->right) q.push(curr->right); } }""", 3),

    ("""void enqueueNode(Node*& front, Node*& rear, int val) {
         Node* n=new Node(val); n->next=NULL;
         if(!rear) { front=rear=n; return; }
         rear->next=n; rear=n; }""", 3),

    ("""int dequeueNode(Node*& front) {
         if(!front) return -1;
         int val = front->data;
         Node* tmp = front; front = front->next; delete tmp;
         return val; }""", 3),

    # ── 4: BST ─────────────────────────────────────────────────────
    ("""struct Node { int data; Node* left; Node* right;
           Node(int d): data(d), left(NULL), right(NULL){} };
       Node* insert(Node* root, int val) {
           if(!root) return new Node(val);
           if(val < root->data) root->left = insert(root->left, val);
           else root->right = insert(root->right, val);
           return root; }""", 4),

    ("""Node* search(Node* root, int key) {
         if(!root || root->data==key) return root;
         if(key < root->data) return search(root->left, key);
         return search(root->right, key); }""", 4),

    ("""void inorder(Node* root) {
         if(!root) return;
         inorder(root->left);
         cout << root->data << \" \";
         inorder(root->right); }""", 4),

    ("""Node* minValueNode(Node* node) {
         Node* curr = node;
         while(curr && curr->left) curr = curr->left;
         return curr; }
       Node* deleteNode(Node* root, int key) {
           if(!root) return root;
           if(key < root->data) root->left = deleteNode(root->left, key);
           else if(key > root->data) root->right = deleteNode(root->right, key);
           else {
               if(!root->left) { Node* t=root->right; delete root; return t; }
               else if(!root->right) { Node* t=root->left; delete root; return t; }
               Node* t = minValueNode(root->right);
               root->data = t->data;
               root->right = deleteNode(root->right, t->data); }
           return root; }""", 4),

    ("""int height(Node* root) {
         if(!root) return 0;
         return 1 + max(height(root->left), height(root->right)); }""", 4),

    ("""void preorder(Node* root) {
         if(!root) return;
         cout << root->data << \" \";
         preorder(root->left);
         preorder(root->right); }""", 4),

    ("""void postorder(Node* root) {
         if(!root) return;
         postorder(root->left);
         postorder(root->right);
         cout << root->data << \" \"; }""", 4),

    ("""bool isBST(Node* root, int mn=INT_MIN, int mx=INT_MAX) {
         if(!root) return true;
         if(root->data<=mn || root->data>=mx) return false;
         return isBST(root->left, mn, root->data) && isBST(root->right, root->data, mx); }""", 4),

    ("""// BST: all left subtree values < root < all right subtree values
       Node* buildBST(vector<int>& vals) {
         Node* root = NULL;
         for(int v : vals) root = insert(root, v);
         return root; }""", 4),

    ("""int countNodes(Node* root) {
         if(!root) return 0;
         return 1 + countNodes(root->left) + countNodes(root->right); }""", 4),

    # ── 5: AVL TREE ────────────────────────────────────────────────
    ("""struct AVLNode { int data, height; AVLNode* left; AVLNode* right;
           AVLNode(int d): data(d), height(1), left(NULL), right(NULL){} };
       int getHeight(AVLNode* n){ return n ? n->height : 0; }
       int getBalance(AVLNode* n){ return n ? getHeight(n->left)-getHeight(n->right) : 0; }""", 5),

    ("""AVLNode* rotateRight(AVLNode* y) {
         AVLNode* x = y->left; AVLNode* T2 = x->right;
         x->right = y; y->left = T2;
         y->height = max(getHeight(y->left), getHeight(y->right)) + 1;
         x->height = max(getHeight(x->left), getHeight(x->right)) + 1;
         return x; }""", 5),

    ("""AVLNode* rotateLeft(AVLNode* x) {
         AVLNode* y = x->right; AVLNode* T2 = y->left;
         y->left = x; x->right = T2;
         x->height = max(getHeight(x->left), getHeight(x->right)) + 1;
         y->height = max(getHeight(y->left), getHeight(y->right)) + 1;
         return y; }""", 5),

    ("""AVLNode* avlInsert(AVLNode* node, int key) {
         if(!node) return new AVLNode(key);
         if(key < node->data) node->left = avlInsert(node->left, key);
         else if(key > node->data) node->right = avlInsert(node->right, key);
         else return node;
         node->height = 1 + max(getHeight(node->left), getHeight(node->right));
         int balance = getBalance(node);
         // LL case
         if(balance>1 && key<node->left->data) return rotateRight(node);
         // RR case
         if(balance<-1 && key>node->right->data) return rotateLeft(node);
         // LR case
         if(balance>1 && key>node->left->data){ node->left=rotateLeft(node->left); return rotateRight(node); }
         // RL case
         if(balance<-1 && key<node->right->data){ node->right=rotateRight(node->right); return rotateLeft(node); }
         return node; }""", 5),

    ("""// AVL tree maintains balance factor between -1 and 1
       // balance = height(left) - height(right)
       // If |balance| > 1, rotations are triggered
       int bf = getHeight(node->left) - getHeight(node->right);""", 5),

    ("""// Four rotation cases in AVL:
       // LL: single right rotation
       // RR: single left rotation
       // LR: left rotation on child, then right rotation on node
       // RL: right rotation on child, then left rotation on node
       AVLNode* rebalance(AVLNode* node, int key){ /* ... */ }""", 5),

    ("""AVLNode* avlDelete(AVLNode* root, int key) {
         if(!root) return root;
         if(key < root->data) root->left = avlDelete(root->left, key);
         else if(key > root->data) root->right = avlDelete(root->right, key);
         else {
             if(!root->left || !root->right) {
                 AVLNode* tmp = root->left ? root->left : root->right;
                 if(!tmp) { tmp=root; root=NULL; } else *root=*tmp;
                 delete tmp; } }
         if(!root) return root;
         root->height = 1 + max(getHeight(root->left), getHeight(root->right));
         int balance = getBalance(root);
         return root; }""", 5),

    ("""// AVL node height update after every insert/delete
       void updateHeight(AVLNode* node) {
         node->height = 1 + max(
             node->left  ? node->left->height  : 0,
             node->right ? node->right->height : 0
         ); }""", 5),

    ("""// Self-balancing BST: height stored in each node
       struct AVLNode {
           int key, height;
           AVLNode* left;
           AVLNode* right;
       };
       int avlHeight(AVLNode* n){ return n ? n->height : -1; }""", 5),

    ("""// In-order traversal of AVL gives sorted sequence (same as BST)
       void avlInorder(AVLNode* root) {
           if(!root) return;
           avlInorder(root->left);
           cout << root->key << \" \";
           avlInorder(root->right); }""", 5),

    # ── 6: GRAPH ───────────────────────────────────────────────────
    ("""// Adjacency list graph representation
       int V = 5;
       vector<int> adj[10];
       void addEdge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }""", 6),

    ("""// Adjacency matrix
       int graph[100][100] = {0};
       void addEdge(int u, int v) { graph[u][v]=1; graph[v][u]=1; }
       bool hasEdge(int u, int v) { return graph[u][v]==1; }""", 6),

    ("""// Depth First Search
       bool visited[100] = {false};
       void dfs(int node) {
           visited[node] = true;
           cout << node << \" \";
           for(int nb : adj[node])
               if(!visited[nb]) dfs(nb); }""", 6),

    ("""// Breadth First Search on graph
       void bfs(int src) {
           vector<bool> vis(V, false);
           queue<int> q; q.push(src); vis[src]=true;
           while(!q.empty()) {
               int u=q.front(); q.pop(); cout<<u<<\" \";
               for(int v : adj[u]) if(!vis[v]){ vis[v]=true; q.push(v); } } }""", 6),

    ("""// Directed graph — edges go one way
       void addDirectedEdge(int u, int v) {
           adj[u].push_back(v); // u → v only
       }
       int indegree[100] = {0};
       void computeIndegree() { for(int u=0;u<V;u++) for(int v:adj[u]) indegree[v]++; }""", 6),

    ("""// Detect cycle in undirected graph using Union-Find
       int parent[100];
       int find(int x){ return parent[x]==x ? x : parent[x]=find(parent[x]); }
       void unite(int x, int y){ parent[find(x)]=find(y); }
       bool hasCycle(vector<pair<int,int>>& edges) {
           for(auto& e : edges) { if(find(e.first)==find(e.second)) return true; unite(e.first,e.second); }
           return false; }""", 6),

    ("""// Dijkstra's shortest path
       void dijkstra(int src) {
           vector<int> dist(V, INT_MAX); dist[src]=0;
           priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
           pq.push({0, src});
           while(!pq.empty()) {
               int u = pq.top().second; pq.pop();
               for(auto [w,v] : adjW[u])
                   if(dist[u]+w < dist[v]) { dist[v]=dist[u]+w; pq.push({dist[v],v}); } } }""", 6),

    ("""// Topological sort (DAG only)
       void topoSort(int u, vector<bool>& vis, stack<int>& st) {
           vis[u]=true;
           for(int v : adj[u]) if(!vis[v]) topoSort(v, vis, st);
           st.push(u); }""", 6),

    ("""// Edge list representation
       struct Edge { int src, dest, weight; };
       vector<Edge> edges;
       void addEdge(int u, int v, int w) { edges.push_back({u, v, w}); }""", 6),

    ("""// Check if graph is connected
       bool isConnected() {
           vector<bool> vis(V, false);
           dfs(0, vis);
           for(bool b : vis) if(!b) return false;
           return true;
       }
       // vertices, edges, adjacency list""", 6),
]
