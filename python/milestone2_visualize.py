"""
VisualDSA — Milestone 2
========================
Input  : C/C++ code string (or .cpp file path)
Output : PNG image of the predicted data structure with random data

Pipeline:
  1. Preprocess code (same as Colab notebook)
  2. Load .pkl model → predict data structure
  3. Generate random values
  4. Draw the correct structure → save PNG

Usage (after training in Colab and downloading .pkl):
  python milestone2_visualize.py
  python milestone2_visualize.py --file mycode.cpp
  python milestone2_visualize.py --code "stack<int> s; s.push(10);"
"""

import re
import sys
import random
import argparse
import pickle
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ──────────────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────────────

CLASS_NAMES = [
    "Singly Linked List",  # 0
    "Doubly Linked List",  # 1
    "Stack",               # 2
    "Queue",               # 3
    "BST",                 # 4
    "AVL Tree",            # 5
    "Graph",               # 6
]

# Color palette (background, border, text, edge-color)
PALETTE = {
    "node_fill":   "#DBEAFE",   # light blue
    "node_border": "#2563EB",   # blue
    "node_text":   "#1E3A5F",
    "edge":        "#64748B",
    "root_fill":   "#BFDBFE",
    "root_border": "#1D4ED8",
    "highlight":   "#FDE68A",
    "bg":          "#F8FAFC",
    "title":       "#1E3A5F",
    "subtitle":    "#64748B",
}

# Save PNGs in the same folder as this script (works on Windows, Linux, Mac)
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ──────────────────────────────────────────────────────────────────────────────
# PREPROCESSING  (identical to Colab notebook)
# ──────────────────────────────────────────────────────────────────────────────

def preprocess_code(code: str) -> str:
    code = re.sub(r"//.*", " ", code)
    code = re.sub(r"/\*.*?\*/", " ", code, flags=re.DOTALL)
    code = re.sub(r'".*?"', " ", code)
    code = code.lower()
    code = re.sub(r"[^a-z0-9_\s]", " ", code)
    code = re.sub(r"\s+", " ", code).strip()
    return code


# ──────────────────────────────────────────────────────────────────────────────
# KEYWORD-BASED FALLBACK (when no .pkl is available)
# ──────────────────────────────────────────────────────────────────────────────

KEYWORDS = {
    0: ["head", "next", "node", "singly", "insert", "list", "null"],
    1: ["prev", "head", "tail", "doubly", "next", "backward"],
    2: ["push", "pop", "top", "stack", "peek", "overflow"],
    3: ["front", "rear", "enqueue", "dequeue", "queue", "fifo"],
    4: ["left", "right", "root", "inorder", "bst", "binary", "search"],
    5: ["avl", "rotate", "balance", "height", "rotateright", "rotateleft", "getbalance"],
    6: ["adj", "addedge", "vertex", "edge", "dfs", "bfs", "graph", "visited"],
}


def fallback_predict(code: str):
    tokens = preprocess_code(code).split()
    scores = []
    for i in range(7):
        score = sum(1 for kw in KEYWORDS[i] for tok in tokens if kw in tok)
        scores.append(score)
    total = sum(scores) or 1
    probs = [s / total for s in scores]
    pred = probs.index(max(probs))
    return pred, max(probs) * 100


def predict(code: str, model_path: str = "visualdsa_nb_model.pkl"):
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            pipeline = pickle.load(f)
        cleaned = preprocess_code(code)
        pred = pipeline.predict([cleaned])[0]
        proba = pipeline.predict_proba([cleaned])[0]
        conf = max(proba) * 100
        print(f"[Model]    Loaded: {model_path}", file=sys.stderr)
    else:
        print(f"[Warning]  {model_path} not found — using keyword fallback.", file=sys.stderr)
        pred, conf = fallback_predict(code)

    print(f"[Predict]  → {CLASS_NAMES[pred]}  (confidence: {conf:.1f}%)", file=sys.stderr)
    return pred, conf


# ──────────────────────────────────────────────────────────────────────────────
# RANDOM DATA GENERATORS
# ──────────────────────────────────────────────────────────────────────────────

def rand_vals(n: int, lo: int = 10, hi: int = 99) -> list:
    """Unique random integers in [lo, hi]."""
    return random.sample(range(lo, hi + 1), n)


