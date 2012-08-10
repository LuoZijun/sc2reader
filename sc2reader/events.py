from __future__ import absolute_import

from sc2reader.utils import Length, LITTLE_ENDIAN
from sc2reader.data.utils import DataObject
from sc2reader.log_utils import loggable

@loggable
class Event(object):
    def __init__(self, frame, pid):
        self.pid = pid
        self.frame = frame
        self.second = frame >> 4
        self.time = Length(seconds=self.second)
        if not hasattr(self, 'name'):
            self.name = self.__class__.__name__

    def load_context(self, replay):
        if self.pid != 16:
            self.player = replay.person[self.pid]

@loggable
class GameEvent(Event):
    """Abstract Event Type, should not be directly instanciated"""
    def __init__(self, frame, pid, event_type):
        super(GameEvent, self).__init__(frame, pid)

        self.type = event_type
        self.is_local = (pid != 16)

        self.is_init = (event_type == 0x00)
        self.is_player_action = (event_type == 0x01)
        self.is_camera_movement = (event_type == 0x03)
        self.is_unknown = (event_type == 0x02 or event_type == 0x04 or event_type == 0x05)

    def _str_prefix(self):
        player_name = self.player.name if self.is_local else "Global"
        return "%s\t%-15s " % (Length(seconds=int(self.frame/16)), player_name)

    def __str__(self):
        return self._str_prefix() + self.name

#############################################3
# Message Events
#########################

@loggable
class MessageEvent(Event):
    def __init__(self, frame, pid, flags):
        super(MessageEvent, self).__init__(frame, pid)
        self.flags=flags

@loggable
class ChatEvent(MessageEvent):
    def __init__(self, frame, pid, flags, target, text):
        super(ChatEvent, self).__init__(frame, pid, flags)
        self.target = target
        self.text = text
        self.to_all = (self.target == 0)
        self.to_allies = (self.target == 2)
        self.to_observers = (self.target == 4)

@loggable
class PacketEvent(MessageEvent):
    def __init__(self, frame, pid, flags, info):
        super(PacketEvent, self).__init__(frame, pid, flags)
        self.info = info

@loggable
class PingEvent(MessageEvent):
    def __init__(self, frame, pid, flags, x, y):
        super(PingEvent, self).__init__(frame, pid, flags)
        self.x, self.y = x, y


#############################################3
# Game Events
#########################

class UnknownEvent(GameEvent):
    pass

class PlayerJoinEvent(GameEvent):
    def __init__(self, frames, pid, event_type, flags):
        super(PlayerJoinEvent, self).__init__(frames, pid, event_type)
        self.flags = flags

class GameStartEvent(GameEvent):
    pass

class PlayerLeaveEvent(GameEvent):
	pass

class CameraEvent(GameEvent):
    def __init__(self, frames, pid, event_type, x, y, distance, pitch, yaw, height_offset):
        super(CameraEvent, self).__init__(frames, pid, event_type)
        self.x, self.y = x, y
        self.distance = distance
        self.pitch = pitch
        self.yaw = yaw
        self.height_offset = height_offset

    def __str__(self):
        return self._str_prefix() + " camera at ({}, {})".format(x,y)

class PlayerActionEvent(GameEvent):
    pass

@loggable
class SendResourceEvent(PlayerActionEvent):
    def __init__(self, frames, pid, event_type, target, minerals, vespene, terrazine, custom):
        super(SendResourceEvent, self).__init__(frames, pid, event_type)
        self.sender = pid
        self.reciever = target
        self.minerals = minerals
        self.vespene = vespene
        self.terrazine = terrazine
        self.custom = custom

    def __str__(self):
        return self._str_prefix() + " transfer {} minerals, {} gas, {} terrazine, and {} custom to {}" % (self.minerals, self.vespene, self.terrazine, self.custom, self.reciever)

    def load_context(self, replay):
        super(SendResourceEvent, self).load_context(replay)
        self.sender = replay.player[self.sender]
        self.reciever = replay.player[self.reciever]

@loggable
class RequestResourceEvent(PlayerActionEvent):
    def __init__(self, frames, pid, event_type, minerals, vespene, terrazine, custom):
        super(RequestResourceEvent, self).__init__(frames, pid, event_type)
        self.minerals = minerals
        self.vespene = vespene
        self.terrazine = terrazine
        self.custom = custom

    def __str__(self):
        return self._str_prefix() + " requests {} minerals, {} gas, {} terrazine, and {} custom" % (self.minerals, self.vespene, self.terrazine, self.custom)

