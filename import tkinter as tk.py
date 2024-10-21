import tkinter as tk
import random

# Create the main game window
class BalloonPopperGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Balloon Popper Game")

        # Create a canvas with a gradient background
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()

        self.create_gradient()

        self.score = 0
        self.time_left = 60
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.pack()

        self.time_label = tk.Label(root, text=f"Time Left: {self.time_left}", font=("Arial", 14))
        self.time_label.pack()

        self.balloons = []
        self.balloon_ids = []
        self.create_balloon()

        # Update ballon positionss
        self.update_balloons()

        # Bind mouse clicks to balloon popping
        self.canvas.bind("<Button-1>", self.pop_balloon)

        # Countdown timer for the game
        self.update_timer()

    def create_gradient(self):
        """Create a gradient background."""
        for i in range(500):
            red = hex(int(i / 2)).replace('0x', '').zfill(2)
            blue = hex(255 - int(i / 2)).replace('0x', '').zfill(2)
            color = f"#{red}00{blue}"
            self.canvas.create_line(0, i, 500, i, fill=color)

    def create_balloon(self):
        """"Create a balloon at a random location."""
        for _ in range(5):
            x = random.randint(50, 450)
            y = 500
            color = random.choice(["red", "green", "blue", "yellow", "purple"])
            balloon_id = self.canvas.create_oval(x - 20, y - 30, x + 20, y + 30, fill=color, outline="")
            self.balloons.append({"id": balloon_id, "x": x, "y": y, "speed": random.randint(1,3)})
            self.balloon_ids.append(balloon_id)

    def update_balloons(self):
        """"Update balloon positions and remove them if they leave the screen."""
        for balloon in self.balloons:
            self.canvas.move(balloon["id"], 0, -balloon["speed"])
            balloon["y"] -= balloon["speed"]

        # Remove balloons that go off-screen and create new ones
        self.balloons = [balloon for balloon in self.balloons if balloon["y"] > -30]
        if len(self.balloons) < 5:
            self.create_balloon()

        self.root.after(50, self.update_balloons)

    def pop_balloon(self, event):
        """"Check if a balloon was clicked and  remove it."""
        items = self.canvas.find_overlapping(event.x, event.y, event.x + 1, event.y + 1)

        for item in items:
            if item in self.balloon_ids:
                self.canvas.delete(item)
                self.balloon_ids.remove(item)
                self.balloons = [balloon for balloon in self.balloons if balloon["id"] != item]
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                break

    def update_timer(self):
        """Update the countdown time."""
        if self.time_left> 0:
           self.time_left -= 1
           self.time_label.config(text=f"Time Left: {self.time_left}")
           self.root.after(1000, self.update_timer)
        else:
           self.end_game()

    def end_game(self):
        """End the game when time is up."""
        self.canvas.unbind("<Button-1>")
        self.canvas.create_text(250, 250, text="Game Over!", font=("Arial, 24"), fill="white")
        self.canvas.create_text(250, 300, text=f"Final Score: {self.score}", font=("Arial", 20), fill="white")

# Initialize and run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = BalloonPopperGame(root)
    root.mainloop()        

