# Pygame Ghouls 'n Ghosts
#### Video Demo (CS50P Final Project): https://youtu.be/1SQpq-fdN_I
#### Description: An arcade-style game inspired by the classic Super Ghouls 'n Ghosts. It features simple rogue-like elements and character progression, encouraging players to replay and compete for the highest score.


## Overview
This project is a game created with the Pygame library, inspired by Capcom's Ghosts ‘n Goblins series, particularly based on **Super Ghouls ‘n Ghosts** released in 1991 for the Super Nintendo Entertainment System (SNES). Most assets, such as sprites, art, tiles, and sounds, were obtained from rips and screenshots of the original game found on the internet.

***Pygame Ghouls ‘n Ghosts*** is an arcade-style game where the player controls Arthur, who needs to survive hordes of enemy monsters and defeat as many as possible of them to achieve the highest score possible before he inevitably succumbs to the odds.

Throughout the game, players can collect **items** to increase Arthur’s *damage, speed, hit points*, and discover other *weapons* to help overcome the challenge of staying alive. The game also features a **leaderboard** system that stores the top ten highest scores and the names of the players who achieved them.


## Design and Vision

### Concept

The inspiration for this game came from my desire to recreate and enhance an older Scratch project of mine called *Scratch Ghouls 'n Ghosts*, that was a simple game where players controlled a knight battling skeleton enemies to increase their final score. While that project featured music and a logo reminiscent of *Super Ghouls 'n Ghosts*, it did not go beyond those thematic elements.

With *Pygame Ghouls 'n Ghosts*, my aim is to more closely capture the look and feel of the original game and pay homage to this 90s classic. By utilizing assets from the source material, I strive to create a more nostalgic experience for players, while also  introducing new features and ideas to enhance gameplay and add replayability. 

### Features and Changes:

-  **Expanded Gameplay:** New mechanics such as character leveling and the ability to swap between different weapons, add a layer of depth and strategy to the game.

- **Arcade Experience:** Survive and kill hordes of enemies on an arena map, and compete with other players for a place on the leaderboard.

- **Improved Controls:** Control customization options that provide a more personalized and fluid gaming experience.

- **Replayability:** Short playthroughs with progressive challenges and dynamic elements like enemy spawns and item drops, ensuring each session feels unique and engaging.


## Structure

### Object-Oriented Design

This project is developed using an Object-Oriented Programming (OOP) approach, ensuring the codebase is modular, maintainable, and scalable. By utilizing classes for various game components, it becomes easier to manage and extend the game’s features. Here are some key aspects of the structure:

- **Classes for Core Components:** Each core element of the game, such as the player, enemies, weapons, and items, is encapsulated within its own class. This separation allows for cleaner code and simplifies testing.

- **Scalability:** As the game evolves, new gameplay mechanics and features can be introduced with minimal disruption to the existing code. The class-based structure supports scalability, ensuring that the game can grow in complexity over time without becoming unwieldy.

- **Modularity:** The use of classes promotes a modular design where new features, such as additional enemy types, weapons, or abilities, can be more easily added or tweaked.

> I already have some ideas for new features that would be fun to add, such as:
> - A close-range weapon.
> - Special attacks unique to each weapon.
> - An ultimate magic attack.
> - Different arenas for more varied gameplay.
> - A dynamic platform system that changes the layout of the map in the middle of the playthrough.
> - New armors with different abilities, similar to the original game.


## Steps of the Program

### Initialization

The initialization phase sets up the game environment, loads necessary assets, and prepares the initial game state. This includes importing required libraries and modules, defining essential functions for loading images, and initializing the main game class.

- **Library Imports:** The necessary libraries and custom classes are imported at the beginning. This includes **`pygame`**, **`random`**, **`os`** and **`sys`**. Custom classes such as **`Animation`**, **`Player`**, and various game entities are also imported.

- **Asset Loading Functions:** Functions to load images and animations from the asset directory are defined. **`load_image`** loads a single image, applies a color key for transparency, and scales it. **`load_images`** load multiple images, returning them as a list (primarily used for the animations). **`load_images_dict`** load multiple images, returning them as a dictionary (used for the font images).

- **Game Class Initialization:** The **`Game`** class initializes the game environment. This includes creating the game window, setting up the display, loading fonts (used for the `write` function), sound effects, animations, and other game assets. Variables to track the player's state, score, and controls are also initialized here.

- **Control Initialization:** The control inputs are defined in a dictionary (`self.inputs`), mapping actions to their corresponding key bindings.

