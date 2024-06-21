import time
import threading
import tkinter as tk
from tkinter import ttk

# Initialize global variables
coins = 50
earn_per_tap = 1
energy = 100
energy_limit = 100
regeneration_speed = 5
lock = threading.Lock()

# Initialize upgrade costs
upgrade_tap_cost = 10
refill_energy_cost = energy_limit / 10
increase_energy_limit_cost = 10
quicken_regeneration_cost = 10

# Function to add coins when the button is pressed
def add_coins():
    global coins, energy, earn_per_tap
    with lock:
        if energy >= 1:
            coins += earn_per_tap
            coinValue.config(text=f"{int(coins)} coins")
            energy -= 1
            energyValue.config(text=f"{energy}/{energy_limit}")
            energyBar['value'] = energy

# Function to regenerate energy over time
def regenerate_energy():
    global energy, energy_limit, regeneration_speed
    while True:
        with lock:
            current_speed = regeneration_speed
        time.sleep(current_speed)
        with lock:
            if energy < energy_limit:
                energy += 1
                energyValue.config(text=f"{energy}/{energy_limit}")
                energyBar['value'] = energy

# Function to upgrade the amount earned per tap
def upgrade_tap():
    global coins, earn_per_tap, upgrade_tap_cost
    with lock:
        if coins >= upgrade_tap_cost:
            coins -= upgrade_tap_cost
            earn_per_tap += 1
            upgrade_tap_cost += 5
            coinValue.config(text=f"{int(coins)} coins")
            earnPerTapValue.config(text=f"{earn_per_tap} coins")
            upgradeTapButton.config(text=f"Upgrade Tap\n{upgrade_tap_cost} coins")

# Function to refill energy
def refill_energy():
    global coins, energy, energy_limit, refill_energy_cost
    with lock:
        if coins >= refill_energy_cost and energy != energy_limit:
            coins -= refill_energy_cost
            energy = energy_limit
            coinValue.config(text=f"{int(coins)} coins")
            energyValue.config(text=f"{energy}/{energy_limit}")
            energyBar['value'] = energy

# Function to increase the energy limit
def increase_energy_limit():
    global coins, energy_limit, increase_energy_limit_cost, refill_energy_cost
    with lock:
        if coins >= increase_energy_limit_cost:
            coins -= increase_energy_limit_cost
            coinValue.config(text=f"{int(coins)} coins")
            energy_limit += 10
            energyValue.config(text=f"{energy}/{energy_limit}")
            energyBar.config(maximum=energy_limit)
            increase_energy_limit_cost += 5
            increaseEnergyLimitButton.config(text=f"Increase Energy Limit\n{increase_energy_limit_cost} coins")
            refill_energy_cost = energy_limit / 10 
            refillEnergyButton.config(text=f"Refill Energy\n{int(refill_energy_cost)} coins")

# Function to quicken the regeneration speed
def quicken_regeneration():
    global coins, regeneration_speed, quicken_regeneration_cost
    with lock:
        if coins >= quicken_regeneration_cost and regeneration_speed > 0.5:
            coins -= quicken_regeneration_cost
            regeneration_speed -= 0.5
            quicken_regeneration_cost += 10 
            coinValue.config(text=f"{int(coins)} coins")
            energyRegenerationValue.config(text=f"{regeneration_speed:.1f} seconds")
            if regeneration_speed == 0.5:
                quickenRegenerationButton.config(text="Quicken Regeneration\nMaximum Level")
            else:
                quickenRegenerationButton.config(text=f"Quicken Regeneration\n{quicken_regeneration_cost} coins")

# Initialize the main window
root = tk.Tk()
root.title("Game")
root.geometry('333x645')
root.resizable(False, False)

# Create the main frame for the game
gameFrame = tk.Frame(root)
gameFrame.grid(row=0, column=0)

# Create a frame for displaying earn per tap value
earnPerTapFrame = tk.Frame(gameFrame, highlightbackground="black", highlightthickness=1)
earnPerTapFrame.grid(row=0, column=0, padx=(10, 0), pady=10)

earnPerTapLabel = tk.Label(earnPerTapFrame, text="Earn Per Tap", width=18)
earnPerTapLabel.grid(row=0, column=0)

earnPerTapValue = tk.Label(earnPerTapFrame, text=f"{earn_per_tap} coins")
earnPerTapValue.grid(row=1, column=0)

# Create a frame for displaying energy regeneration speed
energyRegenerationFrame = tk.Frame(gameFrame, highlightbackground="black", highlightthickness=1)
energyRegenerationFrame.grid(row=0, column=1, padx=(10, 0), pady=10)

energyRegenerationLabel = tk.Label(energyRegenerationFrame, text="Energy Regeneration", width=18)
energyRegenerationLabel.grid(row=0, column=0)

energyRegenerationValue = tk.Label(energyRegenerationFrame, text=f"{regeneration_speed} seconds")
energyRegenerationValue.grid(row=1, column=0)

# Create a frame for displaying the coin count
coinFrame = tk.Frame(gameFrame, highlightbackground="black", highlightthickness=1)
coinFrame.grid(row=2, column=0, columnspan=2, padx=(10, 0), pady=10)

coinValue = tk.Label(coinFrame, text=f"{coins} coins", font=('Helvetica 22'), width=18)
coinValue.grid(row=0, column=0, pady=(10, 0))

# Create a button to earn coins
earnButton = tk.Button(coinFrame, text="Tap to Earn", height=2, width=36, command=add_coins)
earnButton.grid(row=1, column=0, pady=(10, 10))

# Create a frame for displaying energy
energyFrame = tk.Frame(gameFrame, highlightbackground="black", highlightthickness=1)
energyFrame.grid(row=4, column=0, columnspan=2, padx=(10, 0), pady=10)

energyLabel = tk.Label(energyFrame, text="Energy")
energyLabel.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

energyValue = tk.Label(energyFrame, text=f"{energy}/{energy_limit}")
energyValue.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="e")

energyBar = ttk.Progressbar(energyFrame, length=290, maximum=energy_limit)
energyBar.grid(row=5, column=0, columnspan=2, padx=10, pady=(10, 10))
energyBar['value'] = energy

# Create a frame for upgrade buttons
upgradesFrame = tk.Frame(gameFrame, highlightbackground="black", highlightthickness=1)
upgradesFrame.grid(row=6, column=0, columnspan=2, padx=(10, 0), pady=10)

upgradesLabel = tk.Label(upgradesFrame, text="Upgrades", width=38)
upgradesLabel.grid(row=0, column=0, pady=(10, 0))

upgradeTapButton = tk.Button(upgradesFrame, text="Upgrade Tap\n10 coins", width=36, command=upgrade_tap)
upgradeTapButton.grid(row=1, column=0, pady=(10, 0))

refillEnergyButton = tk.Button(upgradesFrame, text=f"Refill Energy\n{int(refill_energy_cost)} coins", width=36, command=refill_energy)
refillEnergyButton.grid(row=2, column=0, pady=(10, 0))

increaseEnergyLimitButton = tk.Button(upgradesFrame, text="Increase Energy Limit\n10 coins", width=36, command=increase_energy_limit)
increaseEnergyLimitButton.grid(row=3, column=0, pady=(10, 0))

quickenRegenerationButton = tk.Button(upgradesFrame, text="Quicken Regeneration\n10 coins", width=36, command=quicken_regeneration)
quickenRegenerationButton.grid(row=4, column=0, pady=(10, 10))

# Start the energy regeneration thread
t = threading.Thread(target=regenerate_energy)
t.daemon = True
t.start()

# Run the main loop
root.mainloop()
