import pyMeow as pm

from typing import TypedDict, List
from scuttlebuddy.Models import PlayerEntity, World, MinionEntity, TurretEntity, WardEntity, Entity
import scuttlebuddy.Offsets as Offsets
from scuttlebuddy.Managers import ListReader
from scuttlebuddy.Stats import Stats

class LocalStore(TypedDict):
    world: World
    local_player: PlayerEntity
    team_players: List[PlayerEntity]
    enemy_players: List[PlayerEntity]


class LeagueReader:
    def __init__(self) -> None:
        # PyMeow Setup
        self.process = pm.open_process("League of Legends.exe")
        self.base_address = pm.get_module(self.process, "League of Legends.exe")['base']

        self.__world_obj: World = World(process=self.process, base_address=self.base_address)

        # Local store for performance cache
        self.__local_store: LocalStore = {
            'world': self.__world_obj,
            'local_player': PlayerEntity(
                entity_address=pm.r_int64(
                    self.process,
                    self.base_address + Offsets.LocalPlayer
                ),
                process=self.process,
                world=self.__world_obj
            )
        }

        # Manager Setup
        self.list_reader: ListReader = ListReader(
            process=self.process,
            base_address=self.base_address,
            local_team=self.local_player.team_id
        )

        # Stats Setup
        self.stats: Stats = Stats()

        # Populate Enemy/Team Players
        self.__setup_all_players()

    @property
    def world(self) -> World:
        return self.__local_store['world']

    @property
    def local_player(self) -> PlayerEntity:
        return self.__local_store['local_player']
    
    @property
    def team_players(self) -> List[PlayerEntity]:
        return self.__local_store['team_players']
    
    @property
    def enemy_players(self) -> List[PlayerEntity]:
        return self.__local_store['enemy_players']
    
    @property
    def all_players(self) -> List[PlayerEntity]:
        return self.team_players + self.enemy_players
    
    @property
    def team_minions(self) -> List[MinionEntity]:
        return self.get_entities(is_enemy=False, get_type="minion")
    
    @property
    def enemy_minions(self) -> List[MinionEntity]:
        return self.get_entities(is_enemy=True, get_type="minion")
    
    @property
    def all_minions(self) -> List[MinionEntity]:
        return self.get_entities(is_all=True, get_type="minion")
    
    @property
    def team_turrets(self) -> List[TurretEntity]:
        return self.get_entities(is_enemy=False, get_type="turret")
    
    @property
    def enemy_turrets(self) -> List[TurretEntity]:
        return self.get_entities(is_enemy=True, get_type="turret")
    
    @property
    def all_turrets(self) -> List[TurretEntity]:
        return self.get_entities(is_all=True, get_type="turret")
    
    # region Setup Functions
    def __setup_all_players(self) -> None:
        champion_pointers: List[int] = self.list_reader.get_pointers(Offsets.HeroList, self.stats.names, size=128, search_mode=0)

        team_champions: List[PlayerEntity] = []
        enemy_champions: List[PlayerEntity] = []
        for champ_p in champion_pointers:
            p = PlayerEntity(
                entity_address=champ_p,
                process=self.process,
                world=self.__world_obj
            )

            if p.team_id == self.local_player.team_id:
                team_champions.append(p)
            else:
                enemy_champions.append(p)
        
        self.__local_store['team_players'] = team_champions
        self.__local_store['enemy_players'] = enemy_champions

    # endregion

    # region Minion Helpers
    def get_entities(self, is_enemy: bool = False, is_all: bool = False, get_type: str = "minion") -> List[MinionEntity]:
        entity_pointers: List[int] = None
        match get_type:
            case "minion":
                entity_pointers = self.list_reader.get_pointers(Offsets.MinionList, size=512, search_mode=1)
            case "turret":
                entity_pointers = self.list_reader.get_pointers(Offsets.TurretList, size=64, search_mode=2)
            case "ward":
                entity_pointers = self.list_reader.get_pointers(Offsets.MinionList, size=512, search_mode=3)

        all_entities: List[Entity] = []
        team_entities: List[Entity] = []
        enemy_entities: List[Entity] = []
        for entity_p in entity_pointers:
            entity: Entity = None

            match get_type:
                case "minion":
                    entity = MinionEntity(
                        process=self.process,
                        entity_address=entity_p,
                        world=self.world
                    )
                case "turret":
                    entity = TurretEntity(
                        process=self.process,
                        entity_address=entity_p,
                        world=self.world
                    )
                case "ward":
                    entity = WardEntity(
                        process=self.process,
                        entity_address=entity_p,
                        world=self.world
                    )

            if is_all:
                all_entities.append(entity)
                continue

            is_team_entity: bool = entity.team_id == self.local_player.team_id

            if is_enemy and not is_team_entity:
                enemy_entities.append(entity)
            elif not is_enemy and is_team_entity:
                team_entities.append(entity)
        
        if is_all:
            return all_entities
        
        return enemy_entities if is_enemy else team_entities
    # endregion