The initialization sets the foundation for the game, ensuring all necessary assets, variables and settings are in place before transitioning to the game's different screens and main loop.

### Opening

The opening attempts to resemble the booting sequence from *Super Ghouls 'n Ghosts* for the *SNES*, swapping Capcom's logo with CS50's. This sequence consists of a fade-in and fade-out effect for the logo, accompanied by the original game's sound effect, followed by a transition to the main menu.


### Main Menu 

The main menu provides the player with options to start the game, view control settings, and see credits. It features a visual interface with selectable options and navigation using keyboard inputs.

- **Menu Layout:** Images for the logo, **`game start`** button, and **`control options`** are loaded and positioned on the screen. A selection cursor (*small spear*) is displayed next to the currently selected option.

- **Transition to Game or Controls Screen:** A variable called `select` keeps track of where the cursor should be and what section to load. Depending on the selected option, the game transitions to the main gameplay loop (`self.run()`) or the controls screen (`self.controls_screen()`).

 - **Sound Effects:** Different sound effects play for navigating the menu and for the selected button, providing audio feedback for user actions.


### Controls Screen

The controls screen allows players to view and change key bindings for various actions in the game. The interface is navigated using keyboard inputs, and changes can be saved and applied. Effort was put into making every selected action clear, and the sound effects provided great feedback.

- **Controls Layout:** Displays key bindings for actions like moving, jumping, crouching, shooting, and swapping weapons. Players can see the current bindings and navigate through them.

- **User Interaction:** The user navigates through the options and changes key bindings using the arrow keys (the `spacebar` also can be used to change the selected action). The selected action is highlighted using the different fonts.

- **Saving Changes:** When the Enter key is pressed or the `game start` button is selected, the new key bindings are saved to a **`controls.csv`** file. The game then starts with the updated controls.

- **Sound Effects:** Different sound effects play for navigating and changing selections, providing audio feedback for user actions.


### Game Running

The `run` method handles the main game loop, including the initialization and updating of game elements, managing player input, and rendering the game's graphics.

#### 1. Initialization:

- Initializes variables for handling the `name_prompt`, player movement, weapon selection, and various game entities (enemies, items, weapons), and call the `reset_variables()` function.

- Loads background images and other assets.

#### 2. Main Game Loop:

- Handles music transitions from the intro to the main game music.

- Fills the background with the map layers, and updates the player's position and state based on input and game events.

- Manages game entities like enemies, items, and weapons, including their creation (`create_horde()` and `item_drop()`), updating, and rendering.

#### 3. Name Prompt Handling:

- Activates when the player dies, prompting the player to input their name.

- Displays instructions and handles input for navigating and selecting characters to form the player's name.

- Updates the displayed name in real-time and allows confirmation of the entered name.

#### 4. Event Handling:

- Listens for various input events (keyboard and mouse) to control player actions, such as movement, and attacking.

- Includes special handling for the name prompt, allowing character selection and confirmation.


#### 5. Rendering:

- Draws all game elements, including the player, enemies, items, and background layers.

- Displays additional HUD elements and the name prompt as needed.

- Updates the display at a fixed frame rate (60 FPS).

During the game loop, various variables are constantly being updated to keep track of the current player stats that will be shown on the *Game Over Screen*. Some of these are:
```
self.score
self.horde
self.enemies_defeated
self.seconds
self.player.power_level
self.weapons_n_kills (dict)
```

### Game Over

The `game_over` method is responsible for handling the end-game sequence and showing the user their stats from the previous run, as well as the **leaderboard**.

#### 1. SFX and Load Images: 

-  Plays the "game over" music. 

- Loads and positions images, including the game over message, the "game start" button, and a selection spear icon.

#### 2. All-Time Scores Update:

- Checks if the current run's score should be added to the all-time scores (`all_scores.csv`). 

- This file saves the name and score of every player whose final score is more than 200. This condition is set to prevent clutter in the stored data.

- If the condition is met, it updates the list and writes the updated scores back to the CSV file.

#### 3. Leaderboard Update:

- If the current score is high enough to be in the top 10, it updates the local leaderboard list.

- Writes the updated leaderboard to `leaderboard.csv`.

#### 4. Stats Display:

- Displays the player's name, score, hordes cleared, enemies defeated, power level, speed level, and kills with various weapons.

- Also shows the elapsed time of the game session, measured using the `count_time()` function.

#### 5. Leaderboard Display:

- Shows the top 10 high scores with *ranks*, *scores*, and *player names*.

#### 6. Controls and Navigation:

- Displays control instructions for moving the cursor and selecting options.

