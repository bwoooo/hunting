import json
import random
import os
import time
import sys

class MonsterHuntingGame:
    def __init__(self):
        self.hunt_file = "monster_hunts.json"
        self.hunts = self.load_hunts()
    
    def load_hunts(self):
        """Load existing hunts from file or create empty dict if file doesn't exist"""
        if os.path.exists(self.hunt_file):
            try:
                with open(self.hunt_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def save_hunts(self):
        """Save hunts to file"""
        with open(self.hunt_file, 'w') as f:
            json.dump(self.hunts, f, indent=2)
    
    def display_open_hunts(self):
        """Display all open hunts"""
        print("\nOpen Hunts:")
        for i, (monster_name, hunt_data) in enumerate(self.hunts.items(), 1):
            marks_collected = hunt_data['marks_collected']
            total_marks = hunt_data['total_marks']
            print(f"{i}. {monster_name} - {marks_collected}/{total_marks} marks")
    
    def select_hunt(self):
        """Let player select which hunt to continue"""
        hunt_list = list(self.hunts.keys())
        
        if len(hunt_list) == 1:
            selected_hunt = hunt_list[0]
            print(f"\nLoading hunt: {selected_hunt}")
            return selected_hunt
        
        while True:
            try:
                choice = int(input("\nSelect hunt number: ")) - 1
                if 0 <= choice < len(hunt_list):
                    return hunt_list[choice]
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def create_new_hunt(self):
        """Create a new monster hunt"""
        monster_name = input("\nEnter the monster name: ").strip()
        
        while True:
            try:
                total_marks = int(input("How many marks is this hunt worth? "))
                if total_marks > 0:
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
        
        self.hunts[monster_name] = {
            'marks_collected': 0,
            'total_marks': total_marks
        }
        self.save_hunts()
        return monster_name
    
    def display_hunt_details(self, monster_name):
        """Display current hunt details"""
        hunt_data = self.hunts[monster_name]
        print(f"\n--- Hunt Details ---")
        print(f"Monster: {monster_name}")
        print(f"Marks: {hunt_data['marks_collected']}/{hunt_data['total_marks']}")
    
    def dice_rolling_animation(self):
        """Display a dice rolling animation"""
        dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
        
        print("\n🎲 Rolling the dice...", end="", flush=True)
        
        # Show rolling animation
        for i in range(15):  # Roll for about 1.5 seconds
            dice = random.choice(dice_faces)
            print(f"\r🎲 Rolling the dice... {dice}", end="", flush=True)
            time.sleep(0.1)
        
        print()  # New line after animation
        time.sleep(0.5)  # Brief pause before showing result
    
    def roll_hunt_outcome(self):
        """Roll for hunt outcome and return result"""
        roll = random.randint(1, 6)
        
        outcomes = {
            1: "Major setback",
            2: "Mark, minor setback",
            3: "Mark",
            4: "Double marks",
            5: "Minor setback",
            6: "Double marks, boon"
        }
        
        return roll, outcomes[roll]
    
    def check_setback(self, setback_type):
        """Check if setback actually occurs"""
        roll = random.randint(1, 4)
        if roll in [1, 2]:
            return False  # No setback
        else:
            return True   # Setback occurs
    
    def process_outcome(self, monster_name, roll, outcome):
        """Process the hunt outcome and update marks"""
        hunt_data = self.hunts[monster_name]
        marks_gained = 0
        setback_occurred = False
        
        print(f"\nRoll: {roll}")
        print(f"Outcome: {outcome}")
        
        # Process marks first
        if "Mark" in outcome:
            if "Double marks" in outcome:
                marks_gained = 2
                print("You gained 2 marks!")
            else:
                marks_gained = 1
                print("You gained 1 mark!")
            
            # Update marks
            hunt_data['marks_collected'] += marks_gained
            self.save_hunts()
        
        # Process setbacks
        if "Major setback" in outcome:
            if self.check_setback("major"):
                print("Major setback occurs!")
                setback_occurred = True
            else:
                print("Major setback avoided!")
        
        elif "minor setback" in outcome:
            if self.check_setback("minor"):
                print("Minor setback occurs!")
                setback_occurred = True
            else:
                print("Minor setback avoided!")
        
        # Process boon
        if "boon" in outcome:
            print("You received a boon!")
        
        return marks_gained, setback_occurred
    
    def is_hunt_complete(self, monster_name):
        """Check if hunt is complete"""
        hunt_data = self.hunts[monster_name]
        return hunt_data['marks_collected'] >= hunt_data['total_marks']
    
    def complete_hunt(self, monster_name):
        """Complete the hunt and remove from active hunts"""
        print(f"\n🎉 Hunt Complete! You have successfully hunted the {monster_name}!")
        del self.hunts[monster_name]
        self.save_hunts()
    
    def run_game(self):
        """Main game loop"""
        print("=== D&D Monster Hunting ===")
        
        # Check if there are open hunts
        if self.hunts:
            print("\nWould you like to:")
            print("1. Continue an open hunt")
            print("2. Start a new hunt")
            
            while True:
                choice = input("\nEnter your choice (1 or 2): ").strip()
                if choice == "1":
                    self.display_open_hunts()
                    monster_name = self.select_hunt()
                    break
                elif choice == "2":
                    monster_name = self.create_new_hunt()
                    break
                else:
                    print("Please enter 1 or 2.")
        else:
            print("\nNo open hunts found. Starting a new hunt...")
            monster_name = self.create_new_hunt()
        
        # Display hunt details
        self.display_hunt_details(monster_name)
        
        # Wait for player to be ready
        input("\nPress Enter when you're ready to roll...")
        
        # Show dice rolling animation
        self.dice_rolling_animation()
        
        # Roll and process outcome
        roll, outcome = self.roll_hunt_outcome()
        marks_gained, setback_occurred = self.process_outcome(monster_name, roll, outcome)
        
        # Display final results
        hunt_data = self.hunts.get(monster_name, {'marks_collected': 0, 'total_marks': 0})
        print(f"\n--- Final Results ---")
        print(f"Monster: {monster_name}")
        print(f"Total Marks: {hunt_data['marks_collected']}/{hunt_data['total_marks']}")
        
        # Check if hunt is complete
        if monster_name in self.hunts and self.is_hunt_complete(monster_name):
            self.complete_hunt(monster_name)
        
        print("\nThanks for playing!")

def main():
    game = MonsterHuntingGame()
    game.run_game()

if __name__ == "__main__":
    main()