from scuttlebuddy.Types import Vector3, Process, Vector2
import scuttlebuddy.Offsets as Offsets
import pyMeow as pm
import ctypes
import numpy

class Spell:
    def __init__(self, spell_address: int, process: Process) -> None:
        self.spell_address: int = spell_address
        self.process: Process = process

    @property
    def level(self) -> int:
        return pm.r_int(self.process, self.spell_address + Offsets.SpellSlotLevel)

class World:
    def __init__(self, process: Process, base_address: int) -> None:
        self.process: Process = process
        self.base_address: int = base_address

        # Window dimensions
        self.width, self.height = None, None
        self.__populate_window_dimensions()

    def get_view_proj_matrix(self):
        data = pm.r_bytes(self.process, self.base_address + Offsets.ViewProjMatrix, 0x128)
        view_matrix = numpy.frombuffer(data[:64], dtype=numpy.float32).reshape(4, 4)
        proj_matrix = numpy.frombuffer(data[64:128], dtype=numpy.float32).reshape(4, 4)
        return numpy.matmul(view_matrix, proj_matrix)
    
    def world_to_screen(self, view_proj_matrix, gamePos: Vector3) -> Vector2:
        clip_coords = numpy.matmul(numpy.array([gamePos['x'], gamePos['y'], gamePos['z'], 1.0]), view_proj_matrix.reshape(4, 4))
        if clip_coords[3] <= 0:
            clip_coords[3] = 0.1
        
        clip_coords /= clip_coords[3]
        return Vector2(
            x=int((self.width / 2.0 * clip_coords[0]) + (clip_coords[0] + self.width / 2.0)),
            y=int(-(self.height / 2.0 * clip_coords[1]) + (clip_coords[1] + self.height / 2.0))
        )

    def __populate_window_dimensions(self) -> None:
        pm.overlay_init("League of Legends (TM) Client")
        self.width, self.height = pm.get_screen_width(), pm.get_screen_height()
        


# region Entities
class Entity:
    def __init__(self, entity_address: int, process: Process, world: World) -> None:
        self.process: Process = process
        self.entity_address: int = entity_address
        self.world: World = world

    @property
    def name(self) -> str:
        return pm.r_string(self.process, self.entity_address + Offsets.ObjectName)

    @property
    def level(self) -> int:
        return pm.r_int(self.process, self.entity_address + Offsets.Level)

    @property
    def team_id(self) -> int:
        return pm.r_int(self.process, self.entity_address + Offsets.Team)

    @property
    def is_targetable(self) -> bool:
        return pm.r_bool(self.process, self.entity_address + Offsets.Targetable)

    @property
    def health(self) -> float:
        return pm.r_float(self.process, self.entity_address + Offsets.Health)

    @property
    def max_health(self) -> float:
        return pm.r_float(self.process, self.entity_address + Offsets.MaxHealth)

    @property
    def mana(self) -> float:
        return pm.r_float(self.process, self.entity_address + Offsets.Mana)

    @property
    def max_mana(self) -> float:
        return pm.r_float(self.process, self.entity_address + Offsets.MaxMana)

    @property
    def ap(self) -> float:
        return pm.r_float(self.process, self.entity_address + Offsets.AbilityPower)

    @property
    def ad(self) -> float:
        return pm.r_float(self.process, self.entity_address + Offsets.BaseAttackDamage) + pm.r_float(self.process, self.entity_address + Offsets.BonusAttackDamage)

    @property
    def bonus_attack_speed_percent(self) -> float:
        return pm.r_float(self.process, self.entity_address + Offsets.BonusAttackSpeed)

    @property
    def magic_resist(self) -> float:
        return pm.r_float(self.process, self.entity_address + Offsets.MagicResistance) + pm.r_float(self.process, self.entity_address + Offsets.BonusMagicResistance)

    @property
    def armor(self) -> float:
        return pm.r_float(self.process, self.entity_address + Offsets.Armor) + pm.r_float(self.process, self.entity_address + Offsets.BonusArmor)

    @property
    def magic_pen_flat(self) -> float:
        return pm.r_float(self.process, self.entity_address + Offsets.MagicPenetration)

    @property
    def magic_pen_percent(self) -> float:
        return None

    @property
    def armor_pen_percent(self) -> float:
        return None

    @property
    def lethality(self) -> float:
        return pm.r_float(self.process, self.entity_address + Offsets.Lethality)

    @property
    def attack_range(self) -> float:
        return pm.r_float(self.process, self.entity_address + Offsets.AttackRange)

    @property
    def game_pos(self) -> Vector3:
        pos = pm.r_vec3(self.process, self.entity_address + Offsets.HeroPosition)
        return pos

    @property
    def screen_pos(self) -> Vector2:
        return self.world.world_to_screen(self.world.get_view_proj_matrix(), self.game_pos)

    @property
    def is_visible(self) -> bool:
        return pm.r_bool(self.process, self.entity_address + Offsets.IsVisible)

    @property
    def on_screen(self) -> bool:
        screen_pos: Vector2 = self.screen_pos
        return screen_pos['x'] > 0 and screen_pos['x'] < self.world.width and screen_pos['y'] > 0 and screen_pos['y'] < self.world.height
    

class PlayerEntity(Entity):
    def __init__(self, entity_address, process: Process, world: World) -> None:
        super().__init__(entity_address=entity_address, process=process, world=world)

        self.__player_store: dict = {
            'spells': self.__setup_spells()
        }
    
    @property
    def spells(self) -> list:
        return self.__player_store['spells']

    # region Setup Functions
    def __setup_spells(self) -> list[Spell]:
        s: list[Spell] = []

        spell_book: list[int] = pm.r_ints64(self.process, self.entity_address + Offsets.SpellBook, 0x4)
        for spell_slot in spell_book:
            s.append(Spell(spell_slot, self.process))
        
        return s
    # endregion

class MinionEntity(Entity):
    def __init__(self, entity_address, process: Process, world: World) -> None:
        super().__init__(entity_address=entity_address, process=process, world=world)
# endregion
