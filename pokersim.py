import random

class Player:
    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.hand_score = 0  # Numerical representation of hand strength
        self.cards = []

    def __repr__(self):
        return f"{self.name} (Score: {self.hand_score})"

class PokerGameEngine:
    """
    The Core Data Structure Project.
    Implements a Max Heap with a Hash Map to support O(log N) arbitrary updates and deletes.
    """
    def __init__(self):
        # The Binary Tree stored as an array (Resume Point: "via binary trees/arrays")
        self.heap = []
        
        # The Lookup Table (Resume Point: "Supported updates/deletions")
        # Maps player_id -> index in self.heap array
        self.position_map = {}

    def _parent(self, i): return (i - 1) // 2
    def _left(self, i): return 2 * i + 1
    def _right(self, i): return 2 * i + 2

    def _swap(self, i, j):
        """Swaps two nodes in the heap and updates their position in the map."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        
        # Update the auxiliary map with new indices
        p1, p2 = self.heap[i], self.heap[j]
        self.position_map[p1.player_id] = i
        self.position_map[p2.player_id] = j

    def _sift_up(self, i):
        """Moves a node up to its correct position (O(log N))."""
        while i > 0 and self.heap[i].hand_score > self.heap[self._parent(i)].hand_score:
            self._swap(i, self._parent(i))
            i = self._parent(i)

    def _sift_down(self, i):
        """Moves a node down to its correct position (O(log N))."""
        max_idx = i
        l, r = self._left(i), self._right(i)
        size = len(self.heap)

        if l < size and self.heap[l].hand_score > self.heap[max_idx].hand_score:
            max_idx = l
        if r < size and self.heap[r].hand_score > self.heap[max_idx].hand_score:
            max_idx = r

        if i != max_idx:
            self._swap(i, max_idx)
            self._sift_down(max_idx)

    # --- PUBLIC INTERFACE (The Resume deliverables) ---

    def add_player(self, player):
        """O(log N) - Adds a player to the game."""
        self.heap.append(player)
        index = len(self.heap) - 1
        self.position_map[player.player_id] = index
        self._sift_up(index)

    def get_winner(self):
        """O(1) - Returns the current leader."""
        return self.heap[0] if self.heap else None

    def fold_player(self, player_id):
        """
        O(log N) - Deletion.
        Resume Point: "Supported deletions in O(log N)"
        """
        if player_id not in self.position_map:
            return
        
        index = self.position_map[player_id]
        last_idx = len(self.heap) - 1
        
        print(f"[FOLD] {self.heap[index].name} has folded.")

        # Swap target with the last element
        self._swap(index, last_idx)
        
        # Remove the last element (which is now the folded player)
        self.heap.pop()
        del self.position_map[player_id]

        # Rebalance heap if the folded player wasn't already the last one
        if index < len(self.heap):
            self._sift_up(index)
            self._sift_down(index)

    def update_hand_strength(self, player_id, new_score):
        """
        O(log N) - Update Key.
        Resume Point: "Supported updates in O(log N)"
        Used when Flop/Turn/River cards change a player's hand strength.
        """
        if player_id not in self.position_map:
            return

        index = self.position_map[player_id]
        old_score = self.heap[index].hand_score
        self.heap[index].hand_score = new_score
        
        print(f"[UPDATE] {self.heap[index].name}'s score changed: {old_score} -> {new_score}")

        if new_score > old_score:
            self._sift_up(index)
        else:
            self._sift_down(index)


# --- SIMULATION DRIVER ---
# This simulates the Texas Hold'em Game flow to prove functionality.

def simulate_game():
    game = PokerGameEngine()
    
    # 1. Setup Players
    players = [
        Player(1, "Alice"),
        Player(2, "Bob"),
        Player(3, "Charlie"),
        Player(4, "Dave")
    ]
    
    print("--- Dealing Hole Cards (Pre-Flop) ---")
    # Simulate dealing cards and assigning initial random strengths
    for p in players:
        p.hand_score = random.randint(100, 500) 
        game.add_player(p)
    
    print(f"Current Leader: {game.get_winner()}\n")

    # 2. The Flop (Updates)
    print("--- The Flop (3 Community Cards Revealed) ---")
    # Scenario: Alice hits a set (score increases drastically)
    game.update_hand_strength(1, 850)
    print(f"Current Leader: {game.get_winner()}\n")

    # 3. Betting Round (Deletion/Fold)
    print("--- Betting Round ---")
    # Scenario: Dave has a bad hand and folds
    game.fold_player(4) 
    print(f"Remaining Players: {len(game.heap)}\n")

    # 4. The Turn (Updates)
    print("--- The Turn (4th Card) ---")
    # Scenario: Charlie gets a flush draw (score increases moderately)
    game.update_hand_strength(3, 900)
    print(f"Current Leader: {game.get_winner()}\n")
    
    # 5. The River (Updates)
    print("--- The River (5th Card) ---")
    # Scenario: Bob misses his draw, score stays same. Charlie completes Flush.
    game.update_hand_strength(3, 1200) # Charlie hits Flush
    
    print("--- SHOWDOWN ---")
    winner = game.get_winner()
    print(f"WINNER: {winner.name} with score {winner.hand_score}")

if __name__ == "__main__":
    simulate_game()