- Handles user input to navigate and select options on the game over screen. If "game start" is selected, it restarts the game. If "control options" is selected, it navigates to the controls screen.

The *Game Over Screen* extensively uses the **`write()`** function to render all the text elements on the display. Many improvements to this function arose from the necessities encountered during the implementation of the elements required to provide all the end-game information to the user.


## Functions

Throughout the game loop, several custom functions are called at specific points in the game. These functions collectively manage the core mechanics of the game, such as resetting the game state, handling item and weapon drops, updating drop possibilities based on the player's state, and creating enemy hordes.


### `reset_variables()`
 Resets all necessary game variables to their initial states at the beginning of each game loop iteration. This ensures a clean slate for the game state.

 #### Score and Progress Variables:
  - `self.score`, `self.horde`, `self.enemies_defeated`: Track the player's score, current horde level, and the number of enemies defeated.

 #### Time Tracking:
  - `self.frames`, `self.seconds`, `self.minutes`: Track the in-game time.

 #### Items and Weapons:
  - `self.game_items`, `self.game_weapons`: Lists of possible items and weapons that can drop.
  - `self.weapon_roll`: A counter to track the probability of weapon drops.
  - `self.weapon_droped`: A flag to check if a weapon has already been dropped.
  - `self.weapons_n_kills`: Dictionary to track the number of kills made with each weapon.

 #### Item Drop Control:
  - `self.item_roll`, `self.hp_up_droped`, `self.speed_up_droped`, `self.power_up_droped`: Counters and flags for item drops.

 #### Player and Movement:
  - `self.player`, `self.movement`: Initializes the player with a random weapon and resets all its states.
  - `self.player_name`: Sets the player's default name to "arthur". 


### `item_drop()`
 Manages the logic for dropping items or weapons at a specified position when an enemy is defeated. This function handles the randomness and logic behind item drops based on the current game state and scores. 

 #### Weapon Drop Logic:
  - Checks if a weapon has not been dropped and evaluates the score to determine the possibility of dropping a weapon.
  - Calls `self.weapon_drop(enemy_pos)` to attempt a weapon drop.

 #### Item Drop Logic:
  - If no weapon is dropped, it attempts to drop an item by calling `self.upgrade_drop(enemy_pos)`.


### `weapon_drop()`
 Determines if a weapon should be dropped based on a random chance.

 #### Drop Chance Calculation:
  - Uses `self.weapon_roll` to determine the probability.
  - If `self.weapon_roll` reaches 0, a weapon is guaranteed to drop.
  - Otherwise, a random number from -8 to 1 is chosen to decide the drop and `self.weapon_roll` is decremented by 1.
  - If the random number chosen is greater than 0, a weapon is dropped.

 #### Weapon Drop Execution:
  - Resets `self.weapon_roll` and plays the weapon drop sound effect if a weapon is dropped.
  - Returns a WeaponDrop object with a randomly chosen weapon from the self.game_weapons list.


### `upgrade_drop()`
 Manages the logic for dropping upgrade items (e.g., PowerUp, SpeedUp).

 #### Drop Chance Calculation: 
  - Uses `self.item_roll` to determine the probability.
  - If `self.item_roll` reaches 0, an item is guaranteed to drop.
  - Otherwise, a random number from -5 to 1 is chosen to decide the drop and `self.item_roll` is decremented by 1.
  - If the random number chosen is greater than 0, a item is dropped.

 #### Item Drop Execution:
  - Resets `self.item_roll` and plays the item drop sound effect if an item is dropped.
  - Returns an `Item` object with the chosen item.


### `update_itemsToDrop()`
 Dynamically updates the list of items and weapons that can drop based on the player's current state and existing items.

 #### HP Up Item Logic:
  - Adds or removes `hp_up` from the drop list based on the player's health.
  - Ensures items are added back to the list if conditions change (e.g., player loses health).

 #### Upgrade Item Logic:
  - Adds or removes speed and power upgrades from the drop list based on the player's upgrade levels and if a item already dropped.

 #### Weapon Drop Logic:
  - Updates the list of droppable weapons based on the weapons the player already holds.


### `create_horde()`
 Generates a new horde of enemies based on the player's score and current horde level.

 #### Horde Size and Composition:
  - Determines the number of enemies in the horde and the types of enemies based on the score.
  - Sets limits for each type of enemy.

 #### Enemy Spawn Logic:
  - Determines the spawn location for each enemy type.
  - Creates enemy objects and adds them to the horde.

 #### Return Value:
  - Returns a list of enemy objects representing the new horde.


