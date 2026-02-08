from utils.sprite_loader import load_sprite_sheet


class MeteorSprite(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(MeteorSprite, cls).__new__(cls)
      cls.meteor_frames = load_sprite_sheet('assets/meteor/meteor.png', 2, 2, 580, 160)
    return cls.instance
    