# ──────────────────────────────────────────────────────────────────────────────
# DRAW HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def fig_base(w: float = 10, h: float = 6, title: str = "", subtitle: str = ""):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(PALETTE["bg"])
    ax.set_facecolor(PALETTE["bg"])
    ax.axis("off")
    if title:
        fig.text(0.5, 0.97, title, ha="center", va="top",
                 fontsize=16, fontweight="bold", color=PALETTE["title"],
                 fontfamily="monospace")
    if subtitle:
        fig.text(0.5, 0.925, subtitle, ha="center", va="top",
                 fontsize=10, color=PALETTE["subtitle"])
    return fig, ax


def draw_circle_node(ax, cx, cy, r, val, is_root=False, color=None):
    fill = color or (PALETTE["root_fill"] if is_root else PALETTE["node_fill"])
    border = PALETTE["root_border"] if is_root else PALETTE["node_border"]
    circle = plt.Circle((cx, cy), r, color=fill, zorder=3)
    ax.add_patch(circle)
    circle2 = plt.Circle((cx, cy), r, fill=False,
                          edgecolor=border, linewidth=2, zorder=4)
    ax.add_patch(circle2)
    ax.text(cx, cy, str(val), ha="center", va="center",
            fontsize=13, fontweight="bold", color=PALETTE["node_text"], zorder=5)


def draw_rect_node(ax, cx, cy, w, h, val, fill=None, border=None, fontsize=13):
    fill = fill or PALETTE["node_fill"]
    border = border or PALETTE["node_border"]
    rect = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                          boxstyle="round,pad=0.04",
                          facecolor=fill, edgecolor=border,
                          linewidth=2, zorder=3)
    ax.add_patch(rect)
    ax.text(cx, cy, str(val), ha="center", va="center",
            fontsize=fontsize, fontweight="bold",
            color=PALETTE["node_text"], zorder=4)


def arrow(ax, x1, y1, x2, y2, color=None, both=False):
    c = color or PALETTE["edge"]
    style = "<->" if both else "->"
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                 arrowprops=dict(arrowstyle=style, color=c,
                                 lw=1.6, connectionstyle="arc3,rad=0.0"))


def line(ax, x1, y1, x2, y2, color=None, lw=1.6):
    c = color or PALETTE["edge"]
    ax.plot([x1, x2], [y1, y2], color=c, lw=lw, zorder=2)


# ──────────────────────────────────────────────────────────────────────────────
# VISUALIZATIONS
# ──────────────────────────────────────────────────────────────────────────────

# 0 — SINGLY LINKED LIST
def draw_sll(vals):
    n = len(vals)
    fig, ax = fig_base(11, 3.5,
                       "Singly Linked List",
                       f"head → {' → '.join(str(v) for v in vals)} → NULL")
    ax.set_xlim(-0.5, n * 2.4 + 0.5)
    ax.set_ylim(-1, 2)

    nw, nh, ptr_w = 1.3, 0.8, 0.45
    y = 0.6

    for i, v in enumerate(vals):
        x = i * 2.4
        # data box
        draw_rect_node(ax, x + nw/2, y, nw, nh, v)
        # pointer box
        ptr_fill = "#E0E7FF"
        ptr_rect = FancyBboxPatch((x + nw, y - nh/2), ptr_w, nh,
                                  boxstyle="round,pad=0.02",
                                  facecolor=ptr_fill,
                                  edgecolor=PALETTE["node_border"],
                                  linewidth=1.5, zorder=3)
        ax.add_patch(ptr_rect)

        if i < n - 1:
            ax.annotate("", xy=(x + 2.4, y),
                        xytext=(x + nw + ptr_w, y),
                        arrowprops=dict(arrowstyle="->",
                                        color=PALETTE["node_border"], lw=1.5))
        else:
            ax.text(x + nw + ptr_w/2, y, "∅", ha="center", va="center",
                    fontsize=12, color=PALETTE["subtitle"], zorder=5)

    # head label
    ax.annotate("head", xy=(0, y + nh/2), xytext=(0, y + 1.0),
                fontsize=10, color=PALETTE["subtitle"], ha="center",
                arrowprops=dict(arrowstyle="->", color=PALETTE["subtitle"], lw=1))

    plt.tight_layout(rect=[0, 0, 1, 0.88])
    path = f"{OUTPUT_DIR}/visualdsa_sll.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close(fig)
    return path