### `count_time()`
 Keeps track of the in-game time, and is called when the player is alive. Works by incrementing frame, second, and minute counters (assuming the game is running at 60 FPS).


### `write()`
 Responsible for rendering text or symbols on the screen at a specified position. It supports various options such as centering, left alignment, scaling, and compensation for different character widths. 

 #### Parameters:
  - `sentence`: The text or symbol to be rendered.
  - `position`: The (x, y) coordinates where the text or symbol will be displayed.
  - `surf`: The surface on which to render the text or symbol.
  - `font`: The font to be used for rendering. Default is "fontA".
  - `center`: Boolean flag to center the text. Default is `False`.
  - `left`: Boolean flag to left-align the text. Default is `False`.
  - `symbol`: Boolean flag indicating if the input is a symbol. Default is `False`.
  - `scale`: Scaling factor for the text or symbols. Default is `1.0`.
  - `compansate`: Boolean flag to adjust spacing for different character widths. Default is `True`.

 #### Functionality:
  1. **Initialize Variables**:
     - Converts the sentence to a string and creates a position list.
     - Initializes a dictionary `symbols_dict` to map special characters to their corresponding symbols.

  2. **Centering Logic**:
     - If centering is enabled, adjusts the starting x-position based on the length of the string and the width of the first character.

  3. **Left Alignment Logic**:
     - If left alignment is enabled, adjusts the starting x-position based on the length of the string.

  4. **Symbol Handling**:
     - If the input is a symbol, it directly scales and renders the symbol.

  5. **Text Rendering**:
     - Iterates over each character in the string:
       - Converts special characters to their corresponding symbols using `symbols_dict`.
       - Adjusts the x-position for spaces and certain characters.
       - Scales and renders each character, compensating for different widths if needed.
     - Stores the rendered characters in the `final_sentence` dictionary.

  6. **Blitting to Surface**:
     - If a surface is provided, it blits each character image to the surface.

  7. **Return Value**:
     - Returns a list containing the initial position, the first and last characters `x` positions, and the keys of the final rendered characters.

> This function is extensively used for displaying game information such as damage numbers, player names, and game instructions.


## Classes
Description of the classes imported from the `classes.py` file.


### `Animation`
 Responsible for handling animations in the game. It manages a sequence of images, updating them based on a specified duration and handling looping if required.

 #### Attributes:
  - `images`: A list of images that make up the animation.
  - `loop`: A boolean indicating whether the animation should loop.
  - `img_duration`: The duration each image is displayed.
  - `done`: A boolean indicating whether the animation is complete.
  - `frame`: The current frame of the animation.
  - `animation_Nframes`: The total number of frames in the animation.
  - `time`: A counter to manage the timing of frame changes.

 #### Methods:
  - `__init__(self, images, img_dur=8, loop=False, done=False)`: Initializes the animation with the given images, duration, looping option, and done status.
  - `copy(self)`: Returns a copy of the current animation.
  - `update(self)`: Updates the current frame of the animation based on the timing and looping options.
  - `sprite(self)`: Returns the current image of the animation based on the current frame.


### `PhysicsEntity`
 Serves as a base class for all entities in the game that have physical properties, such as position, size, and velocity. It manages the entity's movement, collision detection, and animations.

 #### Attributes:
  - `game`: Reference to the main game object.
  - `type`: The type of the entity.
  - `pos`: The position of the entity as a list `[x, y]`.
  - `size`: The size of the entity `[width, height]`.
  - `velocity`: The velocity of the entity `[x_velocity, y_velocity]`.
  - `collisions`: A dictionary to track collisions on each side (`top`, `bottom`, `right`, `left`).
  - `hit`: A dictionary to track hits on each side (`top`, `bottom`, `right`, `left`).
  - `flip`: Boolean to determine the direction of the entity.
  - `action`: The current action of the entity.
  - `bottom_tiles`: List to keep track of the platforms below the entity.

 #### Methods:
  - `__init__(self, game, e_type, pos, size)`: Initializes the physics entity with the game reference, type, position, and size.
  - `rect(self)`: Returns the rectangular area of the entity.
  - `set_action(self, action)`: Sets the current action and updates the corresponding animation.
  - `show_hitbox(self, surf, color=(0, 200, 0))`: Displays the hitbox of the entity on the surface `surf`.
  - `gravity(self, x=0.1)`: Applies gravity to the entity.
  - `update(self, movement=(0, 0), tiles=None, boundaries=None, entities=None)`: Updates the entity's position, handles collisions, and updates the animation.
  - `render(self, surf)`: Renders the entity on the surface `surf`.


