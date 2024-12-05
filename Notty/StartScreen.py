import pygame

class StartScreen(ScreenBase):
    def __init__(self):
        super().__init__(pygame.Color('black'))

        pygame.mixer.init()
        pygame.mixer.music.load('Assets/music.mp3')  # 替换为你的音乐文件路径
        pygame.mixer.music.play(-1)  # 无限循环播放音乐

        # 添加标题
        title_text = "WELCOME TO THE NOTTY GAME!"
        title_colors = [pygame.Color('red'), pygame.Color('yellow'), pygame.Color('blue'), pygame.Color('green')]
        title_pos = (
            (WINDOW_WIDTH - sum([pygame.font.Font('Fonts/PressStart2P-Regular.ttf', 36).render(c, True, title_colors[i % len(title_colors)]).get_width() for i, c in enumerate(title_text)])) // 2,
            100
        )
        title = MulticolorLabel(title_text, title_pos, title_colors)
        self.objects.append(title)

        # 添加“玩家人数”标签
        num_players_label = Label('NUMBER OF PLAYERS:', (0, 0), pygame.Color('white'))
        num_players_label.pos = (
            (WINDOW_WIDTH - num_players_label.font.size('NUMBER OF PLAYERS:')[0]) // 2,
            200
        )
        self.objects.append(num_players_label)

        # 添加玩家人数按钮
        btn_padding = 50  # 按钮间距
        btn_width = 50    # 按钮宽度
        total_btn_width = 2 * btn_width + btn_padding

        self.objects.append(PlayerNumberLabel(
            '2',
            ((WINDOW_WIDTH - total_btn_width) // 2, 400),
            pygame.Color('white'),
            pygame.Color('red')
        ))

        self.objects.append(PlayerNumberLabel(
            '3',
            ((WINDOW_WIDTH + btn_width) // 2, 400),
            pygame.Color('white'),
            pygame.Color('red')
        ))

        # 添加“规则”按钮
        rules_text = "CLICK HERE TO READ THE GAME RULES!"
        rules_label = RuleLabel(rules_text, (0, 0), pygame.Color('white'), pygame.Color('red'))
        rules_label.pos = (
            (WINDOW_WIDTH - rules_label.font.size(rules_text)[0]) // 2,
            600
        )
        self.objects.append(rules_label)
