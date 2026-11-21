"""
Fase4CarlosBasto - BST Explorer
Course: Data Structures (301305) - UNAD
Phase 4: Implementation of Binary Trees and Binary Structures

Graphical application (Tkinter) that lets the user build a Binary Search Tree
(BST) interactively, with a maximum of 4 levels, and shows the Pre-order,
In-order and Post-order traversals.
"""

import re
import tkinter as tk
from datetime import date
from tkinter import messagebox

APP_NAME = "Fase4CarlosBasto"
STUDENT_NAME = "Carlos Eduardo Basto"
COURSE_NAME = "Data Structures \u00b7 301305"
PASSWORD = "UNAD"
MAX_LEVELS = 4

# ----------------------------------------------------------------- palette
BG = "#0f1b2a"
BG_PANEL = "#16263a"
BG_CANVAS = "#0b1522"
BORDER = "#0e8ca8"
CYAN = "#00b4d8"
GREEN = "#06d6a0"
ORANGE = "#f4a261"
RED = "#e63946"
YELLOW = "#ffd166"
TEXT = "#d7e3f0"
MUTED = "#6c8299"
FONT = "Consolas"

INTEGER_PATTERN = re.compile(r"^[+-]?\d+$")


# ---------------------------------------------------------------- BST model
class MaxDepthError(Exception):
    """Raised when inserting a node would create a level beyond MAX_LEVELS."""


class DuplicateNodeError(Exception):
    """Raised when the value already exists in the tree."""


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self, max_levels=MAX_LEVELS):
        self.root = None
        self.size = 0
        self.max_levels = max_levels

    def insert(self, value):
        """Insert a value. Levels are counted from 1 (the root)."""
        if self.root is None:
            self.root = Node(value)
            self.size = 1
            return 1

        current = self.root
        level = 1
        while True:
            if value == current.value:
                raise DuplicateNodeError(value)
            child_attr = "left" if value < current.value else "right"
            child = getattr(current, child_attr)
            level += 1
            if child is None:
                if level > self.max_levels:
                    raise MaxDepthError(value)
                setattr(current, child_attr, Node(value))
                self.size += 1
                return level
            current = child

    def search(self, value):
        """Return (found, path) where path is the list of visited values."""
        path = []
        current = self.root
        while current is not None:
            path.append(current.value)
            if value == current.value:
                return True, path
            current = current.left if value < current.value else current.right
        return False, path

    def clear(self):
        self.root = None
        self.size = 0

    def height(self, node="root"):
        if node == "root":
            node = self.root
        if node is None:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def preorder(self):
        result = []

        def visit(node):
            if node:
                result.append(node.value)
                visit(node.left)
                visit(node.right)

        visit(self.root)
        return result

    def inorder(self):
        result = []

        def visit(node):
            if node:
                visit(node.left)
                result.append(node.value)
                visit(node.right)

        visit(self.root)
        return result

    def postorder(self):
        result = []

        def visit(node):
            if node:
                visit(node.left)
                visit(node.right)
                result.append(node.value)

        visit(self.root)
        return result