# 1 — DOUBLY LINKED LIST
def draw_dll(vals):
    n = len(vals)
    fig, ax = fig_base(12, 4,
                       "Doubly Linked List",
                       "NULL ← [prev|data|next] ⇄ ... → NULL")
    ax.set_xlim(-0.5, n * 2.8 + 0.5)
    ax.set_ylim(-1.5, 2.5)

    nw, nh = 1.5, 0.9
    y = 0.8

    for i, v in enumerate(vals):
        x = i * 2.8
        cx = x + nw/2

        # prev box (left, orange)
        p_rect = FancyBboxPatch((x, y - nh/2), 0.4, nh,
                                boxstyle="round,pad=0.02",
                                facecolor="#FEF3C7", edgecolor="#D97706",
                                linewidth=1.5, zorder=3)
        ax.add_patch(p_rect)
        ax.text(x + 0.2, y, "p", ha="center", va="center",
                fontsize=9, color="#92400E", fontweight="bold", zorder=5)

        # data box
        d_rect = FancyBboxPatch((x + 0.4, y - nh/2), 0.7, nh,
                                boxstyle="round,pad=0.02",
                                facecolor=PALETTE["node_fill"],
                                edgecolor=PALETTE["node_border"],
                                linewidth=2, zorder=3)
        ax.add_patch(d_rect)
        ax.text(x + 0.75, y, str(v), ha="center", va="center",
                fontsize=13, fontweight="bold", color=PALETTE["node_text"], zorder=5)

        # next box (right, blue)
        n_rect = FancyBboxPatch((x + 1.1, y - nh/2), 0.4, nh,
                                boxstyle="round,pad=0.02",
                                facecolor="#DBEAFE", edgecolor="#2563EB",
                                linewidth=1.5, zorder=3)
        ax.add_patch(n_rect)
        ax.text(x + 1.3, y, "n", ha="center", va="center",
                fontsize=9, color="#1E3A5F", fontweight="bold", zorder=5)

        if i < n - 1:
            nx2 = (i+1) * 2.8
            # forward arrow
            ax.annotate("", xy=(nx2, y + 0.2),
                        xytext=(x + nw, y + 0.2),
                        arrowprops=dict(arrowstyle="->",
                                        color="#2563EB", lw=1.5))
            # backward arrow
            ax.annotate("", xy=(x + nw, y - 0.2),
                        xytext=(nx2, y - 0.2),
                        arrowprops=dict(arrowstyle="->",
                                        color="#D97706", lw=1.5))
        else:
            ax.text(x + nw + 0.15, y, "∅", ha="left", va="center",
                    fontsize=12, color=PALETTE["subtitle"])

    ax.text(-0.3, y, "∅", ha="right", va="center",
            fontsize=12, color=PALETTE["subtitle"])
    ax.text(0.5, -0.8, "head", ha="center", fontsize=10, color=PALETTE["subtitle"])
    ax.annotate("", xy=(0.5, y - nh/2),
                xytext=(0.5, -0.6),
                arrowprops=dict(arrowstyle="->", color=PALETTE["subtitle"], lw=1))

    plt.tight_layout(rect=[0, 0, 1, 0.88])
    path = f"{OUTPUT_DIR}/visualdsa_dll.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close(fig)
    return path


# 2 — STACK
def draw_stack(vals):
    fig, ax = fig_base(5, 8, "Stack", "LIFO — Last In, First Out")
    nw, nh, gap = 2.4, 0.75, 0.05
    cx = 0
    ax.set_xlim(-2, 3.5)
    ax.set_ylim(-0.5, len(vals) + 1.5)

    for i, v in enumerate(vals):
        y = i * (nh + gap)
        is_top = i == len(vals) - 1
        fill = PALETTE["highlight"] if is_top else PALETTE["node_fill"]
        border = "#D97706" if is_top else PALETTE["node_border"]
        draw_rect_node(ax, cx, y + nh/2, nw, nh, v,
                       fill=fill, border=border)
        if is_top:
            ax.text(cx + nw/2 + 0.15, y + nh/2, "← top",
                    va="center", fontsize=10,
                    color="#92400E", fontweight="bold")

    # base
    base_y = 0
    ax.plot([-nw/2, nw/2], [base_y - 0.05, base_y - 0.05],
            color=PALETTE["node_border"], lw=3)

    # push arrow
    top_y = len(vals) * (nh + gap) + 0.1
    ax.annotate("push", xy=(cx, top_y - 0.05),
                xytext=(cx, top_y + 0.5),
                fontsize=10, ha="center", color="#059669",
                arrowprops=dict(arrowstyle="->", color="#059669", lw=1.5))
    ax.annotate("pop", xy=(cx, top_y + 0.55),
                xytext=(cx, top_y + 0.1),
                fontsize=10, ha="center", color="#DC2626",
                arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.5))

    plt.tight_layout(rect=[0, 0, 1, 0.92])
    path = f"{OUTPUT_DIR}/visualdsa_stack.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close(fig)
    return path