### `Player(PhysicsEntity)`
 The `Player` class inherits from `PhysicsEntity` and represents the player character in the game. It includes additional attributes and methods specific to player actions, abilities, and upgrades.

 #### Attributes:
  - `power_level`: The current power level of the player.
  - `power_upgrade`: A dictionary mapping power levels to power multipliers.
  - `power`: The current power multiplier.
  - `speed_level`: The current speed level of the player.
  - `speed_upgrade`: A dictionary mapping speed levels to speed multipliers.
  - `speed`: The current speed multiplier.
  - `max_level`: Boolean indicating if both speed and power levels are at their maximum.
  - `hp`: The player's health points.
  - `dead`: Boolean indicating if the player is dead.
  - `crouch`: Boolean indicating if the player is crouching.
  - `pick_up`: Boolean indicating if the player is picking up an item.
  - `item_taken`: The item being picked up.
  - `weapon`: The current weapon equipped.
  - `weapons_held`: A list of weapons the player holds.
  - `current_weapon`: Index of the current weapon in `weapons_held`.
  - `cooldown`: A dictionary mapping each weapon to its cooldown time.
  - `renderPos_x`: X-axis adjustment for rendering the sprite.
  - `renderPos_y`: Y-axis adjustment for rendering the sprite.
  - `in_air`: Frames the player has been in the air.
  - `n_jumps`: Number of jumps available.
  - `current_jump_animation`: Current animation for the first jump.
  - `current_jumpD_animation`: Current animation for the double jump.
  - `throw`: Boolean indicating if the player is throwing a weapon.
  - `throw_animation_cooldown`: Cooldown for the throw animation.
  - `throw_cooldown`: Cooldown for the current weapon.
  - `tuck`: Boolean indicating if the player is tucking in the air.
  - `tuck_dur`: Duration for the tuck action.
  - `n_tucks`: Number of tucks available.
  - `knock_back`: Knockback effect on the player.
  - `hit_animation_dur`: Duration for the hit animation.
  - `hit_cooldown`: Invencibility frames after getting hit.
  - `damaged`: Boolean indicating if the player is damaged.

 #### Methods:
  - `__init__(self, game, pos, size, weapon)`: Initializes the player with the game reference, position, size, and initial weapon.
  - `set_action(self, action)`: Sets the current action and updates the corresponding animation, with special handling for when the player is hit or dead.
  - `update(self, movement=(0, 0), tiles=None, boundaries=None, entities=None)`: Updates the player's position, handles collisions, manages power and speed upgrades, checks for pickups, and updates animations based on actions like crouching, throwing, jumping, and tucking.
  - `attack(self)`: Handles the player's attack action with the current weapon.
  - `jump(self)`: Handles the player's jump action.
  - `knockback(self)`: Applies knockback effect when the player is hit.
  - `weapon_swap(self)`: Swaps to the next weapon in the player's inventory.
  - `power_up(self)`: Increases the player's power level.
  - `speed_up(self)`: Increases the player's speed level.
  - `hp_up(self)`: Increases the player's health points.
  - `upgrade(self, upgrade_item)`: Upgrades the player's abilities or adds new weapons based on the item picked up.
  - `rect(self)`: Returns the rectangular area of the player.
  - `render(self, surf)`: Renders the player on the surface `surf`, with special handling for invencibility frames, death animation, and jumps.


### `Enemy(PhysicsEntity)`
 The `Enemy` class inherits from `PhysicsEntity` and represents an enemy character in the game. It includes attributes and methods specific to enemy behavior, such as movement, damage handling, and rendering.

 #### Attributes:
  - `renderPos_x`: X-axis adjustment for rendering the sprite.
  - `renderPos_y`: Y-axis adjustment for rendering the sprite.
  - `damage_timer`: Timer for handling damage effects.
  - `damage_taken_write`: Amount of damage taken, written for display.
  - `blink_timer`: Timer for handling blinking effect when spawning.
  - `enemy_type`: The type of enemy.
  - `hp`: Health points of the enemy.
  - `spawn`: Boolean indicating if the enemy has spawned.
  - `moving`: Boolean indicating if the enemy is moving.
  - `move_direction`: Direction of movement; 0 for not moving, positive for right, negative for left.
  - `hit_weapon`: Weapon that hit the enemy.
  - `damage_taken`: Amount of damage taken.
  - `damaged`: Boolean indicating if the enemy is damaged.
  - `die`: Boolean indicating if the enemy is dead.
  - `delete`: Boolean indicating if the enemy should be deleted.
  - `activate_knockback`: Boolean to address a potential bug with entities changing size during knockback.
  - `knockback_taken`: Amount of knockback taken.
  - `knock_back`: Knockback effect on the enemy.
  - `hit_direction_right`: Boolean indicating the direction of the hit (right or left).

 #### Methods:
  - `__init__(self, game, enemy_type, pos, hp, size)`: Initializes the enemy with the game reference, enemy type, position, health points, and size.
  - `set_action(self, action)`: Sets the current action and updates the corresponding animation.
  - `update(self, movement=(0, 0), tiles=None, boundaries=None, entities=None)`: Updates the enemy's position, handles damage, checks if the enemy is dead, and updates animations based on actions like moving and knockback.
  - `knockback(self, knockback_amount)`: Applies knockback effect when the enemy is hit.
  - `render(self, surf)`: Renders the enemy on the surface `surf`, with special handling for damage effects, spawning, and death animations.