# ------------------------------------------------------------- login window
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.authenticated = False
        self.title(f"{APP_NAME} \u2014 Login")
        self.configure(bg=BG)
        self.resizable(False, False)
        self._center(460, 560)
        self._build()
        self.password_entry.focus_set()
        self.bind("<Return>", lambda _e: self.try_login())

    def _center(self, w, h):
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        tk.Frame(self, bg=CYAN, height=4).pack(fill="x")

        tk.Label(self, text="\u25b2  BST Explorer", bg=BG, fg=CYAN,
                 font=(FONT, 24, "bold")).pack(pady=(32, 2))
        tk.Label(self, text="Binary Search Tree \u2014 Phase 4", bg=BG, fg=MUTED,
                 font=(FONT, 11)).pack(pady=(0, 20))

        info = tk.Frame(self, bg=BG_PANEL, highlightbackground=BORDER,
                        highlightthickness=1)
        info.pack(padx=40, fill="x")
        rows = [
            ("Application:", APP_NAME),
            ("Student:", STUDENT_NAME),
            ("Course:", COURSE_NAME),
            ("Date:", date.today().strftime("%B %d, %Y")),
        ]
        for label, value in rows:
            row = tk.Frame(info, bg=BG_PANEL)
            row.pack(fill="x", padx=14, pady=4)
            tk.Label(row, text=label, bg=BG_PANEL, fg=MUTED, width=13,
                     anchor="w", font=(FONT, 10)).pack(side="left")
            tk.Label(row, text=value, bg=BG_PANEL, fg=TEXT, anchor="w",
                     font=(FONT, 10)).pack(side="left")

        tk.Label(self, text="Enter Password", bg=BG, fg=TEXT, anchor="w",
                 font=(FONT, 10, "bold")).pack(padx=40, pady=(24, 4), fill="x")

        box = tk.Frame(self, bg=BG_PANEL, highlightbackground=BORDER,
                       highlightthickness=1)
        box.pack(padx=40, fill="x")
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            box, textvariable=self.password_var, show="\u2022", bg=BG_PANEL,
            fg=TEXT, insertbackground=TEXT, relief="flat", font=(FONT, 13))
        self.password_entry.pack(side="left", fill="x", expand=True,
                                 padx=10, pady=10)
        self.show_btn = tk.Button(box, text="\U0001F441", bg=BG_PANEL, fg=MUTED,
                                  relief="flat", bd=0, activebackground=BG_PANEL,
                                  activeforeground=CYAN, cursor="hand2",
                                  command=self.toggle_password)
        self.show_btn.pack(side="right", padx=10)

        tk.Label(self, text="Password is masked (\u2014 \u2014 \u2014)", bg=BG,
                 fg=MUTED, anchor="w", font=(FONT, 9)).pack(padx=40, pady=(4, 0),
                                                           fill="x")

        tk.Button(self, text="Access BST Explorer  \u2192", bg=CYAN, fg="#06222b",
                  activebackground=GREEN, relief="flat", cursor="hand2",
                  font=(FONT, 11, "bold"), command=self.try_login
                  ).pack(padx=40, pady=22, fill="x", ipady=10)

        tk.Label(self, text="UNAD \u00b7 ECBTI \u00b7 Systems Engineering", bg=BG,
                 fg=MUTED, font=(FONT, 8)).pack(side="bottom", pady=10)

    def toggle_password(self):
        hidden = self.password_entry.cget("show") != ""
        self.password_entry.config(show="" if hidden else "\u2022")

    def try_login(self):
        if self.password_var.get() == PASSWORD:
            self.authenticated = True
            self.destroy()
        else:
            messagebox.showerror("Access Denied",
                                 "Incorrect password.\nPlease try again.",
                                 parent=self)
            self.password_var.set("")
            self.password_entry.focus_set()


