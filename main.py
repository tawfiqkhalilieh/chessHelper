import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
import chess
import chess.engine

moves = {
    "list": [],
    "count": 0
}

# Create a window
window = tk.Tk()

# Set the title of the window
window.title("Chess Move Suggester")

# create a webdriver instance
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.chess.com/play/computer")

# Create a function to show the main page
def show_main_page():

    # Hide the start page
    start_frame.pack_forget()

    # Show the main page
    main_frame.pack()

# Create a function to update the label with new moves
def update_moves():

    # create a chess board and configure the engine
    chess_board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(r"fish.exe")
    engine.configure(
        {
            "UCI_LimitStrength": True, 
            "UCI_Elo": 2400
        }
    )
    count = int(driver.find_element(By.CLASS_NAME, "selected").get_attribute("data-ply"))
    for i in range(1,count+1):
        chess_board.push_san(
            driver.find_element(
                By.CSS_SELECTOR, f'[data-ply="{i}"]'
            ).text
        )
    
    print(chess_board)
    # get the top 3 engine moves
    analysis = engine.analyse(chess_board, chess.engine.Limit(time=2.0), multipv=3)
    top_moves = [ str(m["pv"][0]) for m in analysis ]
    text_label.config(text=f"Best Moves I found:\n1. {top_moves[0]}\n2. {top_moves[1]}\n3. {top_moves[2]}")

# Create a frame for the start page
start_frame = tk.Frame(window)

# Create a label for the start page
start_label = tk.Label(start_frame, text="Welcome to the Chess Move Suggester!")
start_label.pack()

# Create a button for the start page
start_button = tk.Button(start_frame, text="Start", command=show_main_page)
start_button.pack()

# Pack the start frame
start_frame.pack()

# Create a frame for the main page
main_frame = tk.Frame(window)

# Create a label for the main page
text_label = tk.Label(main_frame, text="Best Moves I found:\n1. \n2. \n3. ")
text_label.pack()

# Create a button to trigger the update of the label text
update_button = tk.Button(main_frame, text="Update", command=update_moves)
update_button.pack()

# Pack the main frame
main_frame.pack_forget()


# Start the main loop of the window
window.mainloop()