### Enemy types
 For every enemy type in the game, a subclass of the Enemy class is created. Here are the distinct attributes and methods for those classes:

 #### **`Zombie`**

  ##### Distinct Attributes:
   - `player_pos`: This attribute holds the position of the player, which may be used to determine the zombie's behavior or movements relative to the player.
   - `enemy_type`: This attribute is set to "zombie".
   - `points`: The zombie is worth 5 points.

  #### Distinct Methods:
   - `__init__`:
     - Initializes the `Zombie` with a specific position, player position, type, points, health points (hp), and size.
     - Depending on the zombie's initial position, it sets the action to either "*spawn_ground*" or "*spawn_coffin*".

   - `update`:
     - Overrides the `update` method of the `Enemy` class to include specific behaviors for the `Zombie`.
     - Adjusts the zombie's position and animation based on its state (e.g., spawning, moving, dying).
     - Controls the zombie's gravity and movement direction. The zombie can randomly choose to move left or right when it starts moving.
     - Handles collision with the environment and changes direction upon hitting a boundary.
     - Sets the zombie's action and size based on its spawning animation.


 #### **`Maddog`**

  ##### Distinct Attributes:
   - `player_pos`: This attribute holds the position of the player, used to determine the maddog's behavior or movements relative to the player.
   - `enemy_type`: This attribute is set to "maddog".
   - `points`: The maddog is worth 10 points.
   - `in_air`: Tracks how long the maddog has been in the air.
   - `attack_timer`: A timer used to control the frequency of the maddog's attacks, set to 60.
   - `jump_timer`: A timer used to control the frequency of the maddog's jumps, set to 60.
   - `jump`: A boolean indicating whether the maddog is currently jumping.
   - `activate_knockback`: Used to address a potential bug with entities changing size while in knockback.

  ##### Distinct Methods:
   - `__init__`:
     - Initializes the `Maddog` with a specific position, player position, type, points, health points (hp), and size.
     - Initializes additional attributes specific to the `Maddog, such as `in_air`, `attack_timer`, `jump_timer`, and `jump`.
     - Sets `activate_knockback` to `False`.

   - `update`:
     - Overrides the `update` method of the `Enemy` class to include specific behaviors for the `Maddog`.
     - Adjusts the maddog's position and animation based on its state (e.g., in air, jumping, attacking, dying).
     - Controls the maddog's gravity and movement direction. The maddog's movement speed increases when in the air.
     - Handles the maddog's jumping and attacking mechanics, setting appropriate actions and timers.
     - Adjusts the maddog's size and render position based on its current action and state.
     - Handles collision with the environment, updating the maddog's state and action upon landing.


 #### **`MaddogS`**
  Represents a stronger version of the Maddog, with basically the same distinct attributes and methods. 

  ##### Distinct Attributes:
   - `enemy_type`: This attribute is set to "maddogS".
   - `points`: The `MaddogS` is worth 15 points.
   - `in_air`: Tracks how long the `MaddogS` has been in the air.
   - `attack_timer`: Set to 30.
   - `jump_timer`: Set to 30.

  The `MaddogS` will jump and attack more frequently than the regular `Maddog` due to its shorter timers, and it will follow the player's movement while in the air.
  ```
    if self.in_air > 5 and not self.die:
        if self.player_pos[1] - self.pos[1] > 80 or self.player_pos[0] - self.pos[0] < 30 or self.player_pos[0] - self.pos[0] > 30:
            if self.player_pos[0] > self.pos[0]:
                self.velocity[0] += 1
            elif self.player_pos[0] < self.pos[0]:
                self.velocity[0] -= 1
  ```


 #### **`Ghost`**

  ##### Distinct Attributes:
   - `player_pos`: This attribute holds the position of the player, used to determine the `Ghost`'s behavior and movements relative to the player.
   - `enemy_type`: This attribute is set to "ghost".
   - `points`: The `Ghost` is worth 7 points.
   - `movingX_timer`: A timer to control the horizontal movement direction changes.
   - `movingY_timer`: A timer to control the vertical movement direction changes.
   - Nswirls: A counter for the number of swirls the ghost performs before spawning.
   `default_size`: Stores the default size of the ghost for resetting purposes.
   `spawn_timer`: A timer that determines when the ghost will spawn, chosen randomly from a set of values.

  ##### Distinct Methods:
   - `__init__`:
     - Initializes the `Ghost` with a specific position, player position, type, points, health points (hp), and size.
     - Initializes additional attributes specific to the `Ghost`, such as `movingX_timer`, `movingY_timer`, `Nswirls`, `default_size`, and `spawn_timer`.
     - Sets the initial action to "moving_ball".

   - `update`:
     - Overrides the `update` method of the `Enemy` class to include specific behaviors for the `Ghost`.
     - Adjusts the `Ghost`'s position and animation based on its state (e.g., moving ball, swirling, spawning, wandering, attacking, dying).
     - Handles the `Ghost`'s random movement in both horizontal and vertical directions.
     - Manages the spawning process, including timers and actions related to swirling and spawning.
     - Adjusts the `Ghost`'s size and render position based on its current action and state.
     - Controls the `Ghost`'s behavior based on the player's position, switching between wandering and attacking actions.
     - Handles the `Ghost`'s death, stopping movement and setting the appropriate action.

   - `random_movement`:
     - Controls the random movement of the `Ghost` in both horizontal and vertical directions.
     - Adjusts the velocity based on the `Ghost`'s position and randomly chosen directions.
     - Uses timers to periodically change the direction of movement.

   - `render`:
     - Overrides the `render` method of the `Enemy` class to include specific rendering behavior for the `Ghost`.
     - Adds a blinking effect when the ghost is not spawned and not in the death state.


### `Weapon`
 The `Weapon` class manages the properties and behaviors of different weapons used by the player in the game.

 #### Attributes:
  - `game`: Reference to the game object.
  - `type`: The type of weapon (e.g., "spear", "sword", "axe").
  - `weapons_power`: Dictionary holding the base damage and knockback values for each weapon type.
  - `damage_power`: Calculated damage based on the weapon type and player's power.
  - `knockback_power`: Calculated knockback based on the weapon type and player's power.
  - `pos`: List holding the position of the weapon.
  - `pos_adjust`: Boolean to ensure that the position when the weapon is created is adjusted only once.
  - `size`: Size of the weapon's sprite.
  - `velocity`: List holding the velocity of the weapon.
  - `collisions`: Boolean indicating if the weapon has collided with any entity or tile.
  - `hit`: Boolean indicating if the weapon has hit an enemy.
  - `hit_delay`: Delay timer before the weapon is deleted after hitting an enemy.
  - `Nhits`: Counter for the number of hits the weapon has made.
  - `delete`: Boolean indicating if the weapon should be deleted.
  - `flip`: Boolean indicating the direction the weapon's sprite should be flipped.
  - `weapon`: Holds the current weapon sprite or animation.
  - `hitFalse_animation`: Boolean for animation played when the weapon hits something but doesn't damage it.
  - `hitTrue_animation`: Boolean for animation played when the weapon successfully hits and damages an enemy.
  - `hit_animation_dur`: Duration of the hit animation.

 #### Methods:
  - `__init__(self, game, w_type, pos, flip, player_power)`: Initializes the `Weapon` with the game reference, weapon type, position, flip status, and player power.

  - `rect(self)`: Returns a `pygame.Rect` object representing the weapon's rectangular area based on its position and size.

  - `set_weapon(self, weapon)`: Sets the weapon sprite based on the weapon type.

  - `show_hitbox(self, surf, color=(0, 0, 200))`:Draws the weapon's hitbox on the given surface for debugging purposes.

  - `gravity(self, x=0.1)`: Applies gravity to the weapon by increasing its vertical velocity.

  - `update(self, movement=(0, 0), tiles=None, entities=None)`: Adjusts the weapon's position based on its velocity and movement, and handles collisions with enemies and tiles, updating the weapon's state and animation accordingly.

  - `render(self, surf)`: Renders the weapon's sprite on the given surface, flipping it if necessary.


### Weapon types
 For every weapon type in the game, a subclass of the Weapon class is created. Here are the distinct attributes and methods for those classes:

 #### **`Spear`**

  ##### Distinct Attributes:
  - `index`: An integer set to 1, used for identifying the weapon.
  - `damage_power`: Initially set to 2.0 before calling the parent constructor, which sets the final value.
  
  ##### Distinct Methods:
   - `__init__`:
     - Plays a specific sound effect for throwing a spear upon initialization.
   - `update`:
     - The amount of horizontal velocity aplied for the spear is **`4`**.
     - Sets horizontal velocity based on the `flip` attribute to move the spear in the correct direction.
     - Adjusts the position of the spear when it hits an enemy or obstacle, providing specific visual feedback. 


 #### **`Sword`**

  ##### Distinct Attributes:
   - `index`: An integer set to 2, used for identifying the weapon.
   - `damage_power`: Initially set to 1.5 before calling the parent constructor, which sets the final value.

  ##### Distinct Methods:
   - `__init__`:
     - Plays a specific sound effect for throwing a sword upon initialization.
  
   - `update`:
     - The amount of horizontal velocity applied for the sword is **`5`**.
     - Sets horizontal velocity based on the `flip` attribute to move the sword in the correct direction.
     - Adjusts the position of the sword when it hits an enemy or obstacle, providing specific visual feedback. 


 #### **`Axe`**

  ##### Distinct Attributes:
   - `index`: An integer set to 3, used for identifying the weapon.
   - `damage_power`: Initially set to 4.5 before calling the parent constructor, which sets the final value.

  ##### Distinct Methods:
   - `__init__`:
     - Sets an initial vertical velocity of **`-5`** to give the axe a slight upward motion when thrown.
     - Plays a specific sound effect for throwing an axe upon initialization.
  
   - `update`:
     - The amount of horizontal velocity applied for the axe is **`3`**.
     - Sets horizontal velocity based on the `flip` attribute to move the axe in the correct direction.
     - Adjusts the position of the axe when it hits an enemy or obstacle, providing specific visual feedback.
     - Calls a custom `gravity` method to continuously apply gravity with a slightly increased effect.
   - `gravity`:
     - Increases the vertical velocity by **`0.2`** per call, overriding the default gravity method to simulate a heavier fall.


### `Item`
 The `Item` class manages the properties and behaviors of different items that can be found and used in the game.

 #### Attributes:
  - `game`: Reference to the game object.
  - `type`: The type of item (e.g., "hp_up").
  - `pos`: List holding the position of the item.
  - `size`: Size of the item's sprite.
  - `velocity`: List holding the velocity of the item.
  - `collisions`: Boolean indicating if the item has collided with any tile.
  - `drop`: Boolean indicating if the item has been dropped.
  - `pick_up`: Boolean indicating if the item has been picked up by the player.
  - `delete`: Boolean indicating if the item should be deleted.
  - `item`: Holds the current item sprite or animation.
  - `renderPos_x`: Adjusts the render X position of the sprite.
  - `renderPos_y`: Adjusts the render Y position of the sprite.
  - `blink_timer`: Timer used for the item's blink animation.

 #### Methods:
  - `__init__(self, game, item_type, pos)`: Initializes the `Item` with the game reference, item type, and position.
  
  - `rect(self)`: Returns a `pygame.Rect` object representing the item's rectangular area based on its position and size.
  
  - `show_hitbox(self, surf, color=(200, 0, 100))`: Draws the item's hitbox on the given surface for debugging purposes.
  
  - `set_item(self, item)`: Sets the item sprite based on the item type.
  
  - `gravity(self, x=0.1)`: Applies gravity to the item by increasing its vertical position.
  
  - `update(self, player, tiles=None)`: 
    - Adjusts the item's position based on gravity and handles collisions with tiles.
    - Checks for collisions with the player, marking the item for deletion if picked up.
    - Adjusts the item's position to stay within bounds.
  
- `render(self, surf)`: Renders the item's sprite on the given surface, implementing a blinking effect for dropped items.


### `WeaponDrop`
 The `WeaponDrop` class inherits from the `Item` class and represents a dropped weapon item in the game.

 #### Distinct Attributes:
  - `renderPos_x`: Adjusted to -6 to properly center the sprite due to its different size.
  - `renderPos_y`: Adjusted to -6 to properly center the sprite due to its different size.

 #### Distinct Methods:
  - `__init__(self, game, weapon_type, pos)`: Initializes the `WeaponDrop` with the game reference, weapon type, and position, and adjusts the rendering position for the sprite.

  - `update(self, player, tiles=None)`: Calls the parent class's `update` method to handle the standard item update behavior, including gravity, collision detection, and interaction with the player.
