# coding: utf-8
'''
This is part 3 of the pythonista game tutorial, with very minor additions.
The graphic: https://opengameart.org/content/the-knight-free-sprite
The song: https://opengameart.org/content/battle-theme-a
'''

from scene import *
import sound

player = sound.Player('battleThemeA.mp3')
player.number_of_loops = -1

def cmp(a, b):
        return ((a > b) - (a < b))

standing_texture = Texture('Idle.png',)
walk_textures = [Texture('Walk 1.png'), Texture('Walk 2.png'), Texture('Walk 3.png'), Texture('Walk 4.png'), Texture('Walk 5.png'), Texture('Walk 6.png'), Texture('Walk 7.png'), Texture('Walk 8.png'), Texture('Walk 9.png'), Texture('Walk 10.png')]

class Game (Scene):
        def setup(self):
                self.background_color = '#7bc7ff'
                ground = Node(parent=self)
                x = 0
                while x <= self.size.w + 64:
                        tile = SpriteNode('plf:Ground_Grass', position=(x, 0))
                        ground.add_child(tile)
                        x += 64
                self.player = SpriteNode(standing_texture)
                self.player.anchor_point = (0.5, 0)
                self.player.position = (self.size.w/2, 20)
                self.add_child(self.player)
                self.walk_step = -1
                player.play()

        def touch_began(self, touch):
                if touch.location.x < 48 and touch.location.y > self.size.h - 48:
                        self.show_pause_menu()
                        return
                selected = [s for s in self.tiles if s.selected]
                if selected:
                        return
                t = self.tile_for_touch(touch)
                if t:
                        sound.play_effect('ui:click2')
                        self.select_from(t)

        def stop(self):
                player.stop()

        def update(self):

                g = gravity()
                if abs(g.x) > 0.05:
                        self.player.x_scale = cmp(g.x, 0)
                        x = self.player.position.x
                        max_speed = 40
                        x = max(0, min(self.size.w, x + g.x * max_speed))
                        self.player.position = x, 20
                        step = int(self.player.position.x / 20) % 10
                        if step != self.walk_step:
                                self.player.texture = walk_textures[step]
                                sound.play_effect('rpg:Footstep00', 0.05, 1.0 + 0.5 * step)
                                self.walk_step = step
                else:
                        self.player.texture = standing_texture
                        self.walk_step = -1

if __name__ == '__main__':
        run(Game(), PORTRAIT, show_fps=True)
