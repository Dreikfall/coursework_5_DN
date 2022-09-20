from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        '''НАЧАЛО ИГРЫ -> None
        присваиваем экземпляру класса аттрибуты "игрок" и "противник"
        также выставляем True для свойства "началась ли игра"'''

        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        '''ПРОВЕРКА ЗДОРОВЬЯ ИГРОКА И ВРАГА
        проверка здоровья игрока и врага и возвращение результата строкой:
        может быть три результата:
        Игрок проиграл битву, Игрок выиграл битву, Ничья и сохраняем его в аттрибуте (self.battle_result)
        если Здоровья игроков в порядке то ничего не происходит'''

        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = self._end_game()
            return self.battle_result
        if self.player.hp <= 0:
            self.battle_result = self._end_game('win_enemy')
            return self.battle_result
        if self.enemy.hp <= 0:
            self.battle_result = self._end_game('win_player')
            return self.battle_result

    def _stamina_regeneration(self):
        '''регенерация здоровья и стамины для игрока и врага за ход
                в этом методе к количеству стамины игрока и врага прибавляется константное значение.
                главное чтобы оно не привысило максимальные значения (используйте if)'''

        player_stamina_gain = self.STAMINA_PER_ROUND * self.player.unit_class.stamina
        if self.player.stamina < self.player.unit_class.max_stamina:
            self.player.stamina += player_stamina_gain
            if self.player.stamina > self.player.unit_class.max_stamina:
                self.player.stamina = self.player.unit_class.max_stamina
        enemy_stamina_gain = self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina
        if self.enemy.stamina < self.enemy.unit_class.max_stamina:
            self.enemy.stamina += enemy_stamina_gain
            if self.enemy.stamina > self.enemy.unit_class.max_stamina:
                self.enemy.stamina = self.enemy.unit_class.max_stamina

    def next_turn(self):
        '''срабатывает когда игроп пропускает ход или когда игрок наносит удар.
                создаем поле result и проверяем что вернется в результате функции self._check_players_hp
                если result -> возвращаем его
                если же результата пока нет и после завершения хода игра продолжается,
                тогда запускаем процесс регенирации стамины и здоровья для игроков (self._stamina_regeneration)
                и вызываем функцию self.enemy.hit(self.player) - ответный удар врага'''
        result = self._check_players_hp()
        if result:
            return result
        self._stamina_regeneration()
        self.enemy.hit(self.player)

    def _end_game(self, result='draw'):
        '''КНОПКА ЗАВЕРШЕНИЕ ИГРЫ - > return result: str
        очищаем синглтон - self._instances = {}
        останавливаем игру (game_is_running)
        возвращаем результат'''

        self._instances = {}
        self.game_is_running = False
        if result == 'win_player':
            return 'Игрок выиграл битву'
        if result == 'win_enemy':
            return 'Игрок проиграл битву'
        return 'Ничья'

    def player_hit(self):
        '''КНОПКА УДАР ИГРОКА -> return result: str
        получаем результат от функции self.player.hit
        запускаем следующий ход
        возвращаем результат удара строкой'''

        result = self.player.hit(self.enemy)
        self.next_turn()
        return result

    def player_use_skill(self):
        '''КНОПКА ИГРОК ИСПОЛЬЗУЕТ УМЕНИЕ
            получаем результат от функции self.use_skill
            включаем следующий ход
            возвращаем результат удара строкой'''

        result = self.player.use_skill(self.enemy)
        self.next_turn()
        return result

