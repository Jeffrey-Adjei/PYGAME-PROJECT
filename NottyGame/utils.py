import itertools
import pygame
import os

def load_card_images():
    card_images = {}
    colors = ['red', 'blue', 'green', 'yellow']
    numbers = range(1, 11)
    for color in colors:
        for number in numbers:
            image_filename = f"{color}_{number}.png"
            image_path = os.path.join('assets', 'images', 'cards', image_filename)
            if os.path.exists(image_path):
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (Card.CARD_WIDTH, Card.CARD_HEIGHT))
                card_images[f"{color}_{number}"] = image
            else:
                print(f"Warning: Image {image_path} not found.")
    return card_images

# utils.py (continue from previous code)

def is_valid_group(group):
    if len(group) < 3:
        return False
    colors = [card.color for card in group]
    numbers = [card.number for card in group]

    # Check for Set: Same number, different colors
    if len(set(numbers)) == 1 and len(set(colors)) == len(colors):
        return True

    # Check for Sequence: Same color, consecutive numbers
    if len(set(colors)) == 1:
        sorted_numbers = sorted(numbers)
        expected_sequence = list(range(min(numbers), max(numbers) + 1))
        if sorted_numbers == expected_sequence:
            return True

    return False

def find_possible_groups(hand):
    groups = []
    # Find sets (same number, different colors)
    numbers = set(card.number for card in hand)
    for number in numbers:
        same_number_cards = [card for card in hand if card.number == number]
        colors = set(card.color for card in same_number_cards)
        if len(colors) >= 3:
            # Get combinations without color repeats
            unique_color_cards = []
            seen_colors = set()
            for card in same_number_cards:
                if card.color not in seen_colors:
                    unique_color_cards.append(card)
                    seen_colors.add(card.color)
            if len(unique_color_cards) >= 3:
                groups.append(unique_color_cards)
    # Find sequences (same color, consecutive numbers)
    colors = set(card.color for card in hand)
    for color in colors:
        same_color_cards = [card for card in hand if card.color == color]
        numbers = sorted(set(card.number for card in same_color_cards))
        # Check for consecutive sequences
        for i in range(len(numbers)):
            for j in range(i + 3, len(numbers) + 1):
                sequence = numbers[i:j]
                if sequence == list(range(sequence[0], sequence[-1] + 1)):
                    sequence_cards = [card for card in same_color_cards if card.number in sequence]
                    groups.append(sequence_cards)
    return groups
