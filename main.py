import pygame
import random
import os
from pygame.locals import *

from game.game import Game
from Network.agent import DQNAgent

pygame.init()

def main(nn_playing=False):
    generation = 1
    
    game = Game()
    game.init_game()
    
    state_size = 8
    action_size = 3
    agent = DQNAgent(state_size, action_size)
    
    model_name = f"models/spaceinvaders_model_gen_{generation}.pkl"
    if not os.path.exists(model_name):
        model_name = "models/spaceinvaders_model.pkl"
    agent.load(model_name)
    
    batch_size = 32
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not nn_playing:
                    bullet = game.player.shoot()
                    if bullet:
                        game.all_sprites.add(bullet)
                        game.bullets.add(bullet)
                elif event.key == pygame.K_r and game.game_over and not nn_playing:
                    game.init_game()
                    game.score = 0
                    game.game_over = False
                elif event.key == pygame.K_a:
                    nn_playing = not nn_playing
                    print(f"NN {'enabled' if nn_playing else 'disabled'}")
        
        if not game.game_over:
            state = game.get_state()
            
            if nn_playing:
                action = agent.act(state)
                
                if random.random() < 0.1:
                    bullet = game.player.shoot()
                    if bullet:
                        game.all_sprites.add(bullet)
                        game.bullets.add(bullet)
                
                game_over = game.update(action)
                
                if game_over:
                    generation += 1
                    print(f"Generation {generation}, Max score: {game.score}")
                    agent = DQNAgent(state_size, action_size)
                    agent.save(f"models/spaceinvaders_model_gen_{generation}.pkl")
                    game.init_game()
                    game.score = 0
                    game.game_over = False
                
                if len(agent.memory) > batch_size:
                    agent.replay(batch_size)
                    
                    if random.random() < 0.001:
                        agent.save(f"models/spaceinvaders_model_gen_{generation}.pkl")
                        print("Model saved!")
            else:
                game.update()
        
        game.draw(nn_playing, generation)
    
    if nn_playing:
        agent.save(f"models/spaceinvaders_model_gen_{generation}.pkl")
    
    pygame.quit()

if __name__ == "__main__":
    main(nn_playing=True)