@loggable
class AbilityEvent(PlayerActionEvent):
    def __init__(self, frame, pid, event_type, ability):
        super(AbilityEvent, self).__init__(frame, pid, event_type)
        self.ability_code = ability
        self.ability_name = 'Uknown'

    def load_context(self, replay):
        super(AbilityEvent, self).load_context(replay)
        if not replay.datapack:
            return

        if self.ability_code not in replay.datapack.abilities:
            if not getattr(replay, 'marked_error', None):
                replay.marked_error=True
                self.logger.error(replay.filename)
                self.logger.error("Release String: "+replay.release_string)
                for player in replay.players:
                    self.logger.error("\t"+str(player))

            print [hex(key) for key in replay.datapack.abilities.keys()]

            self.logger.error("{0}\t{1}\tMissing ability {2} from {3}".format(self.frame, self.player.name, hex(self.ability_code), replay.datapack.__class__.__name__))
            print "{0}\t{1}\tMissing ability {2} from {3}".format(self.frame, self.player.name, hex(self.ability_code), replay.datapack.id)

        else:
            self.ability_name = replay.datapack.abilities[self.ability_code].name


    def __str__(self):
        if not self.ability_code:
            return self._str_prefix() + "Move"
        else:
            return self._str_prefix() + "Ability (%s) - %s" % (hex(self.ability_code), self.ability_name)

@loggable
class TargetAbilityEvent(AbilityEvent):
    def __init__(self, frame, pid, event_type, ability, target, player, team, location):
        super(TargetAbilityEvent, self).__init__(frame, pid, event_type, ability)
        self.target = None
        self.target_id, self.target_type = target

        self.target_owner = None
        self.target_owner_id = player
        self.target_team = None
        self.target_team_id = team
        self.location = location

        # We can't know if it is a hallucination or not so assume not
        self.target_type = self.target_type << 8 | 0x01


    def load_context(self, replay):
        super(TargetAbilityEvent, self).load_context(replay)

        if self.target_owner_id:
            self.target_owner = replay.player[self.target_owner_id]

        """ Disabled since team seems to always be the same player
        if self.target_team_id:
            self.target_team = replay.team[self.target_team_id]
        """

        if not replay.datapack:
            return

        uid = (self.target_id, self.target_type)
        if uid in replay.objects:
            self.target = replay.objects[uid]

        else:
            if self.target_type not in replay.datapack.units:
                self.target = None
                print [hex(key) for key in replay.datapack.units]
                print "{0}\t{1}\tMissing unit {2} from {3}".format(self.frame, self.player.name, hex(self.target_type), replay.datapack.id)
            else:
                unit_class = replay.datapack.units[self.target_type]
                self.target = unit_class(self.target_id)
                replay.objects[uid] = self.target

    def __str__(self):
        if self.target:
            if isinstance(self.target, DataObject):
                target = "{0} [{1:0>8X}]".format(self.target.name, self.target.id)
            else:
                target = "{0:X} [{1:0>8X}]".format(self.target[1], self.target[0])
        else:
            target = "NONE"

        return AbilityEvent.__str__(self) + "; Target: {0}".format(target)

@loggable
class LocationAbilityEvent(AbilityEvent):
    def __init__(self, frame, pid, event_type, ability, location):
        super(LocationAbilityEvent, self).__init__(frame, pid, event_type, ability)
        self.location = location

    def __str__(self):
        return AbilityEvent.__str__(self) + "; Location: %s" % str(self.location)

@loggable
class SelfAbilityEvent(AbilityEvent):
    def __init__(self, frame, pid, event_type, ability, info):
        super(SelfAbilityEvent, self).__init__(frame, pid, event_type, ability)
        self.info = info

@loggable
class HotkeyEvent(PlayerActionEvent):
    def __init__(self, frame, pid, event_type, hotkey, deselect):
        super(HotkeyEvent, self).__init__(frame, pid, event_type)
        self.hotkey = hotkey
        self.deselect = deselect

class SetToHotkeyEvent(HotkeyEvent):
    pass

class AddToHotkeyEvent(HotkeyEvent):
    pass

class GetFromHotkeyEvent(HotkeyEvent):
    pass

@loggable
class SelectionEvent(PlayerActionEvent):
    def __init__(self, frame, pid, event_type, bank, objects, deselect):
        super(SelectionEvent, self).__init__(frame, pid, event_type)
        self.bank = bank
        self.objects = objects
        self.deselect = deselect

    def load_context(self, replay):
        super(SelectionEvent, self).load_context(replay)

        if not replay.datapack:
            return

        objects = list()
        data = replay.datapack
        for (obj_id, obj_type) in self.objects:
            if obj_type not in data.units:
                msg = "Unit Type {0} not found in {1}"
                self.logger.error(msg.format(hex(obj_type), data.__class__.__name__))
                objects.append(DataObject(0x0))

            else:
                if (obj_id, obj_type) not in replay.objects:
                    obj = data.units[obj_type](obj_id)
                    replay.objects[(obj_id,obj_type)] = obj
                else:
                    obj = replay.objects[(obj_id,obj_type)]

                objects.append(obj)

        self.objects = objects
