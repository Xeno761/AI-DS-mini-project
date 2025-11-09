from maze_generator import MazeGenerator
from algorithms import MazeSolver
from visualizer import MazeVisualizer

def main():
    print("="*70)
    print(" "*15 + "INTERACTIVE MAZE SOLVER - DFS vs BFS")
    print("="*70)
    print("\nSelect maze type:")
    print("  1. Perfect Maze (one unique path)")
    print("  2. Multi-Path Maze (multiple routes, BFS finds shortest)")

    choice = input("Enter choice [1 or 2, default 1]: ").strip() or "1"
    maze_type = int(choice) if choice in ["1", "2"] else 1

    running = True
    maze_size_index = 0
    # Both types now have three sizes, same as before
    maze_sizes = [
        (8, 8, "SMALL"),
        (12, 12, "MEDIUM"),
        (20, 20, "LARGE")
    ]

    while running:
        width, height, size_name = maze_sizes[maze_size_index]
        maze_gen = MazeGenerator(width, height)
        maze = maze_gen.get_maze(maze_type=maze_type)
        maze_cells = max(maze.shape[0], maze.shape[1])
        target_size = 450
        cell_size = max(1, target_size // maze_cells)

        maze_title = f"{size_name} {'Multi-Path' if maze_type == 2 else 'Perfect'} Maze"

        print(f"\n{'='*70}")
        print(f"Generating {maze_title}...")
        print(f"Cell size: {cell_size}px | Maze dimensions: {maze.shape}")

        solver = MazeSolver(maze)
        visualizer = MazeVisualizer(maze, cell_size=cell_size, maze_size=maze_title)

        print(f"✓ Start: {visualizer.start} | End: {visualizer.end}")
        print("-"*70)

        result = visualizer.run_interactive(solver)

        if result == "NEW_MAZE":
            print("\n► Generating new maze...\n")
            maze_size_index = (maze_size_index + 1) % len(maze_sizes)
            continue
        else:
            running = False

        visualizer.quit()

    print("\n" + "="*70)
    print(" "*20 + "✓ Thank you for using Maze Solver!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