# 3 — QUEUE
def draw_queue(vals):
    n = len(vals)
    fig, ax = fig_base(12, 3.8, "Queue", "FIFO — dequeue from front, enqueue at rear")
    nw, nh = 1.4, 0.8
    gap = 0.1
    y = 0.6
    ax.set_xlim(-1.5, n * (nw + gap) + 2.5)
    ax.set_ylim(-1, 2.2)

    for i, v in enumerate(vals):
        x = i * (nw + gap)
        is_front = i == 0
        is_rear  = i == n - 1
        fill   = "#D1FAE5" if is_front else ("#FEF3C7" if is_rear else PALETTE["node_fill"])
        border = "#059669" if is_front else ("#D97706" if is_rear  else PALETTE["node_border"])
        draw_rect_node(ax, x + nw/2, y, nw, nh, v, fill=fill, border=border)

        if is_front:
            ax.text(x + nw/2, y - nh/2 - 0.22, "front",
                    ha="center", fontsize=9, color="#059669", fontweight="bold")
        if is_rear:
            ax.text(x + nw/2, y - nh/2 - 0.22, "rear",
                    ha="center", fontsize=9, color="#D97706", fontweight="bold")

    total_w = n * (nw + gap)

    # dequeue arrow (left)
    ax.annotate("dequeue", xy=(-0.1, y), xytext=(-1.3, y),
                fontsize=9, ha="center", va="center", color="#059669",
                arrowprops=dict(arrowstyle="->", color="#059669", lw=1.5))

    # enqueue arrow (right)
    ax.annotate("enqueue", xy=(total_w + 0.1, y), xytext=(total_w + 1.4, y),
                fontsize=9, ha="center", va="center", color="#D97706",
                arrowprops=dict(arrowstyle="<-", color="#D97706", lw=1.5))

    plt.tight_layout(rect=[0, 0, 1, 0.88])
    path = f"{OUTPUT_DIR}/visualdsa_queue.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close(fig)
    return path


# 4 — BST
class BSTNode:
    def __init__(self, val):
        self.val = val
        self.left = self.right = None

def bst_insert(root, val):
    if root is None:
        return BSTNode(val)
    if val < root.val:
        root.left = bst_insert(root.left, val)
    else:
        root.right = bst_insert(root.right, val)
    return root

def bst_positions(node, depth=0, pos=0, positions=None, edges=None):
    """Assign (x, y) positions via in-order index."""
    if positions is None:
        positions = {}
        edges = []
    if node is None:
        return positions, edges, pos
    positions, edges, pos = bst_positions(node.left, depth+1, pos, positions, edges)
    positions[node.val] = (pos, -depth)
    pos += 1
    positions, edges, pos = bst_positions(node.right, depth+1, pos, positions, edges)
    return positions, edges, pos

def collect_edges(node, edges):
    if node is None:
        return
    if node.left:
        edges.append((node.val, node.left.val))
        collect_edges(node.left, edges)
    if node.right:
        edges.append((node.val, node.right.val))
        collect_edges(node.right, edges)