# -------------------------------------------------------------- main window
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} \u2014 BST Explorer")
        self.configure(bg=BG)
        self.minsize(1000, 650)
        w, h = 1180, 740
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        self.tree = BinarySearchTree()
        self.highlight = {}  # value -> color (search path / found node)

        self._build_header()
        self._build_body()
        self._build_status()
        self.bind("<Return>", lambda _e: self.add_node())
        self.refresh()
        self.set_status("Tree cleared successfully.", MUTED)

    # ---- layout
    def _build_header(self):
        header = tk.Frame(self, bg=BG_PANEL, highlightbackground=BORDER,
                          highlightthickness=1)
        header.pack(fill="x")
        tk.Label(header, text="\u25b2  BST Explorer \u2014 Binary Search Tree",
                 bg=BG_PANEL, fg=CYAN, font=(FONT, 12, "bold")
                 ).pack(side="left", padx=14, pady=8)
        tk.Label(header, text=f"{STUDENT_NAME}  |  {COURSE_NAME}", bg=BG_PANEL,
                 fg=MUTED, font=(FONT, 9)).pack(side="right", padx=14)

    def _panel(self, parent, title):
        frame = tk.Frame(parent, bg=BG_CANVAS, highlightbackground=BORDER,
                         highlightthickness=1)
        tk.Label(frame, text=title, bg=BG_PANEL, fg=CYAN, anchor="w",
                 font=(FONT, 9, "bold")).pack(fill="x")
        canvas = tk.Canvas(frame, bg=BG_CANVAS, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        return frame, canvas

    def _build_body(self):
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=6, pady=6)

        # --- sidebar
        side = tk.Frame(body, bg=BG_PANEL, width=210, highlightbackground=BORDER,
                        highlightthickness=1)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

        tk.Label(side, text="Controls", bg=BG_PANEL, fg=CYAN,
                 font=(FONT, 13, "bold")).pack(pady=(12, 8))
        tk.Label(side, text="Node Value (integer)", bg=BG_PANEL, fg=TEXT,
                 anchor="w", font=(FONT, 9)).pack(fill="x", padx=12)
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(side, textvariable=self.entry_var, bg=BG_CANVAS,
                              fg=TEXT, insertbackground=TEXT, justify="center",
                              relief="flat", font=(FONT, 14),
                              highlightbackground=BORDER, highlightthickness=1)
        self.entry.pack(fill="x", padx=12, pady=(4, 12), ipady=6)
        self.entry.focus_set()

        def button(text, color, command):
            tk.Button(side, text=text, bg=color, fg="#06141c",
                      activebackground=TEXT, relief="flat", cursor="hand2",
                      font=(FONT, 10, "bold"), command=command
                      ).pack(fill="x", padx=12, pady=4, ipady=8)

        button("+  Add Node", CYAN, self.add_node)
        button("\u2315  Search Node", GREEN, self.search_node)
        button("\u2716  Clear Tree", ORANGE, self.clear_tree)
        button("\u23fb  Exit", RED, self.exit_app)

        tk.Frame(side, bg=BORDER, height=1).pack(fill="x", padx=12, pady=10)
        tk.Label(side, text="Tree Statistics", bg=BG_PANEL, fg=MUTED, anchor="w",
                 font=(FONT, 9, "bold")).pack(fill="x", padx=12)
        self.stats = {}
        for key in ("Nodes", "Height", "Root"):
            row = tk.Frame(side, bg=BG_PANEL)
            row.pack(fill="x", padx=12, pady=1)
            tk.Label(row, text=f"{key}:", bg=BG_PANEL, fg=MUTED, width=8,
                     anchor="w", font=(FONT, 9)).pack(side="left")
            lbl = tk.Label(row, text="0", bg=BG_PANEL, fg=TEXT, anchor="w",
                           font=(FONT, 9, "bold"))
            lbl.pack(side="left")
            self.stats[key] = lbl

        tk.Frame(side, bg=BORDER, height=1).pack(fill="x", padx=12, pady=10)
        tk.Label(side, text="Legend", bg=BG_PANEL, fg=MUTED, anchor="w",
                 font=(FONT, 9, "bold")).pack(fill="x", padx=12)
        for color, text in ((CYAN, "Regular node"), (GREEN, "Found node"),
                            (ORANGE, "Search path"), (YELLOW, "Traversal node")):
            row = tk.Frame(side, bg=BG_PANEL)
            row.pack(fill="x", padx=12, pady=1)
            tk.Label(row, text="\u25cf", bg=BG_PANEL, fg=color,
                     font=(FONT, 10)).pack(side="left")
            tk.Label(row, text=text, bg=BG_PANEL, fg=TEXT,
                     font=(FONT, 9)).pack(side="left", padx=6)

        # --- right side
        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))

        tree_frame, self.tree_canvas = self._panel(
            right, f"  BST Tree  (max {MAX_LEVELS} levels)")
        tree_frame.pack(fill="both", expand=True)

        bottom = tk.Frame(right, bg=BG)
        bottom.pack(fill="x", pady=(6, 0))
        self.trav_canvases = {}
        for col, (name, title) in enumerate((("pre", "  Pre-order"),
                                             ("in", "  In-order"),
                                             ("post", "  Post-order"))):
            bottom.columnconfigure(col, weight=1, uniform="traversal")
            frame, canvas = self._panel(bottom, title)
            frame.grid(row=0, column=col, sticky="nsew",
                       padx=(0 if col == 0 else 6, 0))
            canvas.config(width=10, height=62)
            self.trav_canvases[name] = canvas

        for canvas in (self.tree_canvas, *self.trav_canvases.values()):
            canvas.bind("<Configure>", lambda _e: self.redraw())

    def _build_status(self):
        self.status = tk.Label(self, text="", bg=BG_PANEL, fg=MUTED, anchor="w",
                               font=(FONT, 9))
        self.status.pack(fill="x", side="bottom")

    def set_status(self, text, color=TEXT):
        self.status.config(text="  " + text, fg=color)

    # ---- actions
    def read_integer(self):
        """Return the integer typed in the entry or None (after showing an error)."""
        raw = self.entry_var.get().strip()
        if not INTEGER_PATTERN.match(raw):
            shown = raw if raw else "(empty)"
            messagebox.showerror(
                "Invalid Input",
                f"'{shown}' is not a valid integer.\n"
                "Only whole numbers are accepted (e.g. 15, -8, 42).",
                parent=self)
            self.set_status(f"'{shown}' is not a valid integer.", RED)
            self.entry.focus_set()
            return None
        return int(raw)

    def add_node(self):
        value = self.read_integer()
        if value is None:
            return
        self.highlight = {}
        try:
            level = self.tree.insert(value)
        except DuplicateNodeError:
            messagebox.showwarning(
                "Duplicate Node",
                f"Node {value} already exists in the tree.\n"
                "A binary search tree does not accept repeated values.",
                parent=self)
            self.set_status(f"Node {value} already exists.", ORANGE)
        except MaxDepthError:
            messagebox.showerror(
                "Maximum Depth Reached",
                f"Cannot insert node {value}.\n\n"
                f"This tree is limited to {MAX_LEVELS} levels.\n"
                f"Adding this node would create a level {MAX_LEVELS + 1}.\n\n"
                "Clear the tree or choose a different value.",
                parent=self)
            self.set_status(
                f"Cannot add {value}: maximum {MAX_LEVELS} levels reached.", RED)
        else:
            self.set_status(f"Node {value} added at level {level}.", GREEN)
        self.entry_var.set("")
        self.entry.focus_set()
        self.refresh()

    def search_node(self):
        value = self.read_integer()
        if value is None:
            return
        found, path = self.tree.search(value)
        self.highlight = {v: ORANGE for v in path}
        path_text = " \u2192 ".join(str(v) for v in path) if path else "(empty tree)"
        if found:
            self.highlight[value] = GREEN
            self.refresh()
            self.set_status(f"Node {value} found in the tree. \u2713", GREEN)
            messagebox.showinfo(
                "Node Found",
                f"Node {value} was found in the tree.\nSearch path: {path_text}",
                parent=self)
        else:
            self.refresh()
            self.set_status(f"Node {value} does not exist in the tree.", RED)
            messagebox.showinfo(
                "Node Not Found",
                f"Node {value} does not exist in the tree.\nSearch path: {path_text}",
                parent=self)

    def clear_tree(self):
        self.tree.clear()
        self.highlight = {}
        self.entry_var.set("")
        self.refresh()
        self.set_status("Tree cleared successfully.", MUTED)

    def exit_app(self):
        if messagebox.askyesno("Exit", "Do you want to close the application?",
                               parent=self):
            self.destroy()

    # ---- drawing
    def refresh(self):
        self.stats["Nodes"].config(text=str(self.tree.size))
        self.stats["Height"].config(text=str(self.tree.height()))
        root = self.tree.root.value if self.tree.root else "\u2014"
        self.stats["Root"].config(text=str(root))
        self.redraw()

    def redraw(self):
        self.draw_tree()
        self.draw_traversal(self.trav_canvases["pre"], self.tree.preorder())
        self.draw_traversal(self.trav_canvases["in"], self.tree.inorder())
        self.draw_traversal(self.trav_canvases["post"], self.tree.postorder())

    def draw_tree(self):
        canvas = self.tree_canvas
        canvas.delete("all")
        width, height = canvas.winfo_width(), canvas.winfo_height()
        if self.tree.root is None:
            canvas.create_text(width / 2, height / 2, text="Empty tree",
                               fill=MUTED, font=(FONT, 12))
            return

        top, bottom = 40, 40
        level_gap = max(60, (height - top - bottom) / (MAX_LEVELS - 1))
        positions = {}

        def place(node, level, index):
            if node is None:
                return
            slots = 2 ** level
            x = width * (2 * index + 1) / (2 * slots)
            y = top + level * level_gap
            positions[id(node)] = (x, y)
            place(node.left, level + 1, 2 * index)
            place(node.right, level + 1, 2 * index + 1)

        place(self.tree.root, 0, 0)

        def edges(node):
            if node is None:
                return
            for child in (node.left, node.right):
                if child is not None:
                    x1, y1 = positions[id(node)]
                    x2, y2 = positions[id(child)]
                    in_path = (node.value in self.highlight
                               and child.value in self.highlight)
                    canvas.create_line(x1, y1, x2, y2,
                                       fill=ORANGE if in_path else "#4a6a85",
                                       width=2)
                    edges(child)

        edges(self.tree.root)

        def nodes(node):
            if node is None:
                return
            x, y = positions[id(node)]
            text = str(node.value)
            r = max(20, 5 * len(text) + 8)
            color = self.highlight.get(node.value, CYAN)
            canvas.create_oval(x - r, y - r, x + r, y + r, fill=color,
                               outline="#e8f6fb", width=2)
            canvas.create_text(x, y, text=text, fill="#06141c",
                               font=(FONT, 11 if len(text) <= 3 else 9, "bold"))
            nodes(node.left)
            nodes(node.right)

        nodes(self.tree.root)

    def draw_traversal(self, canvas, values):
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if not values:
            canvas.create_text(width / 2, height / 2, text="No data",
                               fill=MUTED, font=(FONT, 9))
            return
        n = len(values)
        margin = 12
        step = (width - 2 * margin) / n
        r = max(6, min(16, step / 2 - 3))
        y = height / 2
        for i, value in enumerate(values):
            x = margin + step * (i + 0.5)
            if i < n - 1:
                nx = margin + step * (i + 1.5)
                if nx - x - 2 * r > 3:
                    canvas.create_line(x + r, y, nx - r, y, fill=MUTED,
                                       arrow=tk.LAST)
            canvas.create_oval(x - r, y - r, x + r, y + r, fill=YELLOW,
                               outline="#fff3c4", width=1)
            text = str(value)
            size = max(5, int(r * 0.75) - max(0, len(text) - 2))
            canvas.create_text(x, y, text=text, fill="#2b2100",
                               font=(FONT, size, "bold"))


def main():
    login = LoginWindow()
    login.mainloop()
    if login.authenticated:
        MainWindow().mainloop()


if __name__ == "__main__":
    main()
