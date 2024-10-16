import os
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Configuration constants
NUM_PAIRS = 6
MIN_CORRECT = 3
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 1000
IMAGE_WIDTH = 520
IMAGE_HEIGHT = 780
BACKGROUND_COLOR = "#2e2e2e"  # Dark gray background
TEXT_COLOR = "#ffffff"  # White text for better contrast

# Function to load random image pairs from AI and Real folders without repeating
def load_image_pairs(ai_folder, real_folder):
    ai_images = os.listdir(ai_folder)
    real_images = os.listdir(real_folder)

    if len(ai_images) < NUM_PAIRS or len(real_images) < NUM_PAIRS:
        raise ValueError(f"Not enough images. Both folders must contain at least {NUM_PAIRS} images.")

    # Randomly select unique images for the pairs
    selected_ai_images = random.sample(ai_images, NUM_PAIRS)
    selected_real_images = random.sample(real_images, NUM_PAIRS)

    pairs = [(os.path.join(ai_folder, ai), os.path.join(real_folder, real)) 
             for ai, real in zip(selected_ai_images, selected_real_images)]

    return pairs

# Main class for the Captcha application
class CaptchaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Captcha Test")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=BACKGROUND_COLOR)

        # Variables to track the current pair and correct answers
        self.pairs = load_image_pairs('AI', 'Real')
        self.current_pair = 0
        self.correct_answers = 0

        # Title and instructions
        self.title_label = tk.Label(root, text="One picture is real and the other one is AI Generated", 
                                    font=("Arial", 20), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.title_label.pack(pady=10)

        self.instruction_label = tk.Label(root, text="Choose the real picture", font=("Arial", 18), 
                                          bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.instruction_label.pack(pady=5)

        # Frame for images and buttons
        self.image_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        self.image_frame.pack(pady=20)

        self.left_image_label = tk.Label(self.image_frame, bg=BACKGROUND_COLOR)
        self.right_image_label = tk.Label(self.image_frame, bg=BACKGROUND_COLOR)
        self.left_image_label.grid(row=0, column=0, padx=20)
        self.right_image_label.grid(row=0, column=1, padx=20)

        self.left_button = tk.Button(self.image_frame, text="Choose", command=lambda: self.check_answer('left'),
                                     bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.left_button.grid(row=1, column=0, pady=10)

        self.right_button = tk.Button(self.image_frame, text="Choose", command=lambda: self.check_answer('right'),
                                      bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.right_button.grid(row=1, column=1, pady=10)

        # Show the first pair of images
        self.show_next_pair()

    # Function to display the next pair of images
    def show_next_pair(self):
        if self.current_pair < NUM_PAIRS:
            ai_image_path, real_image_path = self.pairs[self.current_pair]
            
            # Randomize the position of the AI and Real image
            left_image_path, right_image_path = random.choice([(ai_image_path, real_image_path), (real_image_path, ai_image_path)])
            
            # Load and display the images
            left_image = Image.open(left_image_path)
            right_image = Image.open(right_image_path)
            left_image = left_image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
            right_image = right_image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
            
            left_image_tk = ImageTk.PhotoImage(left_image)
            right_image_tk = ImageTk.PhotoImage(right_image)
            
            self.left_image_label.config(image=left_image_tk)
            self.right_image_label.config(image=right_image_tk)
            
            # Keep a reference to prevent garbage collection
            self.left_image_label.image = left_image_tk
            self.right_image_label.image = right_image_tk

            # Store the correct image path for comparison
            self.real_image = real_image_path
            self.left_is_real = left_image_path == real_image_path
        else:
            self.show_result()

    # Function to check the user's choice
    def check_answer(self, choice):
        if choice == 'left' and self.left_is_real:
            self.correct_answers += 1
        elif choice == 'right' and not self.left_is_real:
            self.correct_answers += 1

        self.current_pair += 1
        self.show_next_pair()

    # Function to display the final result
    def show_result(self):
        if self.correct_answers >= MIN_CORRECT:
            messagebox.showinfo("Result", "You are human!")
        else:
            messagebox.showinfo("Result", "You are a robot!")
        self.root.quit()

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CaptchaApp(root)
    root.mainloop()