def draw_bst(vals):
    # Build BST — insert in order to ensure a somewhat balanced tree
    sorted_mid_insert = []
    def mid_insert(arr):
        if not arr: return
        mid = len(arr) // 2
        sorted_mid_insert.append(arr[mid])
        mid_insert(arr[:mid])
        mid_insert(arr[mid+1:])
    mid_insert(sorted(vals))

    root = None
    for v in sorted_mid_insert:
        root = bst_insert(root, v)

    positions = {}
    edges = []
    bst_positions(root, positions=positions, edges=edges)
    collect_edges(root, edges)

    # Normalise positions for plotting
    xs = [p[0] for p in positions.values()]
    ys = [p[1] for p in positions.values()]
    x_range = max(xs) - min(xs) or 1
    y_range = max(ys) - min(ys) or 1

    scale_x, scale_y = 8.0 / (x_range + 1), 5.0 / (y_range + 1)
    pos = {v: ((px - min(xs)) * scale_x, (py - min(ys)) * scale_y)
           for v, (px, py) in positions.items()}

    fig, ax = fig_base(10, 7, "Binary Search Tree (BST)",
                       "Left child < Parent < Right child")
    all_x = [p[0] for p in pos.values()]
    all_y = [p[1] for p in pos.values()]
    ax.set_xlim(min(all_x) - 0.8, max(all_x) + 0.8)
    ax.set_ylim(min(all_y) - 0.8, max(all_y) + 0.8)

    R = 0.32

    # edges first
    for (u, v) in edges:
        ux, uy = pos[u]
        vx, vy = pos[v]
        dx, dy = vx - ux, vy - uy
        dist = (dx**2 + dy**2) ** 0.5
        nx2, ny2 = dx / dist, dy / dist
        ax.annotate("", xy=(vx - nx2*R, vy - ny2*R),
                    xytext=(ux + nx2*R, uy + ny2*R),
                    arrowprops=dict(arrowstyle="-|>",
                                    color=PALETTE["edge"], lw=1.8,
                                    mutation_scale=14))

    # nodes
    root_val = sorted_mid_insert[0]
    for v, (px, py) in pos.items():
        draw_circle_node(ax, px, py, R, v, is_root=(v == root_val))

    # legend
    ax.text(0.02, 0.04, "root node highlighted in darker blue",
            transform=ax.transAxes, fontsize=9, color=PALETTE["subtitle"])

    plt.tight_layout(rect=[0, 0, 1, 0.9])
    path = f"{OUTPUT_DIR}/visualdsa_bst.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close(fig)
    return path


# 5 — AVL TREE
class AVLNode:
    def __init__(self, val):
        self.val = val
        self.left = self.right = None
        self.height = 1

def avl_height(n):
    return n.height if n else 0

def avl_balance(n):
    return avl_height(n.left) - avl_height(n.right) if n else 0

def avl_update(n):
    n.height = 1 + max(avl_height(n.left), avl_height(n.right))

def avl_rr(y):
    x = y.left; T2 = x.right
    x.right = y; y.left = T2
    avl_update(y); avl_update(x)
    return x

def avl_ll(x):
    y = x.right; T2 = y.left
    y.left = x; x.right = T2
    avl_update(x); avl_update(y)
    return y

def avl_insert(node, key):
    if not node:
        return AVLNode(key)
    if key < node.val:
        node.left = avl_insert(node.left, key)
    elif key > node.val:
        node.right = avl_insert(node.right, key)
    else:
        return node
    avl_update(node)
    bf = avl_balance(node)
    if bf > 1 and key < node.left.val:   return avl_rr(node)
    if bf < -1 and key > node.right.val: return avl_ll(node)
    if bf > 1 and key > node.left.val:   node.left = avl_ll(node.left); return avl_rr(node)
    if bf < -1 and key < node.right.val: node.right = avl_rr(node.right); return avl_ll(node)
    return node

