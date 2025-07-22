#  main.py  –  wersja kompatybilna z CPython-WASM
import sys, os, pathlib, asyncio
import pygame

from settings import *
from level    import Level
from menu     import Menu

BASE_DIR = pathlib.Path(__file__).parent
if sys.platform == "emscripten":
    os.chdir(BASE_DIR)

pygame.init()

class Game:
    def __init__(self):
        # 1. Main display screen - without SCALED
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        
        # 2. Internal surface for drawing at native resolution
        self.internal_surface = pygame.Surface((screen_width, screen_height))
        
        pygame.display.set_caption("Jumper")
        self.clock = pygame.time.Clock()
        self.last_time = pygame.time.get_ticks()

        # 3. Pass the internal_surface to game objects
        self.menu  = Menu(self.internal_surface)
        self.level = Level(self.internal_surface)

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # In browser, just breaking the loop is better
                if sys.platform != "emscripten":
                    pygame.quit()
                    sys.exit()
                else:
                    # This will need to be handled in the main loop
                    # For now, let's make it compatible.
                    # A better approach is to set a flag to break the main loop.
                    raise SystemExit

    def get_dt(self):
        if sys.platform != "emscripten":
            return self.clock.tick(FPS) / 1000
        else:
            current_time = pygame.time.get_ticks()
            dt = (current_time - self.last_time) / 1000.0  # Convert to seconds
            self.last_time = current_time
            return min(dt, 0.1)

    def update(self, dt):
        # Game logic runs on the internal_surface
        if self.menu.active:
            self.menu.run()
        else:
            # This is the first frame after leaving the menu.
            # It's safe to start music now.
            self.level.start_music()
            
            self.level.player_sprite.character_path = self.menu.player_graph
            self.level.player_sprite.import_character_assets()
            self.level.run()

    def draw(self):
        # 4. Scale the internal_surface to the main screen
        self.screen.blit(pygame.transform.scale(self.internal_surface, self.screen.get_rect().size), (0, 0))
        pygame.display.update()

game = Game()

# ──────────────────────────────────────────────────────────────
async def main():
    """Pętla zgodna z wymogami Pyodide / Pygbag."""
    try:
        while True:
            game.handle_events()
            dt = game.get_dt()
            game.update(dt)
            game.draw()
            await asyncio.sleep(0)
    except SystemExit:
        # Gracefully exit the loop in browser
        pass
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    asyncio.run(main())