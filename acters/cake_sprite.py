from utils.sprite_loader import load_sprite_sheet


class CakeSprite(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(CakeSprite, cls).__new__(cls)
      cls.cake_frames = load_sprite_sheet('assets/cakes/not_a_cake.png', 3, 2, 100, 114)
    return cls.instance
    