def draw_avl(vals):
    root = None
    for v in vals:
        root = avl_insert(root, v)

    # collect positions same way as BST
    node_pos = {}
    edges = []

    def collect(node, depth=0, counter=[0]):
        if not node: return
        collect(node.left, depth+1, counter)
        node_pos[node.val] = (counter[0], -depth, avl_balance(node))
        counter[0] += 1
        collect(node.right, depth+1, counter)

    def get_edges(node):
        if not node: return
        if node.left:  edges.append((node.val, node.left.val)); get_edges(node.left)
        if node.right: edges.append((node.val, node.right.val)); get_edges(node.right)

    collect(root)
    get_edges(root)

    xs = [v[0] for v in node_pos.values()]
    ys = [v[1] for v in node_pos.values()]
    x_range = max(xs) - min(xs) or 1
    y_range = max(ys) - min(ys) or 1
    sx, sy = 8.0 / (x_range + 1), 5.0 / (y_range + 1)
    pos = {v: ((d[0] - min(xs)) * sx, (d[1] - min(ys)) * sy)
           for v, d in node_pos.items()}
    bfs = {v: d[2] for v, d in node_pos.items()}

    fig, ax = fig_base(10, 7, "AVL Tree",
                       "Self-balancing BST | balance factor shown per node")
    ax.set_xlim(min(p[0] for p in pos.values()) - 0.8,
                max(p[0] for p in pos.values()) + 0.8)
    ax.set_ylim(min(p[1] for p in pos.values()) - 0.8,
                max(p[1] for p in pos.values()) + 0.8)
    R = 0.32

    for (u, v) in edges:
        ux, uy = pos[u]; vx, vy = pos[v]
        dx, dy = vx - ux, vy - uy
        dist = (dx**2 + dy**2)**0.5
        nx2, ny2 = dx/dist, dy/dist
        ax.annotate("", xy=(vx - nx2*R, vy - ny2*R),
                    xytext=(ux + nx2*R, uy + ny2*R),
                    arrowprops=dict(arrowstyle="-|>",
                                    color=PALETTE["edge"], lw=1.8, mutation_scale=14))

    root_val = root.val
    for v, (px, py) in pos.items():
        bf = bfs[v]
        color = "#D1FAE5" if bf == 0 else "#FEF3C7"  # green=balanced, amber=skewed
        border = "#059669" if bf == 0 else "#D97706"
        draw_circle_node(ax, px, py, R, v,
                         is_root=(v == root_val),
                         color="#BFDBFE" if v == root_val else color)
        # balance factor label
        ax.text(px + R + 0.08, py + R + 0.04,
                f"{bf:+d}", fontsize=8, color=border, fontweight="bold", zorder=6)

    # legend
    green_p = mpatches.Patch(color="#D1FAE5", label="balance = 0")
    amber_p = mpatches.Patch(color="#FEF3C7", label="|balance| = 1")
    ax.legend(handles=[green_p, amber_p], loc="lower right", fontsize=9,
              framealpha=0.7)

    plt.tight_layout(rect=[0, 0, 1, 0.9])
    path = f"{OUTPUT_DIR}/visualdsa_avl.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close(fig)
    return path


# 6 — GRAPH
def draw_graph(vals):
    n = len(vals)
    import math

    # Arrange nodes in a circle
    angles = [2 * math.pi * i / n for i in range(n)]
    R_outer = 2.8
    pos = {vals[i]: (R_outer * math.cos(a), R_outer * math.sin(a))
           for i, a in enumerate(angles)}

    # Random edges (connected, no duplicate)
    random.shuffle(vals)
    edges = []
    edge_set = set()
    # Ensure connectivity: spanning chain
    for i in range(n - 1):
        a, b = vals[i], vals[i+1]
        edges.append((a, b))
        edge_set.add((min(a,b), max(a,b)))
    # Add ~n//2 extra random edges
    attempts = 0
    while len(edges) < n + n // 2 and attempts < 200:
        a = random.choice(vals)
        b = random.choice(vals)
        if a != b and (min(a,b), max(a,b)) not in edge_set:
            edges.append((a, b))
            edge_set.add((min(a,b), max(a,b)))
        attempts += 1

    fig, ax = fig_base(9, 9, "Graph",
                       f"Undirected graph — {n} vertices, {len(edges)} edges")
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(-4.2, 4.2)
    ax.set_aspect("equal")

    for (u, v) in edges:
        ux, uy = pos[u]; vx, vy = pos[v]
        ax.plot([ux, vx], [uy, vy], color=PALETTE["edge"], lw=1.5, zorder=1)

    NR = 0.38
    for i, v in enumerate(vals):
        px, py = pos[v]
        is_src = i == 0
        draw_circle_node(ax, px, py, NR, v, is_root=is_src)

    ax.text(0, 0, "adj[ ]", ha="center", va="center",
            fontsize=10, color=PALETTE["subtitle"], style="italic")

    plt.tight_layout(rect=[0, 0, 1, 0.9])
    path = f"{OUTPUT_DIR}/visualdsa_graph.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close(fig)
    return path


# ──────────────────────────────────────────────────────────────────────────────
# DISPATCH TABLE
# ──────────────────────────────────────────────────────────────────────────────

NODE_COUNTS = {0: 6, 1: 5, 2: 6, 3: 5, 4: 9, 5: 8, 6: 7}

DRAW_FN = {
    0: draw_sll,
    1: draw_dll,
    2: draw_stack,
    3: draw_queue,
    4: draw_bst,
    5: draw_avl,
    6: draw_graph,
}


# ──────────────────────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ──────────────────────────────────────────────────────────────────────────────

def run(code: str, model_path: str = "visualdsa_nb_model.pkl") -> str:
    print("\n" + "="*55)
    print("  VisualDSA — Milestone 2 Pipeline")
    print("="*55)

    # Step 1: Predict
    pred, conf = predict(code, model_path)
    ds_name = CLASS_NAMES[pred]

    # Step 2: Generate random values
    n = NODE_COUNTS[pred]
    vals = rand_vals(n)
    print(f"[Data]     {n} random values: {vals}", file=sys.stderr)

    # Step 3: Draw
    draw_fn = DRAW_FN[pred]
    out_path = draw_fn(vals)

    print(f"[Output]   PNG saved → {out_path}", file=sys.stderr)
    print("="*55 + "\n")
    return out_path


# ──────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────────────────────────────────────

SAMPLE_CODES = {
    "bst": """
        struct Node { int data; Node* left; Node* right; };
        Node* insert(Node* root, int val) {
            if (!root) return new Node{val, nullptr, nullptr};
            if (val < root->data) root->left = insert(root->left, val);
            else root->right = insert(root->right, val);
            return root;
        }
    """,
    "avl": """
        struct AVLNode { int data, height; AVLNode* left; AVLNode* right; };
        int getBalance(AVLNode* n) { return getHeight(n->left) - getHeight(n->right); }
        AVLNode* rotateRight(AVLNode* y) { AVLNode* x = y->left; x->right = y; return x; }
    """,
    "stack": """
        int stack[100]; int top = -1;
        void push(int v) { stack[++top] = v; }
        int pop() { return stack[top--]; }
    """,
    "queue": """
        queue<int> q;
        q.push(1); q.push(2);
        cout << q.front(); q.pop();
    """,
    "sll": """
        struct Node { int data; Node* next; };
        Node* head = NULL;
        void insert(int val) { Node* n = new Node(); n->data = val; n->next = head; head = n; }
    """,
    "dll": """
        struct Node { int data; Node* prev; Node* next; };
        void insertFront(Node*& head, int val) {
            Node* n = new Node(); n->prev = NULL; n->next = head;
            if(head) head->prev = n; head = n;
        }
    """,
    "graph": """
        vector<int> adj[10];
        void addEdge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }
        void dfs(int node) { visited[node] = true; for(int nb : adj[node]) dfs(nb); }
    """,
}

if __name__ == "__main__":
    import base64, json

    parser = argparse.ArgumentParser()
    parser.add_argument("--code",   type=str, default=None)
    parser.add_argument("--file",   type=str, default=None)
    parser.add_argument("--model",  type=str, default="visualdsa_nb_model.pkl")
    parser.add_argument("--sample", type=str, default=None,
                        choices=list(SAMPLE_CODES.keys()))
    args = parser.parse_args()

    # Read code: --code arg → --file → stdin
    if args.code:
        code = args.code
    elif args.file:
        with open(args.file) as f:
            code = f.read()
    elif args.sample:
        code = SAMPLE_CODES[args.sample]
    else:
        code = sys.stdin.read()

    # Predict
    pred, conf = predict(code, args.model)

    # Generate PNG
    n = NODE_COUNTS[pred]
    vals = rand_vals(n)
    png_path = DRAW_FN[pred](vals)

    # Encode PNG as base64
    with open(png_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    # Output JSON to stdout (Node.js reads this)
    print(json.dumps({
        "label":      CLASS_NAMES[pred],
        "labelShort": ["SLL","DLL","Stack","Queue","BST","AVL","Graph"][pred],
        "confidence": round(conf, 1),
        "image":      "data:image/png;base64," + img_b64
    }))